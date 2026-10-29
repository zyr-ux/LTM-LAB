import pandas as pd
import pytest

from main import (
    load_service_invoices,
    clean_service_invoices,
    merge_with_service_centres,
    add_net_invoice_value,
    aggregate_by_service_type,
    finalize_summary
)


def test_load_service_invoices(tmp_path):
    file_path = tmp_path / "service_invoices.csv"

    pd.DataFrame({
        "invoice_id": [6101],
        "centre_id": [401],
        "customer_name": ["Nora Shah"],
        "customer_email": ["nora@example.com"],
        "labour_hours": [2],
        "hourly_rate": [900],
        "parts_charge": [500],
        "discount_pct": [10],
        "invoice_date": ["2026-10-11"]
    }).to_csv(file_path, index=False)

    result = load_service_invoices(file_path)

    assert list(result.columns) == [
        "invoice_id",
        "centre_id",
        "customer_name",
        "customer_email",
        "labour_hours",
        "hourly_rate",
        "parts_charge",
        "discount_pct"
    ]

    assert len(result) == 1
    assert "invoice_date" not in result.columns


def test_clean_service_invoices():
    df = pd.DataFrame({
        "invoice_id": [6101, 6102, 6102, 6103],
        "centre_id": [401, 402, 402, 403],
        "customer_name": [
            "Nora",
            "Arun",
            "Arun Duplicate",
            "Leah"
        ],
        "customer_email": [
            "nora@example.com",
            "arun@example.com",
            "arun2@example.com",
            None
        ],
        "labour_hours": [2, 1, 4, 3],
        "hourly_rate": [900, 1200, 1200, 750],
        "parts_charge": [500, 800, 900, 300],
        "discount_pct": [10, 0, 0, 5]
    })

    result = clean_service_invoices(df)

    assert list(result["invoice_id"]) == [6101, 6102]
    assert result["customer_email"].isna().sum() == 0

    # First 6102 must be retained
    row = result[result["invoice_id"] == 6102].iloc[0]
    assert row["customer_name"] == "Arun"


def test_merge_with_service_centres(tmp_path):
    df = pd.DataFrame({
        "invoice_id": [6101, 6106],
        "centre_id": [401, 999],
        "customer_name": ["Nora", "Zara"],
        "customer_email": ["nora@example.com", "zara@example.com"],
        "labour_hours": [2, 1],
        "hourly_rate": [900, 500],
        "parts_charge": [500, 100],
        "discount_pct": [10, 0]
    })

    ref_path = tmp_path / "service_centres.csv"

    pd.DataFrame({
        "centre_id": [401],
        "service_type": ["General Service"],
        "region": ["North"],
        "centre_name": ["North Auto"]
    }).to_csv(ref_path, index=False)

    result = merge_with_service_centres(df, ref_path)

    # centre_id 999 should be removed by the inner join
    assert len(result) == 1
    assert result.iloc[0]["invoice_id"] == 6101

    assert list(result.columns) == [
        "invoice_id",
        "centre_id",
        "customer_name",
        "customer_email",
        "labour_hours",
        "hourly_rate",
        "parts_charge",
        "discount_pct",
        "service_type",
        "region",
        "centre_name"
    ]


def test_add_net_invoice_value():
    df = pd.DataFrame({
        "labour_hours": [2, 1],
        "hourly_rate": [900, 1200],
        "parts_charge": [500, 800],
        "discount_pct": [10, 0]
    })

    result = add_net_invoice_value(df)

    assert "net_invoice_value" in result.columns

    # (2 * 900 + 500) * 0.90 = 2070
    assert result.loc[0, "net_invoice_value"] == pytest.approx(2070.00)

    # (1 * 1200 + 800) * 1 = 2000
    assert result.loc[1, "net_invoice_value"] == pytest.approx(2000.00)


def test_aggregate_by_service_type():
    df = pd.DataFrame({
        "invoice_id": [6101, 6104, 6102],
        "service_type": [
            "General Service",
            "General Service",
            "Engine Repair"
        ],
        "net_invoice_value": [2070.00, 1150.00, 2000.00]
    })

    result = aggregate_by_service_type(df)

    assert list(result.columns) == [
        "service_type",
        "avg_net_invoice_value",
        "total_net_invoice_value",
        "valid_invoice_count"
    ]

    general = result[result["service_type"] == "General Service"].iloc[0]

    assert general["avg_net_invoice_value"] == pytest.approx(1610.00)
    assert general["total_net_invoice_value"] == pytest.approx(3220.00)
    assert general["valid_invoice_count"] == 2


def test_finalize_summary():
    df = pd.DataFrame({
        "service_type": [
            "Wheel Alignment",
            "General Service",
            "Engine Repair"
        ],
        "avg_net_invoice_value": [2437.50, 1610, 2000],
        "total_net_invoice_value": [2437.50, 3220, 2000],
        "valid_invoice_count": [1, 2, 1]
    })

    result = finalize_summary(df)

    assert list(result.columns) == [
        "service_type",
        "avg_net_invoice_value",
        "total_net_invoice_value",
        "valid_invoice_count"
    ]

    assert list(result["service_type"]) == [
        "Engine Repair",
        "General Service",
        "Wheel Alignment"
    ]

    assert list(result.index) == [0, 1, 2]


def test_finalize_summary_empty():
    df = pd.DataFrame(columns=[
        "service_type",
        "avg_net_invoice_value",
        "total_net_invoice_value",
        "valid_invoice_count"
    ])

    result = finalize_summary(df)

    assert result.empty

    assert list(result.columns) == [
        "service_type",
        "avg_net_invoice_value",
        "total_net_invoice_value",
        "valid_invoice_count"
    ]