from datetime import datetime

import openpyxl
import pytest
from sqlalchemy import func, select

from app.scripts.import_portfolio_excel import (
    HEADERS,
    normalize,
    parse_partners,
    run_import,
    split_multi,
)


# ───────────────────────── parser ─────────────────────────
def test_split_multi_respects_quotes_and_parentheses():
    cell = '"Vue.js (Vue, Vue2, Vue3)", Nuxt 3 (JavaScript)'
    assert split_multi(cell) == ["Vue.js (Vue, Vue2, Vue3)", "Nuxt 3 (JavaScript)"]
    assert split_multi('"Python (Flask API, FastAPI)", "PHP (CI3, CI4)"') == [
        "Python (Flask API, FastAPI)",
        "PHP (CI3, CI4)",
    ]
    assert split_multi(None) == [] and split_multi("  ") == []
    assert split_multi("A, a, B") == ["A", "B"]  # dobel (beda huruf) dibuang


def test_parse_partners():
    assert parse_partners("Principal: Zabbix SIA, \nVendor: PT Bangunindo Teknusa") == [
        ("Principal", "Zabbix SIA"),
        ("Vendor", "PT Bangunindo Teknusa"),
    ]
    assert parse_partners("Zabbix SIA") == [("Partner", "Zabbix SIA")]


# ───────────────────────── impor end-to-end ─────────────────────────
ROW = {
    "customer": "PT Import Uji",
    "company_size": "Tier 2 : Growth/Valued (100M<1T)",  # typo 100M vs 100B di Excel: cocok lewat nomor tier
    "annual_revenue": "10T (FY 2025)",
    "customer_type": "Strategic Customer",
    "industry": "Government",
    "location": "Jakarta",
    "legal_structure": "State-owned Enterprise",
    "opportunity": "Opp",
    "project_name": "Import Project",
    "year": 2026.0,
    "business_unit": "ITMS",
    "project_code": "IMPORT_TEST_001",
    "value_before_tax": 1000.0,
    "status": "On Going",
    "start_date": datetime(2026, 1, 1),
    "end_date": datetime(2026, 12, 31),
    "revenue": 1000,
    "cogs": 400.0,
    "opex": 100.0,
    "partners": "Principal: Import Partner A, \nVendor: Import Partner B",
}


def build_workbook(path, rows):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Sheet1"
    keys = list(HEADERS)
    sheet.append(["Customer Perspective"])
    sheet.append([HEADERS[key] for key in keys])
    for row in rows:
        sheet.append([row.get(key) for key in keys])
    sheet.append([None] * len(keys))  # baris kosong berformat harus dilewati
    workbook.save(path)


async def counts(db):
    from app.models.customer_model import Customer
    from app.models.project_model import Project

    return (
        (await db.execute(select(func.count(Project.id)))).scalar_one(),
        (await db.execute(select(func.count(Customer.id)))).scalar_one(),
    )


async def test_import_is_idempotent(tmp_path, db, refs):
    path = tmp_path / "data.xlsx"
    build_workbook(path, [ROW])

    summary, results = await run_import(path)
    assert not [r for r in results if r.errors], [r.errors for r in results]
    assert (summary.projects_created, summary.customers_created) == (1, 1)
    assert await counts(db) == (1, 1)

    again, _ = await run_import(path)
    assert (again.projects_created, again.projects_updated) == (0, 1)
    assert await counts(db) == (1, 1)

    changed = {**ROW, "cogs": 500.0}
    build_workbook(path, [changed])
    await run_import(path)

    from app.models.project_financial_model import ProjectFinancial

    assert (await db.execute(select(ProjectFinancial.cogs))).scalar_one() == 500


async def test_import_reports_unknown_values_and_saves_nothing(tmp_path, db, refs):
    path = tmp_path / "bad.xlsx"
    build_workbook(path, [ROW, {**ROW, "project_code": "IMPORT_TEST_002", "industry": "Nope", "frontend": "NoSuchFramework"}])

    summary, results = await run_import(path)
    bad = [r for r in results if r.errors]
    assert len(bad) == 1 and bad[0].project_code == "IMPORT_TEST_002"
    assert any("Industry" in e for e in bad[0].errors) and any("frontend" in e for e in bad[0].errors)
    assert await counts(db) == (0, 0)

    skipped, _ = await run_import(path, skip_invalid=True)
    assert skipped.projects_created == 1 and skipped.skipped == 1
    assert await counts(db) == (1, 1)


async def test_import_dry_run_and_duplicate_ids(tmp_path, db, refs):
    path = tmp_path / "dry.xlsx"
    build_workbook(path, [ROW])
    await run_import(path, dry_run=True)
    assert await counts(db) == (0, 0)

    build_workbook(path, [ROW, {**ROW, "project_code": "import_test_001"}])
    _, results = await run_import(path)
    assert any("dobel" in e for r in results for e in r.errors)


def test_normalize():
    assert normalize("  On   Going ") == "on going"
