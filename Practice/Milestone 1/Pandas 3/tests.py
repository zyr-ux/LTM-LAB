import pandas as pd
import pytest

from main import (
    load_ticket_sales,
    clean_ticket_sales,
    merge_with_events,
    add_net_ticket_value,
    aggregate_by_category,
    finalize_summary
)


def test_load_ticket_sales(tmp_path):
    file_path = tmp_path / "ticket_sales.csv"

    pd.DataFrame({
        "sale_id": [5001],
        "event_id": [301],
        "buyer_name": ["Asha Rao"],
        "buyer_email": ["asha@example.com"],
        "tickets": [2],
        "ticket_price": [1500],
        "discount_pct": [10],
        "sale_date": ["2026-10-01"]
    }).to_csv(file_path, index=False)

    result = load_ticket_sales(file_path)

    assert list(result.columns) == [
        "sale_id",
        "event_id",
        "buyer_name",
        "buyer_email",
        "tickets",
        "ticket_price",
        "discount_pct"
    ]

    assert len(result) == 1
    assert "sale_date" not in result.columns


def test_clean_ticket_sales():
    df = pd.DataFrame({
        "sale_id": [5001, 5002, 5002, 5003],
        "event_id": [301, 302, 302, 303],
        "buyer_name": ["Asha", "Ravi", "Ravi Duplicate", "Mina"],
        "buyer_email": [
            "asha@example.com",
            "ravi@example.com",
            "ravi2@example.com",
            None
        ],
        "tickets": [2, 1, 4, 3],
        "ticket_price": [1500, 2200, 2200, 900],
        "discount_pct": [10, 0, 0, 5]
    })

    result = clean_ticket_sales(df)

    assert list(result["sale_id"]) == [5001, 5002]
    assert result["buyer_email"].isna().sum() == 0

    # First 5002 must be retained
    row = result[result["sale_id"] == 5002].iloc[0]
    assert row["buyer_name"] == "Ravi"


def test_merge_with_events(tmp_path):
    requests_df = pd.DataFrame({
        "sale_id": [5001, 5006],
        "event_id": [301, 999],
        "buyer_name": ["Asha", "Neel"],
        "buyer_email": ["asha@example.com", "neel@example.com"],
        "tickets": [2, 1],
        "ticket_price": [1500, 700],
        "discount_pct": [10, 0]
    })

    ref_path = tmp_path / "events.csv"

    pd.DataFrame({
        "event_id": [301],
        "event_name": ["Jazz Evening"],
        "category": ["Music"],
        "venue": ["Hall A"]
    }).to_csv(ref_path, index=False)

    result = merge_with_events(requests_df, ref_path)

    # event_id 999 should disappear because this is an inner join
    assert len(result) == 1
    assert result.iloc[0]["sale_id"] == 5001

    assert list(result.columns) == [
        "sale_id",
        "event_id",
        "buyer_name",
        "buyer_email",
        "tickets",
        "ticket_price",
        "discount_pct",
        "event_name",
        "category",
        "venue"
    ]


def test_add_net_ticket_value():
    df = pd.DataFrame({
        "tickets": [2, 3],
        "ticket_price": [1500, 900],
        "discount_pct": [10, 5]
    })

    result = add_net_ticket_value(df)

    assert "net_ticket_value" in result.columns
    assert result.loc[0, "net_ticket_value"] == pytest.approx(2700.00)
    assert result.loc[1, "net_ticket_value"] == pytest.approx(2565.00)


def test_aggregate_by_category():
    df = pd.DataFrame({
        "sale_id": [5001, 5004, 5002],
        "category": ["Music", "Music", "Technology"],
        "net_ticket_value": [2700.00, 1500.00, 2200.00]
    })

    result = aggregate_by_category(df)

    assert list(result.columns) == [
        "category",
        "avg_net_ticket_value",
        "total_net_ticket_revenue",
        "valid_sale_count"
    ]

    music = result[result["category"] == "Music"].iloc[0]

    assert music["avg_net_ticket_value"] == pytest.approx(2100.00)
    assert music["total_net_ticket_revenue"] == pytest.approx(4200.00)
    assert music["valid_sale_count"] == 2


def test_finalize_summary():
    df = pd.DataFrame({
        "category": ["Technology", "Music", "Lifestyle"],
        "avg_net_ticket_value": [2200, 2100, 2565],
        "total_net_ticket_revenue": [2200, 4200, 2565],
        "valid_sale_count": [1, 2, 1]
    })

    result = finalize_summary(df)

    assert list(result.columns) == [
        "category",
        "avg_net_ticket_value",
        "total_net_ticket_revenue",
        "valid_sale_count"
    ]

    assert list(result["category"]) == [
        "Lifestyle",
        "Music",
        "Technology"
    ]

    assert list(result.index) == [0, 1, 2]


def test_finalize_summary_empty():
    df = pd.DataFrame(columns=[
        "category",
        "avg_net_ticket_value",
        "total_net_ticket_revenue",
        "valid_sale_count"
    ])

    result = finalize_summary(df)

    assert result.empty

    assert list(result.columns) == [
        "category",
        "avg_net_ticket_value",
        "total_net_ticket_revenue",
        "valid_sale_count"
    ]