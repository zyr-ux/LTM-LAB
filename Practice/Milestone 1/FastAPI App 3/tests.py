import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import models
import main


# A fresh in-memory SQLite database is created for every test.
@pytest.fixture()
def client():
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine,
    )

    models.Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    main.app.dependency_overrides[main.get_db] = override_get_db

    with TestClient(main.app) as test_client:
        yield test_client

    main.app.dependency_overrides.clear()
    models.Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()


def create_branch(client, name="Central Fitness", city="Bhubaneswar"):
    response = client.post(
        "/branches",
        json={"name": name, "city": city},
    )
    assert response.status_code == 201
    return response.json()


def create_plan(
    client,
    branch_id,
    name="Monthly Flex",
    duration_months=1,
    monthly_fee=900,
    guest_passes=1,
):
    response = client.post(
        f"/branches/{branch_id}/membership_plans",
        json={
            "name": name,
            "duration_months": duration_months,
            "monthly_fee": monthly_fee,
            "guest_passes": guest_passes,
        },
    )
    assert response.status_code == 201
    return response.json()


# -----------------------------------------------------------------------------
# POST /branches
# -----------------------------------------------------------------------------

def test_create_branch_success(client):
    response = client.post(
        "/branches",
        json={"name": "Central Fitness", "city": "Bhubaneswar"},
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "name": "Central Fitness",
        "city": "Bhubaneswar",
    }


@pytest.mark.parametrize("field,bad_value", [
    ("name", ""),
    ("name", "   "),
    ("city", ""),
    ("city", "\t  \n"),
])
def test_create_branch_rejects_empty_or_whitespace_strings(client, field, bad_value):
    body = {"name": "Central Fitness", "city": "Bhubaneswar"}
    body[field] = bad_value

    response = client.post("/branches", json=body)

    assert response.status_code == 422


@pytest.mark.parametrize("missing_field", ["name", "city"])
def test_create_branch_rejects_missing_fields(client, missing_field):
    body = {"name": "Central Fitness", "city": "Bhubaneswar"}
    body.pop(missing_field)

    response = client.post("/branches", json=body)

    assert response.status_code == 422


# -----------------------------------------------------------------------------
# POST /branches/{parent_id}/membership_plans
# -----------------------------------------------------------------------------

def test_create_membership_plan_success_and_omits_branch_id(client):
    branch = create_branch(client)

    response = client.post(
        f"/branches/{branch['id']}/membership_plans",
        json={
            "name": "Monthly Flex",
            "duration_months": 1,
            "monthly_fee": 900,
            "guest_passes": 1,
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "name": "Monthly Flex",
        "duration_months": 1,
        "monthly_fee": 900,
        "guest_passes": 1,
    }
    assert "branch_id" not in response.json()


def test_create_plan_returns_404_when_branch_does_not_exist(client):
    response = client.post(
        "/branches/999/membership_plans",
        json={
            "name": "Monthly Flex",
            "duration_months": 1,
            "monthly_fee": 900,
            "guest_passes": 1,
        },
    )

    assert response.status_code == 404


@pytest.mark.parametrize("field,bad_value", [
    ("name", ""),
    ("name", "   "),
    ("duration_months", 0),
    ("monthly_fee", 299),
    ("guest_passes", -1),
])
def test_create_plan_rejects_invalid_values(client, field, bad_value):
    branch = create_branch(client)
    body = {
        "name": "Monthly Flex",
        "duration_months": 1,
        "monthly_fee": 900,
        "guest_passes": 1,
    }
    body[field] = bad_value

    response = client.post(
        f"/branches/{branch['id']}/membership_plans",
        json=body,
    )

    assert response.status_code == 422


@pytest.mark.parametrize("missing_field", [
    "name",
    "duration_months",
    "monthly_fee",
    "guest_passes",
])
def test_create_plan_rejects_missing_fields(client, missing_field):
    branch = create_branch(client)
    body = {
        "name": "Monthly Flex",
        "duration_months": 1,
        "monthly_fee": 900,
        "guest_passes": 1,
    }
    body.pop(missing_field)

    response = client.post(
        f"/branches/{branch['id']}/membership_plans",
        json=body,
    )

    assert response.status_code == 422


@pytest.mark.parametrize("field,bad_value", [
    ("duration_months", True),
    ("duration_months", "1"),
    ("monthly_fee", False),
    ("monthly_fee", "900"),
    ("guest_passes", True),
    ("guest_passes", "1"),
])
def test_create_plan_uses_strict_integer_validation(client, field, bad_value):
    branch = create_branch(client)
    body = {
        "name": "Monthly Flex",
        "duration_months": 1,
        "monthly_fee": 900,
        "guest_passes": 1,
    }
    body[field] = bad_value

    response = client.post(
        f"/branches/{branch['id']}/membership_plans",
        json=body,
    )

    assert response.status_code == 422


# -----------------------------------------------------------------------------
# GET /branches/{parent_id}
# -----------------------------------------------------------------------------

def test_get_branch_with_plans_default_order_is_id_ascending(client):
    branch = create_branch(client)
    first = create_plan(client, branch["id"], "Zeta", 12, 500, 0)
    second = create_plan(client, branch["id"], "Alpha", 1, 900, 1)

    response = client.get(f"/branches/{branch['id']}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == branch["id"]
    assert data["name"] == "Central Fitness"
    assert data["city"] == "Bhubaneswar"
    assert [plan["id"] for plan in data["membership_plans"]] == [
        first["id"],
        second["id"],
    ]


def test_get_branch_with_zero_plans_returns_empty_list(client):
    branch = create_branch(client)

    response = client.get(f"/branches/{branch['id']}")

    assert response.status_code == 200
    assert response.json()["membership_plans"] == []


def test_get_branch_returns_404_when_branch_does_not_exist(client):
    response = client.get("/branches/999")

    assert response.status_code == 404


def test_get_branch_filters_duration_months_by_exact_match(client):
    branch = create_branch(client)
    create_plan(client, branch["id"], "Monthly", 1, 900, 1)
    create_plan(client, branch["id"], "Annual", 12, 500, 2)
    create_plan(client, branch["id"], "Another Monthly", 1, 700, 0)

    response = client.get(
        f"/branches/{branch['id']}",
        params={"duration_months": "1"},
    )

    assert response.status_code == 200
    plans = response.json()["membership_plans"]
    assert len(plans) == 2
    assert all(plan["duration_months"] == 1 for plan in plans)


@pytest.mark.parametrize("blank_value", ["", "   "])
def test_blank_duration_filter_is_treated_as_no_filter(client, blank_value):
    branch = create_branch(client)
    create_plan(client, branch["id"], "Monthly", 1, 900, 1)
    create_plan(client, branch["id"], "Annual", 12, 500, 2)

    response = client.get(
        f"/branches/{branch['id']}",
        params={"duration_months": blank_value},
    )

    assert response.status_code == 200
    assert len(response.json()["membership_plans"]) == 2


def test_get_branch_sorts_by_name_ascending_with_id_tie_breaker(client):
    branch = create_branch(client)
    first_alpha = create_plan(client, branch["id"], "Alpha", 1, 800, 0)
    create_plan(client, branch["id"], "Zeta", 3, 500, 0)
    second_alpha = create_plan(client, branch["id"], "Alpha", 6, 700, 1)

    response = client.get(
        f"/branches/{branch['id']}",
        params={"sort": "name"},
    )

    assert response.status_code == 200
    plans = response.json()["membership_plans"]
    assert [(plan["name"], plan["id"]) for plan in plans] == [
        ("Alpha", first_alpha["id"]),
        ("Alpha", second_alpha["id"]),
        ("Zeta", 2),
    ]


def test_get_branch_sorts_by_monthly_fee_with_id_tie_breaker(client):
    branch = create_branch(client)
    first_500 = create_plan(client, branch["id"], "Plan B", 1, 500, 0)
    create_plan(client, branch["id"], "Plan C", 3, 900, 0)
    second_500 = create_plan(client, branch["id"], "Plan A", 6, 500, 1)

    response = client.get(
        f"/branches/{branch['id']}",
        params={"sort": "monthly_fee"},
    )

    assert response.status_code == 200
    plans = response.json()["membership_plans"]
    assert [(plan["monthly_fee"], plan["id"]) for plan in plans] == [
        (500, first_500["id"]),
        (500, second_500["id"]),
        (900, 2),
    ]


def test_get_branch_can_filter_and_sort_together(client):
    branch = create_branch(client)
    create_plan(client, branch["id"], "Expensive Monthly", 1, 900, 0)
    create_plan(client, branch["id"], "Annual", 12, 500, 0)
    create_plan(client, branch["id"], "Cheap Monthly", 1, 400, 1)

    response = client.get(
        f"/branches/{branch['id']}",
        params={"duration_months": "1", "sort": "monthly_fee"},
    )

    assert response.status_code == 200
    plans = response.json()["membership_plans"]
    assert [plan["monthly_fee"] for plan in plans] == [400, 900]
    assert all(plan["duration_months"] == 1 for plan in plans)


@pytest.mark.parametrize("bad_sort", ["id", "duration_months", "NAME", "invalid"])
def test_get_branch_rejects_unsupported_sort(client, bad_sort):
    branch = create_branch(client)

    response = client.get(
        f"/branches/{branch['id']}",
        params={"sort": bad_sort},
    )

    assert response.status_code == 404


# -----------------------------------------------------------------------------
# PUT /branches/{parent_id}/membership_plans/{child_id}
# -----------------------------------------------------------------------------

def test_update_membership_plan_successfully_replaces_all_fields(client):
    branch = create_branch(client)
    plan = create_plan(client, branch["id"])

    response = client.put(
        f"/branches/{branch['id']}/membership_plans/{plan['id']}",
        json={
            "name": "Annual Premium",
            "duration_months": 12,
            "monthly_fee": 1200,
            "guest_passes": 5,
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": plan["id"],
        "name": "Annual Premium",
        "duration_months": 12,
        "monthly_fee": 1200,
        "guest_passes": 5,
    }
    assert "branch_id" not in response.json()


def test_update_returns_404_when_branch_does_not_exist(client):
    response = client.put(
        "/branches/999/membership_plans/1",
        json={
            "name": "Annual Premium",
            "duration_months": 12,
            "monthly_fee": 1200,
            "guest_passes": 5,
        },
    )

    assert response.status_code == 404


def test_update_returns_404_when_plan_does_not_exist(client):
    branch = create_branch(client)

    response = client.put(
        f"/branches/{branch['id']}/membership_plans/999",
        json={
            "name": "Annual Premium",
            "duration_months": 12,
            "monthly_fee": 1200,
            "guest_passes": 5,
        },
    )

    assert response.status_code == 404


def test_update_returns_404_when_plan_belongs_to_another_branch(client):
    first_branch = create_branch(client, "First Gym", "Pune")
    second_branch = create_branch(client, "Second Gym", "Mumbai")
    plan = create_plan(client, first_branch["id"])

    response = client.put(
        f"/branches/{second_branch['id']}/membership_plans/{plan['id']}",
        json={
            "name": "Moved Plan",
            "duration_months": 6,
            "monthly_fee": 700,
            "guest_passes": 2,
        },
    )

    assert response.status_code == 404

    original_branch_response = client.get(f"/branches/{first_branch['id']}")
    assert original_branch_response.status_code == 200
    plans = original_branch_response.json()["membership_plans"]
    assert len(plans) == 1
    assert plans[0]["id"] == plan["id"]
    assert plans[0]["name"] == "Monthly Flex"


@pytest.mark.parametrize("missing_field", [
    "name",
    "duration_months",
    "monthly_fee",
    "guest_passes",
])
def test_update_is_full_update_and_rejects_missing_fields(client, missing_field):
    branch = create_branch(client)
    plan = create_plan(client, branch["id"])
    body = {
        "name": "Annual Premium",
        "duration_months": 12,
        "monthly_fee": 1200,
        "guest_passes": 5,
    }
    body.pop(missing_field)

    response = client.put(
        f"/branches/{branch['id']}/membership_plans/{plan['id']}",
        json=body,
    )

    assert response.status_code == 422


@pytest.mark.parametrize("field,bad_value", [
    ("name", "   "),
    ("duration_months", 0),
    ("duration_months", True),
    ("duration_months", "12"),
    ("monthly_fee", 299),
    ("monthly_fee", False),
    ("monthly_fee", "1200"),
    ("guest_passes", -1),
    ("guest_passes", True),
    ("guest_passes", "5"),
])
def test_update_rejects_invalid_or_non_strict_values(client, field, bad_value):
    branch = create_branch(client)
    plan = create_plan(client, branch["id"])
    body = {
        "name": "Annual Premium",
        "duration_months": 12,
        "monthly_fee": 1200,
        "guest_passes": 5,
    }
    body[field] = bad_value

    response = client.put(
        f"/branches/{branch['id']}/membership_plans/{plan['id']}",
        json=body,
    )

    assert response.status_code == 422
