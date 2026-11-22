"""Exactly 20 independently graded checks (3 marks each = 60 marks)."""
import ast
import os
import shutil
from pathlib import Path

import joblib
import nbformat
import numpy as np
import pandas as pd
import pytest
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import LabelEncoder, FunctionTransformer
from sklearn.metrics import (
    f1_score, confusion_matrix, mean_absolute_error,
    mean_squared_error, r2_score, silhouette_score, davies_bouldin_score,
)

BASE = Path(__file__).resolve().parent
CASE = "b"


@pytest.fixture(scope="module")
def s():
    """Load imports, constants, classes and functions without running workflow calls."""
    env_notebook = os.environ.get("MS2_NOTEBOOK")
    candidates = [
        env_notebook,
        # "solution_with_code.ipynb",
        # "solution.ipynb",
        # "solution1.ipynb",
        "solution_p1.ipynb",
        "solution_p2.ipynb",
    ]
    candidates = [name for name in candidates if name]
    notebook_path = next((BASE / name for name in candidates if (BASE / name).is_file()), None)
    if notebook_path is None:
        raise FileNotFoundError(
            "No supported notebook found. Expected one of: " + ", ".join(candidates)
        )
    notebook_name = notebook_path.name
    notebook = nbformat.read(notebook_path, as_version=4)
    ns = {"__name__": "notebook_under_test"}

    allowed_nodes = (
        ast.Import, ast.ImportFrom, ast.Assign, ast.AnnAssign,
        ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef,
    )
    for cell in notebook.cells:
        if cell.cell_type != "code" or not cell.source.strip():
            continue
        tree = ast.parse(cell.source, filename=str(notebook_path))
        tree.body = [node for node in tree.body if isinstance(node, allowed_nodes)]
        if tree.body:
            ast.fix_missing_locations(tree)
            exec(compile(tree, str(notebook_path), "exec"), ns)
    return ns


def run_integration(s, tmp_path):
    patterns = {
        "a": ["shipment_train.csv", "shipment_test.csv", "shipment_predict.csv"],
        "b": ["ticket_train.csv", "ticket_test.csv", "ticket_predict.csv"],
        "c": ["water_train.csv", "water_test.csv", "water_predict.csv"],
        "d": ["retail_train.csv", "retail_test.csv", "retail_predict.csv"],
    }
    for name in patterns[CASE]:
        shutil.copy(BASE / name, tmp_path / name)
    old = os.getcwd()
    try:
        os.chdir(tmp_path)
        name, comparison = s["train"]()
        assert Path("best_model.pkl").is_file()
        assert Path("model_comparison.csv").is_file()
        result = s["predict"]()
        return name, comparison, result, Path(tmp_path)
    finally:
        os.chdir(old)


def test_T01_dedup(s, tmp_path):
    df = s["load_data"](str(BASE / "ticket_train.csv"))
    assert df["ticket_id"].is_unique


def test_T02_timestamp(s, tmp_path):
    df = s["load_data"](str(BASE / "ticket_train.csv"))
    assert pd.api.types.is_datetime64_any_dtype(df["opened_ts"])
    assert df["opened_ts"].notna().all()


def test_T03_infinity(s, tmp_path):
    df = s["load_data"](str(BASE / "ticket_train.csv"))
    assert not np.isinf(df[s["RAW_NUMERIC"]].to_numpy(dtype=float)).any()


def test_T04_numericstring(s, tmp_path):
    df = s["load_data"](str(BASE / "ticket_train.csv"))
    assert not df["customer_tier"].str.contains(r"\.0$", regex=True).any()


def test_T05_targetnormal(s, tmp_path):
    df = s["load_data"](str(BASE / "ticket_train.csv"))
    target = df["priority"].dropna()
    assert target.str.upper().eq(target).all()
    assert not target.str.contains(" ").any()


def test_T06_datetimefeatures(s, tmp_path):
    df = s["load_data"](str(BASE / "ticket_test.csv"))
    assert (df["opened_hour"] == df["opened_ts"].dt.hour).all()
    assert (df["opened_month"] == df["opened_ts"].dt.month).all()


def test_T07_safe_division(s, tmp_path):
    df = s["load_data"](str(BASE / "ticket_train.csv"))
    assert not np.isinf(df["backlog_per_agent"].dropna().to_numpy()).any()


def test_T08_features(s, tmp_path):
    assert len(s["FEATURES"]) == 11
    assert "ticket_id" not in s["FEATURES"]
    assert s["TARGET"] not in s["FEATURES"]


def test_T09_preprocessor(s, tmp_path):
    from sklearn.ensemble import RandomForestClassifier
    pipe = s["build_pipeline"](RandomForestClassifier())
    assert isinstance(pipe.named_steps["preprocessor"], ColumnTransformer)
    assert len(pipe.named_steps["preprocessor"].transformers) == 2


def test_T10_labelencode(s, tmp_path):
    prepared = s["prepare_datasets"](str(BASE / "ticket_train.csv"), str(BASE / "ticket_test.csv"))
    xtr, xte, ytr, yte = prepared[:4]
    encoder = prepared[4]
    assert isinstance(encoder, LabelEncoder)
    assert set(encoder.classes_) == set(s["CLASS_NAMES"])
    assert set(ytr.unique()) == {0, 1, 2}

def test_T11_invalidtargets(s, tmp_path):
    prepared = s["prepare_datasets"](str(BASE / "ticket_train.csv"), str(BASE / "ticket_test.csv"))
    xtr, xte, ytr, yte = prepared[:4]
    assert ytr.notna().all() and yte.notna().all()
    assert len(xtr) == len(ytr)

def test_T12_columnexclude(s, tmp_path):
    prepared = s["prepare_datasets"](str(BASE / "ticket_train.csv"), str(BASE / "ticket_test.csv"))
    xtr, xte, ytr, yte = prepared[:4]
    assert xtr.columns.tolist() == s["FEATURES"]
    assert "opened_ts" not in xtr

def test_T13_modelclasses(s, tmp_path):
    prepared = s["prepare_datasets"](str(BASE / "ticket_train.csv"), str(BASE / "ticket_test.csv"))
    xtr, xte, ytr, yte = prepared[:4]
    models = s["train_models"](xtr, ytr)
    assert set(models) == {"logistic_regression", "random_forest"}

def test_T14_fitted(s, tmp_path):
    prepared = s["prepare_datasets"](str(BASE / "ticket_train.csv"), str(BASE / "ticket_test.csv"))
    xtr, xte, ytr, yte = prepared[:4]
    models = s["train_models"](xtr, ytr)
    assert all(hasattr(p.named_steps["model"], "classes_") for p in models.values())

def test_T15_macro(s, tmp_path):
    prepared = s["prepare_datasets"](str(BASE / "ticket_train.csv"), str(BASE / "ticket_test.csv"))
    xtr, xte, ytr, yte = prepared[:4]
    models = s["train_models"](xtr, ytr)
    evaluated = s["evaluate_models"](models, xte, yte)
    comp, matrices = evaluated
    row = comp.iloc[0]
    p = models[row["model_name"]]
    y = p.predict(xte)
    assert np.isclose(row["macro_f1"], f1_score(yte, y, labels=[0, 1, 2], average="macro", zero_division=0))

def test_T16_weighted(s, tmp_path):
    prepared = s["prepare_datasets"](str(BASE / "ticket_train.csv"), str(BASE / "ticket_test.csv"))
    xtr, xte, ytr, yte = prepared[:4]
    models = s["train_models"](xtr, ytr)
    evaluated = s["evaluate_models"](models, xte, yte)
    comp, matrices = evaluated
    row = comp.iloc[0]
    p = models[row["model_name"]]
    y = p.predict(xte)
    assert np.isclose(row["weighted_f1"], f1_score(yte, y, labels=[0, 1, 2], average="weighted", zero_division=0))

def test_T17_confusion(s, tmp_path):
    prepared = s["prepare_datasets"](str(BASE / "ticket_train.csv"), str(BASE / "ticket_test.csv"))
    xtr, xte, ytr, yte = prepared[:4]
    models = s["train_models"](xtr, ytr)
    evaluated = s["evaluate_models"](models, xte, yte)
    comp, matrices = evaluated
    best = s["select_best_model"](comp, models)
    cm = matrices[best[0]]
    assert cm.shape == (3, 3)
    assert cm.sum() == len(yte)

def test_T18_sortbest(s, tmp_path):
    prepared = s["prepare_datasets"](str(BASE / "ticket_train.csv"), str(BASE / "ticket_test.csv"))
    xtr, xte, ytr, yte = prepared[:4]
    models = s["train_models"](xtr, ytr)
    evaluated = s["evaluate_models"](models, xte, yte)
    comp, matrices = evaluated
    best = s["select_best_model"](comp, models)
    assert comp["macro_f1"].is_monotonic_decreasing
    assert best[1] is models[best[0]]

def test_T19_inverse(s, tmp_path):
    prepared = s["prepare_datasets"](str(BASE / "ticket_train.csv"), str(BASE / "ticket_test.csv"))
    xtr, xte, ytr, yte = prepared[:4]
    models = s["train_models"](xtr, ytr)
    evaluated = s["evaluate_models"](models, xte, yte)
    comp, matrices = evaluated
    best = s["select_best_model"](comp, models)
    encoder = prepared[4]
    df = s["load_data"](str(BASE / "ticket_predict.csv"))
    r = s["predict_priority"](best[1], encoder, df)
    assert r.columns.tolist() == ["ticket_id", "predicted_priority", "confidence", "high_probability"]
    assert set(r["predicted_priority"]).issubset(set(s["CLASS_NAMES"]))
    assert r["high_probability"].between(0, 1).all()

def test_T20_integration(s, tmp_path):
    name, comp, result, path = run_integration(s, tmp_path)
    assert (path / "confusion_matrix.csv").exists()
    assert (path / "ticket_predictions.csv").exists()
    assert len(result) > 0
