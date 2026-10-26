from datetime import date, timedelta
from decimal import Decimal

import pytest

from app.api.portfolios import calculations as calc


def customer_payload(refs, name="PT Bank Mandiri"):
    return {
        "customer_name": name,
        "company_size_id": str(refs["company_size"]["TIER_1"]),
        "annual_revenue": "115T (FY 2025)",
        "customer_type_id": str(refs["customer_type"]["STRATEGIC_CUSTOMER"]),
        "industry_id": str(refs["industry"]["GOVERNMENT"]),
        "location": "Jakarta",
        "legal_structure_id": str(refs["legal_structure"]["STATE_OWNED_ENTERPRISE"]),
    }


def portfolio_payload(refs, *, customer=None, customer_id=None, code="ITMS_MON_BMRI_2026_PRO",
                      status="ON_GOING", value="1000000", start=None, end=None, year=2026, **extra):
    today = date.today()
    start = start or today - timedelta(days=100)
    end = end or today + timedelta(days=100)
    body = {
        "project": {
            "project_code": code,
            "project_name": f"Project {code}",
            "project_year": year,
            "business_unit_id": str(refs["business_unit"]["ITMS"]),
            "project_status_id": str(refs["status"][status]),
            "value_before_tax": value,
            "project_manager": "Budi",
            "account_manager": "Sari",
            "start_date": start.isoformat(),
            "end_date": end.isoformat(),
        },
        "financial": {"cogs": "200000", "operational_costs": "100000"},
        "product_ids": refs["products"][:1],
        "tech_stack_ids": [refs["tech"]["frontend"], refs["tech"]["backend"]],
        "partners": [
            {"partner_id": refs["partners"]["principal"], "partner_role": "Principal"},
            {"partner_id": refs["partners"]["vendor"], "partner_role": "Vendor"},
        ],
    }
    if customer_id:
        body["customer_id"] = customer_id
    else:
        body["customer"] = customer or customer_payload(refs)
    body.update(extra)
    return body


async def create(client, headers, body):
    response = await client.post("/api/v1/portfolios", json=body, headers=headers)
    return response


# ───────────────────────── calculations (pure) ─────────────────────────
def test_metrics_follow_excel_formulas():
    metrics = calc.project_metrics(
        value_before_tax=Decimal("1000"), start_date=date(2026, 1, 1), end_date=date(2026, 1, 11),
        status_code="ON_GOING", today=date(2026, 1, 6), vat_rate=Decimal("0.11"),
    )
    assert metrics.value_after_tax == Decimal("1110.00")
    assert metrics.total_days == 10
    assert metrics.remaining_days == 5
    assert metrics.progress_percent == 50.0
    assert metrics.is_overdue is False


def test_metrics_overdue_and_clamped():
    metrics = calc.project_metrics(
        value_before_tax=Decimal("1"), start_date=date(2026, 1, 1), end_date=date(2026, 1, 11),
        status_code="ON_GOING", today=date(2026, 3, 1), vat_rate=Decimal("0.11"),
    )
    assert metrics.remaining_days == 0 and metrics.progress_percent == 100.0 and metrics.is_overdue
    closed = calc.project_metrics(
        value_before_tax=Decimal("1"), start_date=date(2026, 1, 1), end_date=date(2026, 1, 11),
        status_code="CLOSED", today=date(2026, 3, 1), vat_rate=Decimal("0.11"),
    )
    assert closed.is_overdue is False


def test_net_profit_and_margin():
    assert calc.net_profit(Decimal("100"), Decimal("30"), Decimal("20")) == Decimal("50")
    assert calc.net_margin_percent(Decimal("0"), Decimal("0")) is None


# ───────────────────────── permissions ─────────────────────────
async def test_requires_auth(client):
    assert (await client.get("/api/v1/portfolios")).status_code in (401, 403)


async def test_user_without_role_forbidden(client, no_role):
    assert (await client.get("/api/v1/portfolios", headers=no_role)).status_code == 403


async def test_viewer_can_read_but_not_write(client, viewer, admin, refs):
    created = await create(client, admin, portfolio_payload(refs))
    assert created.status_code == 201, created.text
    assert (await client.get("/api/v1/portfolios", headers=viewer)).status_code == 200
    assert (await create(client, viewer, portfolio_payload(refs, code="X1"))).status_code == 403
    pid = created.json()["data"]["id"]
    assert (await client.delete(f"/api/v1/portfolios/{pid}", headers=viewer)).status_code == 403
    assert (await client.post("/api/v1/customers", json=customer_payload(refs, "Z"), headers=viewer)).status_code == 403


# ───────────────────────── create / read ─────────────────────────
async def test_create_returns_all_five_perspectives(client, admin, refs):
    response = await create(client, admin, portfolio_payload(refs))
    assert response.status_code == 201, response.text
    data = response.json()["data"]

    assert data["customer"]["customer_name"] == "PT Bank Mandiri"
    assert data["project"]["project_code"] == "ITMS_MON_BMRI_2026_PRO"
    assert Decimal(data["project"]["value_after_tax"]) == Decimal("1110000.00")
    assert data["project"]["total_days"] == 200
    assert data["project"]["remaining_days"] == 100
    assert data["project"]["progress_percent"] == 50.0
    # revenue kosong -> default value_before_tax; profit = 1.000.000 - 200.000 - 100.000
    assert Decimal(data["financial"]["revenue"]) == Decimal("1000000")
    assert Decimal(data["financial"]["net_profit"]) == Decimal("700000")
    assert len(data["tech_stack"]["products"]) == 1
    assert len(data["tech_stack"]["frontend"]) == 1 and len(data["tech_stack"]["backend"]) == 1
    assert [p["partner_role"] for p in data["partners"]] == ["Principal", "Vendor"]

    detail = await client.get(f"/api/v1/portfolios/{data['id']}", headers=admin)
    assert detail.status_code == 200 and detail.json()["data"]["id"] == data["id"]


async def test_duplicate_project_code_conflict_case_insensitive(client, admin, refs):
    assert (await create(client, admin, portfolio_payload(refs, code="DUP_1"))).status_code == 201
    response = await create(client, admin, portfolio_payload(refs, code="dup_1", customer=customer_payload(refs, "Other")))
    assert response.status_code == 409


async def test_inline_customer_not_created_when_project_invalid(client, admin, refs):
    body = portfolio_payload(refs, code="A1")
    body["project"]["business_unit_id"] = "00000000-0000-0000-0000-000000000000"
    response = await create(client, admin, body)
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "INVALID_REFERENCE"
    assert (await client.get("/api/v1/customers", headers=admin)).json()["meta"]["total"] == 0


async def test_validation_errors(client, admin, refs):
    body = portfolio_payload(refs, code="B1")
    body["project"]["end_date"] = "2000-01-01"
    assert (await create(client, admin, body)).status_code == 422
    body = portfolio_payload(refs, code="bad code!")
    assert (await create(client, admin, body)).status_code == 422
    body = portfolio_payload(refs, code="B2", value="-5")
    assert (await create(client, admin, body)).status_code == 422
    body = portfolio_payload(refs, code="B3")
    body["customer_id"] = "00000000-0000-0000-0000-000000000000"
    assert (await create(client, admin, body)).status_code == 422  # keduanya diisi


async def test_get_unknown_returns_404(client, admin):
    assert (await client.get("/api/v1/portfolios/00000000-0000-0000-0000-000000000000", headers=admin)).status_code == 404


# ───────────────────────── list / filter / sort ─────────────────────────
@pytest.fixture
async def seeded(client, admin, refs):
    mandiri = await client.post("/api/v1/customers", json=customer_payload(refs), headers=admin)
    telkom_body = customer_payload(refs, "PT Telkomsel")
    telkom_body["industry_id"] = str(refs["industry"].get("TELECOMMUNICATION") or next(iter(refs["industry"].values())))
    telkom_body["customer_type_id"] = str(refs["customer_type"]["REGULAR_CUSTOMER"])
    telkom = await client.post("/api/v1/customers", json=telkom_body, headers=admin)
    m, t = mandiri.json()["data"]["id"], telkom.json()["data"]["id"]
    today = date.today()
    await create(client, admin, portfolio_payload(refs, customer_id=m, code="P_MANDIRI_1", value="3000"))
    await create(client, admin, portfolio_payload(refs, customer_id=m, code="P_MANDIRI_2", status="CLOSED", value="1000",
                                                  start=today - timedelta(days=400), end=today - timedelta(days=30), year=2025))
    await create(client, admin, portfolio_payload(refs, customer_id=t, code="P_TELKOM_1", value="2000",
                                                  end=today + timedelta(days=20)))
    return {"mandiri": m, "telkom": t}


async def test_filter_by_customer_name_and_id(client, admin, seeded):
    by_name = await client.get("/api/v1/portfolios", params={"customer_name": "mandiri"}, headers=admin)
    assert by_name.json()["meta"]["total"] == 2
    by_id = await client.get(f"/api/v1/customers/{seeded['telkom']}/portfolios", headers=admin)
    assert [r["project_code"] for r in by_id.json()["data"]] == ["P_TELKOM_1"]


async def test_filters_status_year_search_and_percent_escape(client, admin, seeded, refs):
    get = lambda **p: client.get("/api/v1/portfolios", params=p, headers=admin)  # noqa: E731
    assert (await get(project_status_id=str(refs["status"]["CLOSED"]))).json()["meta"]["total"] == 1
    assert (await get(active_only="true")).json()["meta"]["total"] == 2
    assert (await get(year=2025)).json()["meta"]["total"] == 1
    assert (await get(search="telkom")).json()["meta"]["total"] == 1
    assert (await get(search="%")).json()["meta"]["total"] == 0  # % bukan wildcard
    assert (await get(project_manager="bud")).json()["meta"]["total"] == 3
    assert (await get(partner_id=refs["partners"]["principal"])).json()["meta"]["total"] == 3
    assert (await get(tech_stack_id=refs["tech"]["frontend"])).json()["meta"]["total"] == 3
    assert (await get(product_id=refs["products"][0])).json()["meta"]["total"] == 3


async def test_sort_and_pagination(client, admin, seeded):
    response = await client.get(
        "/api/v1/portfolios",
        params={"sort_by": "value_before_tax", "sort_order": "desc", "page_size": 2, "page": 1},
        headers=admin,
    )
    body = response.json()
    assert [r["project_code"] for r in body["data"]] == ["P_MANDIRI_1", "P_TELKOM_1"]
    assert body["meta"] == {"page": 1, "page_size": 2, "total": 3, "total_pages": 2}
    page2 = await client.get("/api/v1/portfolios", params={"sort_by": "value_before_tax", "sort_order": "desc", "page_size": 2, "page": 2}, headers=admin)
    assert [r["project_code"] for r in page2.json()["data"]] == ["P_MANDIRI_2"]


async def test_invalid_sort_rejected(client, admin):
    assert (await client.get("/api/v1/portfolios", params={"sort_by": "password"}, headers=admin)).status_code == 422


async def test_summary(client, admin, seeded):
    data = (await client.get("/api/v1/portfolios/summary", headers=admin)).json()["data"]
    totals = data["totals"]
    assert totals["customers"] == 2 and totals["projects"] == 3 and totals["active_projects"] == 2
    assert Decimal(totals["total_value_before_tax"]) == Decimal("6000")
    assert Decimal(totals["active_value_before_tax"]) == Decimal("5000")
    assert {s["code"]: s["project_count"] for s in data["by_status"]}["ON_GOING"] == 2
    assert {y["year"]: y["project_count"] for y in data["by_year"]} == {2025: 1, 2026: 2}
    assert [p["project_code"] for p in data["ending_soon"]] == ["P_TELKOM_1"]


# ───────────────────────── update / delete ─────────────────────────
async def test_patch_partial_and_lists(client, admin, refs):
    created = (await create(client, admin, portfolio_payload(refs))).json()["data"]
    pid = created["id"]

    patched = await client.patch(
        f"/api/v1/portfolios/{pid}",
        json={
            "project": {"project_manager": "Andi", "opportunity": None},
            "financial": {"cogs": "500000"},
            "tech_stack_ids": [refs["tech"]["data_storage"]],
            "partners": [{"partner_id": refs["partners"]["principal"], "partner_role": "Distributor"}],
        },
        headers=admin,
    )
    assert patched.status_code == 200, patched.text
    data = patched.json()["data"]
    assert data["project"]["project_manager"] == "Andi"
    assert data["project"]["account_manager"] == "Sari"  # tidak dikirim -> tetap
    assert Decimal(data["financial"]["net_profit"]) == Decimal("400000")
    assert data["tech_stack"]["frontend"] == [] and len(data["tech_stack"]["data_storage"]) == 1
    assert len(data["tech_stack"]["products"]) == 1  # tidak dikirim -> tetap
    assert [(p["partner_role"]) for p in data["partners"]] == ["Distributor"]


async def test_patch_date_order_and_empty_body(client, admin, refs):
    pid = (await create(client, admin, portfolio_payload(refs))).json()["data"]["id"]
    bad = await client.patch(f"/api/v1/portfolios/{pid}", json={"project": {"end_date": "2000-01-01"}}, headers=admin)
    assert bad.status_code == 422
    assert (await client.patch(f"/api/v1/portfolios/{pid}", json={}, headers=admin)).status_code == 400
    assert (await client.patch(f"/api/v1/portfolios/{pid}", json={"project": {"project_code": None}}, headers=admin)).status_code == 422


async def test_patch_code_conflict(client, admin, refs):
    await create(client, admin, portfolio_payload(refs, code="C_ONE"))
    two = (await create(client, admin, portfolio_payload(refs, code="C_TWO", customer=customer_payload(refs, "Other")))).json()["data"]["id"]
    response = await client.patch(f"/api/v1/portfolios/{two}", json={"project": {"project_code": "c_one"}}, headers=admin)
    assert response.status_code == 409


async def test_delete_portfolio_keeps_customer(client, admin, refs):
    created = (await create(client, admin, portfolio_payload(refs))).json()["data"]
    assert (await client.delete(f"/api/v1/portfolios/{created['id']}", headers=admin)).status_code == 200
    assert (await client.get(f"/api/v1/portfolios/{created['id']}", headers=admin)).status_code == 404
    assert (await client.get(f"/api/v1/customers/{created['customer']['id']}", headers=admin)).status_code == 200


# ───────────────────────── customers ─────────────────────────
async def test_customer_crud_and_delete_guard(client, admin, refs):
    created = await client.post("/api/v1/customers", json=customer_payload(refs), headers=admin)
    assert created.status_code == 201
    cid = created.json()["data"]["id"]
    assert (await client.post("/api/v1/customers", json=customer_payload(refs, "pt bank mandiri"), headers=admin)).status_code == 409

    patched = await client.patch(f"/api/v1/customers/{cid}", json={"location": "Bandung"}, headers=admin)
    assert patched.json()["data"]["location"] == "Bandung"

    await create(client, admin, portfolio_payload(refs, customer_id=cid))
    listing = (await client.get("/api/v1/customers", headers=admin)).json()["data"][0]
    assert listing["project_count"] == 1 and listing["active_project_count"] == 1
    assert (await client.delete(f"/api/v1/customers/{cid}", headers=admin)).status_code == 409


async def test_customer_without_projects_can_be_deleted(client, admin, refs):
    cid = (await client.post("/api/v1/customers", json=customer_payload(refs), headers=admin)).json()["data"]["id"]
    assert (await client.delete(f"/api/v1/customers/{cid}", headers=admin)).status_code == 200
    assert (await client.get(f"/api/v1/customers/{cid}", headers=admin)).status_code == 404
