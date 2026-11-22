import ast
import os
from pathlib import Path
import shutil
from unittest.mock import Mock

import joblib
import nbformat
import numpy as np
import pandas as pd
import pytest
from sklearn.ensemble import RandomForestRegressor
from sklearn.exceptions import NotFittedError
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.utils.validation import check_is_fitted

HERE = Path(__file__).resolve().parent
RAW = ['distance_km', 'trip_duration_hours', 'payload_kg', 'ambient_temperature_c', 'idle_minutes']
NUM = RAW + ['start_hour', 'average_speed_kmph']
CAT = ['depot_code', 'vehicle_type', 'route_type']
FEATURES = NUM + CAT
TARGET = 'fuel_consumed_litres'
OUT = 'predicted_fuel_consumed_litres'


def load_notebook_definitions():
    candidates = [
        os.environ.get('MS2_NOTEBOOK'),
        'solution_with_code.ipynb',
        'solution.ipynb',
        'solution1.ipynb',
        'solution_p1.ipynb',
        'solution_p2.ipynb',
    ]
    candidates = [name for name in candidates if name]
    notebook_path = next((HERE / name for name in candidates if (HERE / name).is_file()), None)
    if notebook_path is None:
        raise FileNotFoundError('No supported notebook found. Expected one of: ' + ', '.join(candidates))

    notebook = nbformat.read(str(notebook_path), as_version=4)
    ns = {'__name__': 'notebook_under_test'}
    allowed_nodes = (
        ast.Import,
        ast.ImportFrom,
        ast.FunctionDef,
        ast.AsyncFunctionDef,
        ast.ClassDef,
    )

    for cell in notebook.cells:
        if cell.cell_type != 'code' or not cell.source.strip():
            continue
        tree = ast.parse(cell.source, filename=str(notebook_path))
        filtered = []
        for node in tree.body:
            if isinstance(node, allowed_nodes):
                filtered.append(node)
            elif isinstance(node, (ast.Assign, ast.AnnAssign)):
                value_node = node.value
                if value_node is not None and not any(isinstance(n, ast.Call) for n in ast.walk(value_node)):
                    filtered.append(node)
        tree.body = filtered
        if tree.body:
            ast.fix_missing_locations(tree)
            exec(compile(tree, str(notebook_path), 'exec'), ns)

    return ns


@pytest.fixture(scope='module')
def api():
    return load_notebook_definitions()


@pytest.fixture
def records():
    return pd.DataFrame({
        'trip_id': ['Z9', 'B2', 'C3', 'D4'],
        'trip_start_ts': ['2025-01-25 09:15:00', '26/01/2025 17:40', '2025-02-03 00:05:00', '2025-02-04 12:10:00'],
        'distance_km': [100, 60, 160, 25],
        'trip_duration_hours': [2, 3, 4, 1],
        'payload_kg': [500, 900, 200, 100],
        'ambient_temperature_c': [25, 30, 27, 29],
        'idle_minutes': [10, 5, 0, 8],
        'depot_code': ['pune', 'mumbai', 'pune', 'nashik'],
        'vehicle_type': ['van', 'light_truck', 'van', 'medium_truck'],
        'route_type': ['urban', 'highway', 'mixed', 'urban'],
        TARGET: [14.0, 12.0, 19.0, 6.0],
        'export_note': ['a', 'b', 'c', 'd'],
    })


def write(df, tmp_path, name='fixture.csv'):
    path = tmp_path / name
    df.to_csv(path, index=False)
    return str(path)


@pytest.fixture
def cleaned(api, records, tmp_path):
    return api['load_data'](write(records, tmp_path))


@pytest.fixture(scope='module')
def supervised(api):
    return api['prepare_datasets'](str(HERE / 'fleet_train.csv'), str(HERE / 'fleet_test.csv'))


@pytest.fixture(scope='module')
def fitted(api, supervised):
    X_train, _, y_train, _ = supervised
    return api['train_models'](X_train, y_train)


def test_t01_duplicate_id(api, records, tmp_path):
    dup = records.iloc[[0]].assign(distance_km=999)
    actual = api['load_data'](write(pd.concat([records, dup]), tmp_path))
    assert actual.trip_id.tolist() == records.trip_id.tolist()
    assert actual.iloc[0].distance_km == 100


def test_t02_invalid_timestamp(api, records, tmp_path):
    records.loc[1, 'trip_start_ts'] = 'not-date'
    records.loc[2, 'trip_start_ts'] = None
    actual = api['load_data'](write(records, tmp_path))
    assert actual.trip_id.tolist() == ['Z9', 'D4']
    assert pd.api.types.is_datetime64_any_dtype(actual.trip_start_ts)


def test_t03_mixed_formats(cleaned):
    assert cleaned.start_hour.tolist() == [9, 17, 0, 12]
    assert cleaned.trip_start_ts.dt.month.tolist() == [1, 1, 2, 2]
    assert cleaned.trip_start_ts.dt.day.tolist() == [25, 26, 3, 4]


def test_t04_numeric_conversion(api, records, tmp_path):
    for col in RAW:
        records[col] = ['12.5', 'bad', 'inf', None]
    actual = api['load_data'](write(records, tmp_path))
    for col in RAW:
        assert pd.api.types.is_numeric_dtype(actual[col])
        assert actual[col].iloc[0] == 12.5
        assert actual[col].iloc[1:].isna().all()


def test_t05_category_normalization(api, records, tmp_path):
    for col in CAT:
        records[col] = ['  MiXeD ', ' ', None, ' NORMAL ']
    actual = api['load_data'](write(records, tmp_path))
    for col in CAT:
        assert actual[col].tolist() == ['mixed', 'unknown', 'unknown', 'normal']


def test_t06_speed(api, records, tmp_path):
    records['trip_duration_hours'] = [2, 0, -3, np.nan]
    actual = api['load_data'](write(records, tmp_path))
    assert actual.average_speed_kmph.iloc[0] == 50
    assert actual.average_speed_kmph.iloc[1:].isna().all()


def test_t07_preserve_columns(cleaned, records):
    assert cleaned.trip_id.tolist() == records.trip_id.tolist()
    assert cleaned[TARGET].tolist() == records[TARGET].tolist()
    assert cleaned.export_note.tolist() == records.export_note.tolist()


def test_t08_pipeline(api):
    estimator = LinearRegression()
    pipe = api['build_pipeline'](estimator)
    assert isinstance(pipe, Pipeline)
    assert pipe.steps[-1][1] is estimator
    with pytest.raises(NotFittedError):
        check_is_fitted(pipe)
    transformers = pipe.steps[0][1].transformers
    assert len(transformers) == 2
    assert any(list(cols) == NUM for _, _, cols in transformers)
    assert any(list(cols) == CAT for _, _, cols in transformers)


def test_t09_imputation_scaling(api, cleaned):
    X = cleaned[FEATURES].copy()
    X['distance_km'] = [10.0, 20.0, np.nan, 100.0]
    pipe = api['build_pipeline'](LinearRegression()).fit(X, cleaned[TARGET])
    num_step = next(t for _, t, cols in pipe.steps[0][1].transformers_ if list(cols) == NUM)
    assert num_step.steps[0][1].strategy == 'median'
    assert num_step.steps[0][1].statistics_[0] == 20
    assert num_step.steps[1][1].mean_[0] == 37.5
    transformed = num_step.transform(X[NUM])
    assert np.allclose(transformed.mean(axis=0), 0, atol=1e-9)
    future = X.iloc[[0]].copy()
    future['distance_km'] = 5000.0
    pipe.predict(future)
    assert num_step.steps[0][1].statistics_[0] == 20


def test_t10_unknown_category(api, cleaned):
    pipe = api['build_pipeline'](LinearRegression()).fit(cleaned[FEATURES], cleaned[TARGET])
    new_data = cleaned[FEATURES].iloc[[0]].copy()
    for col in CAT:
        new_data[col] = 'unseen'
    assert np.isfinite(pipe.predict(new_data)).all()


def test_t11_prepare_types(supervised):
    X_train, X_test, y_train, y_test = supervised
    assert isinstance(X_train, pd.DataFrame) and isinstance(X_test, pd.DataFrame)
    assert isinstance(y_train, pd.Series) and isinstance(y_test, pd.Series)
    assert list(X_train.columns) == FEATURES == list(X_test.columns)
    assert len(X_train) == len(y_train) and len(X_test) == len(y_test)


def test_t12_invalid_targets(api, records, tmp_path):
    train = records.copy()
    train[TARGET] = ['14', 'bad', 'inf', None]
    test = records.copy()
    test[TARGET] = [None, '12', '-inf', '6']
    X_train, X_test, y_train, y_test = api['prepare_datasets'](
        write(train, tmp_path, 'tr.csv'),
        write(test, tmp_path, 'te.csv'),
    )
    assert y_train.tolist() == [14]
    assert X_train.distance_km.tolist() == [100]
    assert y_test.tolist() == [12, 6]
    assert X_test.distance_km.tolist() == [60, 25]
    assert X_train.index.equals(y_train.index)
    assert X_test.index.equals(y_test.index)


def test_t13_model_configuration(fitted):
    assert set(fitted) == {'linear_regression', 'random_forest'}
    assert isinstance(fitted['linear_regression'].steps[-1][1], LinearRegression)
    rf = fitted['random_forest'].steps[-1][1]
    assert isinstance(rf, RandomForestRegressor)
    for param, value in dict(n_estimators=150, max_depth=10, min_samples_leaf=2, random_state=42, n_jobs=-1).items():
        assert rf.get_params()[param] == value


def test_t14_fitted_models(fitted, supervised, monkeypatch):
    _, X_test, _, _ = supervised
    model_a, model_b = fitted.values()
    assert model_a is not model_b
    assert model_a.steps[0][1] is not model_b.steps[0][1]
    monkeypatch.setattr(Pipeline, 'fit', Mock(side_effect=AssertionError('Unexpected fit')))
    for model in fitted.values():
        check_is_fitted(model)
        pred = model.predict(X_test.iloc[:8])
        assert len(pred) == 8
        assert np.isfinite(pred).all()


def test_t15_metrics(api):
    X = pd.DataFrame({'x': [0, 1, 2, 3]})
    y = pd.Series([2, 4, 8, 12])
    model_a, model_b = Mock(), Mock()
    model_a.predict.return_value = np.array([1, 5, 7, 14])
    model_b.predict.return_value = np.array([3, 4, 8, 11])
    actual = api['evaluate_models']({'a': model_a, 'b': model_b}, X, y).set_index('model_name')
    for name, model in [('a', model_a), ('b', model_b)]:
        pred = model.predict.return_value
        assert np.allclose(
            actual.loc[name, ['mae', 'rmse', 'r2']].astype(float),
            [mean_absolute_error(y, pred), np.sqrt(mean_squared_error(y, pred)), r2_score(y, pred)],
        )


def test_t16_rank_rmse(api):
    X = pd.DataFrame({'x': [1, 2, 3, 4]})
    y = pd.Series([10, 20, 30, 40])
    model_a, model_b = Mock(), Mock()
    model_a.predict.return_value = np.array([10, 20, 30, 48])
    model_b.predict.return_value = np.array([13, 23, 33, 43])
    result = api['evaluate_models']({'a': model_a, 'b': model_b}, X, y)
    assert list(result.columns) == ['model_name', 'mae', 'rmse', 'r2']
    assert result.model_name.tolist() == ['b', 'a']
    assert list(result.index) == [0, 1]
    for model in [model_a, model_b]:
        model.fit.assert_not_called()


def test_t17_selection(api):
    model_a, model_b = Mock(), Mock()
    comparison = pd.DataFrame({'model_name': ['b', 'a'], 'rmse': [1.0, 5.0]})
    name, chosen = api['select_best_model'](comparison, {'a': model_a, 'b': model_b})
    assert name == 'b'
    assert chosen is model_b
    model_a.fit.assert_not_called()
    model_b.fit.assert_not_called()


def test_t18_prediction(api, cleaned):
    model = Mock()
    model.predict.return_value = np.array([-1.4, 2.36, 7.04, 0.0])
    result = api['predict_fuel'](model, cleaned)
    assert list(result.columns) == ['trip_id', OUT]
    assert result.trip_id.tolist() == cleaned.trip_id.tolist()
    assert result[OUT].tolist() == [0.0, 2.4, 7.0, 0.0]
    pd.testing.assert_frame_equal(model.predict.call_args.args[0], cleaned[FEATURES])
    model.fit.assert_not_called()


def test_t19_training_workflow(api, tmp_path, monkeypatch):
    for split in ['train', 'test']:
        shutil.copy(HERE / f'fleet_{split}.csv', tmp_path)
    monkeypatch.chdir(tmp_path)
    best_name, report = api['train']()
    saved = pd.read_csv('model_comparison.csv')
    pd.testing.assert_frame_equal(saved, report, check_exact=False)
    assert list(saved.columns) == ['model_name', 'mae', 'rmse', 'r2']
    assert saved.rmse.is_monotonic_increasing
    assert best_name == saved.iloc[0].model_name
    model = joblib.load('best_model.pkl')
    check_is_fitted(model)
    assert isinstance(model, Pipeline)
    expected_estimator_type = LinearRegression if best_name == 'linear_regression' else RandomForestRegressor
    assert isinstance(model.steps[-1][1], expected_estimator_type)


def test_t20_independent_prediction(api, tmp_path, monkeypatch, fitted):
    shutil.copy(HERE / 'fleet_predict.csv', tmp_path)
    monkeypatch.chdir(tmp_path)
    model = fitted['linear_regression']
    joblib.dump(model, 'best_model.pkl')
    expected = api['load_data']('fleet_predict.csv')
    expected_values = np.maximum(model.predict(expected[FEATURES]), 0).round(1)
    monkeypatch.setitem(api, 'train', Mock(side_effect=AssertionError('Unexpected training')))
    monkeypatch.setattr(Pipeline, 'fit', Mock(side_effect=AssertionError('Unexpected fit')))
    actual = api['predict']()
    saved = pd.read_csv('fleet_predictions.csv')
    pd.testing.assert_frame_equal(actual, saved, check_exact=False)
    assert list(saved.columns) == ['trip_id', OUT]
    assert saved.trip_id.tolist() == expected.trip_id.tolist()
    assert np.allclose(saved[OUT], expected_values)
