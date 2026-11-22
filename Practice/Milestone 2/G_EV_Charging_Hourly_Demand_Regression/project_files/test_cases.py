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
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_squared_log_error
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeRegressor
from sklearn.utils.validation import check_is_fitted

HERE = Path(__file__).resolve().parent
RAW = ['temperature_c', 'feels_like_c', 'humidity_pct', 'wind_speed_kmph', 'hour']
NUM = RAW[:4] + ['month', 'is_weekend', 'hour_sin', 'hour_cos']
CAT = ['season', 'weather_condition', 'holiday', 'working_day']
FEATURES = NUM + CAT
TARGET = 'session_count'
OUT = 'predicted_sessions'


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
        'observation_id': ['Z9', 'B2', 'C3', 'D4', 'E5', 'F6'],
        'observation_date': ['2025-01-24', '25/01/2025', '2025-01-26', '03/02/2025', '2025-02-04', '05/02/2025'],
        'hour': [0, 6, 12, 18, 23, 9],
        'temperature_c': [18, 24, 33, 21, 29, 25],
        'feels_like_c': [17, 25, 34, 22, 30, 26],
        'humidity_pct': [60, 70, 50, 75, 65, 66],
        'wind_speed_kmph': [2, 3, 5, 6, 9, 11],
        'season': ['winter'] * 6,
        'weather_condition': ['clear', 'rain', 'clear', 'cloudy', 'clear', 'rain'],
        'holiday': [0, 0, 1, 0, 0, 0],
        'working_day': [1, 0, 0, 1, 1, 1],
        TARGET: [4, 12, 20, 28, 0, 6],
        'member_sessions': [2, 8, 12, 19, 0, 3],
        'guest_sessions': [2, 4, 8, 9, 0, 3],
        'export_note': list('abcdef'),
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
    return api['prepare_datasets'](str(HERE / 'ev_train.csv'), str(HERE / 'ev_test.csv'))


@pytest.fixture(scope='module')
def fitted(api, supervised):
    X_train, _, y_train, _ = supervised
    return api['train_models'](X_train, y_train)


def test_t01_first_duplicate(api, records, tmp_path):
    duplicated = pd.concat([records, records.iloc[[0]].assign(temperature_c=99)])
    result = api['load_data'](write(duplicated, tmp_path))
    assert result.observation_id.tolist() == records.observation_id.tolist()
    assert result.temperature_c.iloc[0] == 18


def test_t02_dates(api, records, tmp_path):
    records.loc[4, 'observation_date'] = 'bad-date'
    records.loc[5, 'observation_date'] = None
    result = api['load_data'](write(records, tmp_path))
    assert result.observation_id.tolist() == ['Z9', 'B2', 'C3', 'D4']
    assert result.observation_date.dt.strftime('%Y-%m-%d').tolist() == [
        '2025-01-24',
        '2025-01-25',
        '2025-01-26',
        '2025-02-03',
    ]


def test_t03_numeric(api, records, tmp_path):
    for col in RAW:
        records[col] = ['12.5', 'bad', 'inf', '-inf', None, '4']
    result = api['load_data'](write(records, tmp_path))
    for col in RAW:
        assert pd.api.types.is_numeric_dtype(result[col])
        assert result[col].iloc[0] == 12.5
        assert result[col].iloc[5] == 4
        assert result[col].iloc[1:5].isna().all()


def test_t04_categories(api, records, tmp_path):
    doubled = pd.concat([records, records.assign(observation_id=lambda d: d.observation_id + 'X')], ignore_index=True)
    for col in CAT:
        doubled[col] = ['  MiXeD ', ' ', None, ' NORMAL ', '1.0', '2', '0.000', '+2.00', '-3.0', '2.50', 'abc.0', '1.01']
    result = api['load_data'](write(doubled, tmp_path))
    expected = ['mixed', 'unknown', 'unknown', 'normal', '1', '2', '0', '+2', '-3', '2.50', 'abc.0', '1.01']
    for col in CAT:
        assert result[col].tolist() == expected


def test_t05_month_weekend(cleaned):
    assert cleaned.month.tolist() == [1, 1, 1, 2, 2, 2]
    assert cleaned.is_weekend.tolist() == [0, 1, 1, 0, 0, 0]


def test_t06_cyclical_hour(cleaned):
    angles = 2 * np.pi * np.array([0, 6, 12, 18, 23, 9]) / 24
    np.testing.assert_allclose(cleaned.hour_sin, np.sin(angles), atol=1e-10)
    np.testing.assert_allclose(cleaned.hour_cos, np.cos(angles), atol=1e-10)


def test_t07_invalid_hour(api, records, tmp_path):
    records['hour'] = [0, 'bad', None, 'inf', '-inf', 12]
    result = api['load_data'](write(records, tmp_path))
    assert result[['hour_sin', 'hour_cos']].iloc[1:5].isna().all().all()
    assert np.isfinite(result[['hour_sin', 'hour_cos']].iloc[[0, 5]]).all().all()


def test_t08_preserve_fields(api, records, cleaned, tmp_path):
    for col in ['observation_id', TARGET, 'member_sessions', 'guest_sessions', 'export_note']:
        assert cleaned[col].tolist() == records[col].tolist()
    queued = api['load_data'](write(records.drop(columns=[TARGET]), tmp_path, 'queued.csv'))
    assert TARGET not in queued
    assert queued.observation_id.tolist() == records.observation_id.tolist()


def test_t09_pipeline(api):
    estimator = DecisionTreeRegressor()
    pipe = api['build_pipeline'](estimator)
    assert isinstance(pipe, Pipeline)
    assert pipe.steps[-1][1] is estimator
    with pytest.raises(NotFittedError):
        check_is_fitted(pipe)
    transformers = pipe.steps[0][1].transformers
    assert len(transformers) == 2
    assert any(list(cols) == NUM for _, _, cols in transformers)
    assert any(list(cols) == CAT for _, _, cols in transformers)


def test_t10_preprocessing(api, cleaned):
    X = cleaned[FEATURES].copy()
    X['temperature_c'] = [10, 20, np.nan, 40, 60, 100]
    pipe = api['build_pipeline'](DecisionTreeRegressor()).fit(X, cleaned[TARGET])
    num_step = next(transformer for _, transformer, cols in pipe.steps[0][1].transformers_ if list(cols) == NUM)
    assert num_step.steps[0][1].strategy == 'median'
    assert num_step.steps[0][1].statistics_[0] == 40
    assert num_step.steps[1][1].mean_[0] == 45
    np.testing.assert_allclose(num_step.transform(X[NUM]).mean(axis=0), 0, atol=1e-9)

    future = X.iloc[[0]].copy()
    future['temperature_c'] = 5000
    for col in CAT:
        future[col] = 'unseen'
    assert np.isfinite(pipe.predict(future)).all()
    assert num_step.steps[0][1].statistics_[0] == 40


def test_t11_supervised_contract(supervised):
    X_train, X_test, y_train, y_test = supervised
    assert isinstance(X_train, pd.DataFrame) and isinstance(X_test, pd.DataFrame)
    assert isinstance(y_train, pd.Series) and isinstance(y_test, pd.Series)
    assert list(X_train.columns) == FEATURES == list(X_test.columns)
    assert len(X_train) == len(y_train) and len(X_test) == len(y_test)


def test_t12_target_filter(api, records, tmp_path):
    first = records.copy()
    second = records.copy()
    first[TARGET] = ['0', 'bad', 'inf', None, -1, 6]
    second[TARGET] = [None, '12', '-inf', -2, 0, '6']
    X_train, X_test, y_train, y_test = api['prepare_datasets'](
        write(first, tmp_path, 'a.csv'),
        write(second, tmp_path, 'b.csv'),
    )
    assert y_train.tolist() == [0, 6]
    assert y_test.tolist() == [12, 0, 6]
    assert pd.api.types.is_numeric_dtype(y_train)
    assert pd.api.types.is_numeric_dtype(y_test)


def test_t13_alignment_no_leakage(api, records, tmp_path):
    candidate = records.copy()
    candidate.loc[1, TARGET] = -1
    candidate.loc[3, 'observation_date'] = 'bad'
    X_train, X_test, y_train, y_test = api['prepare_datasets'](
        write(candidate, tmp_path, 'a.csv'),
        write(records, tmp_path, 'b.csv'),
    )
    assert X_train.temperature_c.tolist() == [18, 33, 29, 25]
    assert y_train.tolist() == [4, 20, 0, 6]
    assert X_train.index.equals(y_train.index)
    assert X_test.index.equals(y_test.index)
    assert X_test.temperature_c.tolist() == records.temperature_c.tolist()
    assert list(X_train.columns) == FEATURES == list(X_test.columns)


def test_t14_models(fitted):
    assert set(fitted) == {'decision_tree', 'random_forest'}
    tree_model = fitted['decision_tree']
    forest_model = fitted['random_forest']
    assert tree_model is not forest_model
    assert tree_model.steps[0][1] is not forest_model.steps[0][1]
    assert isinstance(tree_model.steps[-1][1], DecisionTreeRegressor)
    assert isinstance(forest_model.steps[-1][1], RandomForestRegressor)

    for param, value in dict(max_depth=10, min_samples_leaf=4, random_state=42).items():
        assert tree_model.steps[-1][1].get_params()[param] == value

    for param, value in dict(n_estimators=120, max_depth=14, min_samples_leaf=2, random_state=42, n_jobs=-1).items():
        assert forest_model.steps[-1][1].get_params()[param] == value


def test_t15_fitted_predictions(fitted, supervised, monkeypatch):
    _, X_test, _, _ = supervised
    monkeypatch.setattr(Pipeline, 'fit', Mock(side_effect=AssertionError('Unexpected fit')))
    for model in fitted.values():
        check_is_fitted(model)
        sample = X_test.iloc[:8].copy()
        sample['weather_condition'] = 'unseen'
        pred = model.predict(sample)
        assert len(pred) == 8
        assert np.isfinite(pred).all()


def test_t16_metrics(api):
    X = pd.DataFrame({'x': [0, 1, 2]})
    y = pd.Series([0, 3, 10])
    model_a, model_b = Mock(), Mock()
    model_a.predict.return_value = np.array([-5, 2, 13])
    model_b.predict.return_value = np.array([2, -1, 9])
    result = api['evaluate_models']({'a': model_a, 'b': model_b}, X, y).set_index('model_name')
    for name, model in [('a', model_a), ('b', model_b)]:
        pred = np.maximum(model.predict.return_value, 0)
        np.testing.assert_allclose(
            result.loc[name, ['mae', 'rmse', 'rmsle']].astype(float),
            [mean_absolute_error(y, pred), np.sqrt(mean_squared_error(y, pred)), np.sqrt(mean_squared_log_error(y, pred))],
        )
        model.fit.assert_not_called()


def test_t17_rank_rmsle(api):
    X = pd.DataFrame({'x': [1, 2]})
    y = pd.Series([0, 100])
    model_a, model_b = Mock(), Mock()
    model_a.predict.return_value = np.array([2, 100])
    model_b.predict.return_value = np.array([0, 110])
    result = api['evaluate_models']({'a': model_a, 'b': model_b}, X, y)
    assert list(result.columns) == ['model_name', 'mae', 'rmse', 'rmsle']
    assert result.model_name.tolist() == ['b', 'a']
    assert list(result.index) == [0, 1]
    assert result.iloc[0].rmse > result.iloc[1].rmse
    for model in [model_a, model_b]:
        model.fit.assert_not_called()


def test_t18_selection(api):
    model_a, model_b = Mock(), Mock()
    comparison = pd.DataFrame({'model_name': ['b', 'a'], 'rmsle': [0.1, 0.8]})
    name, chosen = api['select_best_model'](comparison, {'a': model_a, 'b': model_b})
    assert name == 'b'
    assert chosen is model_b
    model_a.fit.assert_not_called()
    model_b.fit.assert_not_called()


def test_t19_prediction(api, cleaned):
    model = Mock()
    model.predict.return_value = np.array([-1.4, 2.36, 7.8, 0.0, 4.5, 5.5])
    result = api['predict_demand'](model, cleaned)
    assert list(result.columns) == ['observation_id', OUT]
    assert result.observation_id.tolist() == cleaned.observation_id.tolist()
    assert result[OUT].tolist() == [0, 2, 8, 0, 4, 6]
    assert pd.api.types.is_integer_dtype(result[OUT])
    pd.testing.assert_frame_equal(model.predict.call_args.args[0], cleaned[FEATURES])
    model.fit.assert_not_called()


def test_t20_workflows(tmp_path, monkeypatch):
    for split in ['train', 'test', 'predict']:
        shutil.copy(HERE / f'ev_{split}.csv', tmp_path)
    monkeypatch.chdir(tmp_path)
    workflow_api = load_notebook_definitions()
    assert not Path('best_model.pkl').exists()
    assert not Path('model_comparison.csv').exists()

    best_name, report = workflow_api['train']()
    saved = pd.read_csv('model_comparison.csv')
    pd.testing.assert_frame_equal(saved, report, check_exact=False)
    assert list(saved.columns) == ['model_name', 'mae', 'rmse', 'rmsle']
    assert saved.rmsle.is_monotonic_increasing
    assert best_name == saved.iloc[0].model_name

    model = joblib.load('best_model.pkl')
    check_is_fitted(model)
    assert isinstance(model, Pipeline)
    expected_estimator_type = DecisionTreeRegressor if best_name == 'decision_tree' else RandomForestRegressor
    assert isinstance(model.steps[-1][1], expected_estimator_type)

    fresh_api = load_notebook_definitions()
    expected_data = fresh_api['load_data']('ev_predict.csv')
    expected_values = np.rint(np.maximum(model.predict(expected_data[FEATURES]), 0)).astype(int)

    Path('ev_train.csv').unlink()
    Path('ev_test.csv').unlink()
    monkeypatch.setitem(fresh_api, 'train', Mock(side_effect=AssertionError('Unexpected training')))
    monkeypatch.setattr(Pipeline, 'fit', Mock(side_effect=AssertionError('Unexpected fit')))

    actual = fresh_api['predict']()
    saved_pred = pd.read_csv('ev_predictions.csv')
    pd.testing.assert_frame_equal(actual, saved_pred)
    assert list(saved_pred.columns) == ['observation_id', OUT]
    assert saved_pred.observation_id.tolist() == expected_data.observation_id.tolist()
    np.testing.assert_array_equal(saved_pred[OUT], expected_values)
