"""Model ORM -> dict untuk response. Semua relasi yang dibaca di sini harus sudah di-load oleh repository
(relationship dibuat lazy="raise" supaya kelupaan load langsung ketahuan, bukan diam-diam query tambahan)."""

from datetime import date
from decimal import Decimal

from app.api.portfolios import calculations as calc
from app.models.customer_model import Customer
from app.models.project_model import Project
from app.settings import settings

TECH_STACK_CATEGORIES = ("frontend", "backend", "data_storage")


def ref(item, prefix: str) -> dict:
    """Master data (company_sizes, industries, ...) sebagai {id, code, name}."""
    return {
        "id": item.id,
        "code": getattr(item, f"{prefix}_code"),
        "name": getattr(item, f"{prefix}_name"),
    }


def serialize_customer(
    customer: Customer,
    *,
    project_count: int | None = None,
    active_project_count: int | None = None,
) -> dict:
    data = {
        "id": customer.id,
        "customer_name": customer.customer_name,
        "company_size": ref(customer.company_size, "company_size"),
        "annual_revenue": customer.annual_revenue,
        "customer_type": ref(customer.customer_type, "customer_type"),
        "industry": ref(customer.industry, "industry"),
        "location": customer.location,
        "legal_structure": ref(customer.legal_structure, "legal_structure"),
        "created_at": customer.created_at,
        "updated_at": customer.updated_at,
    }

    if project_count is not None:
        data["project_count"] = project_count
        data["active_project_count"] = active_project_count or 0

    return data


def project_metrics(project: Project, today: date) -> calc.ProjectMetrics:
    return calc.project_metrics(
        value_before_tax=project.value_before_tax,
        start_date=project.start_date,
        end_date=project.end_date,
        status_code=project.project_status.project_status_code,
        today=today,
        vat_rate=settings.PORTFOLIO_VAT_RATE,
    )


def _financial_numbers(project: Project) -> tuple[Decimal, Decimal, Decimal]:
    financial = project.financial

    if financial is None:
        return project.value_before_tax, Decimal(0), Decimal(0)

    return financial.revenue, financial.cogs, financial.operational_costs


def serialize_financial(project: Project) -> dict:
    revenue, cogs, operational_costs = _financial_numbers(project)
    profit = calc.net_profit(revenue, cogs, operational_costs)

    return {
        "revenue": revenue,
        "cogs": cogs,
        "operational_costs": operational_costs,
        "net_profit": profit,
        "net_margin_percent": calc.net_margin_percent(revenue, profit),
    }


def serialize_tech_stack(project: Project) -> dict:
    grouped: dict[str, list[dict]] = {category: [] for category in TECH_STACK_CATEGORIES}

    for link in project.tech_stacks:
        item = link.tech_stack
        grouped.setdefault(item.tech_stack_category, []).append(
            {"id": item.id, "name": item.tech_stack_name}
        )

    for items in grouped.values():
        items.sort(key=lambda entry: entry["name"].lower())

    products = sorted(
        (
            {"id": link.product.id, "name": link.product.product_name}
            for link in project.products
        ),
        key=lambda entry: entry["name"].lower(),
    )

    return {"products": products, **grouped}


def serialize_partners(project: Project) -> list[dict]:
    return sorted(
        (
            {
                "partner_id": link.partner.id,
                "partner_name": link.partner.partner_name,
                "partner_role": link.partner_role,
            }
            for link in project.partners
        ),
        key=lambda entry: (entry["partner_role"].lower(), entry["partner_name"].lower()),
    )


def serialize_project(project: Project, today: date) -> dict:
    metrics = project_metrics(project, today)

    return {
        "project_code": project.project_code,
        "project_name": project.project_name,
        "opportunity": project.opportunity,
        "project_year": project.project_year,
        "contract_po_name": project.contract_po_name,
        "contract_po_number": project.contract_po_number,
        "business_unit": ref(project.business_unit, "business_unit"),
        "project_status": ref(project.project_status, "project_status"),
        "value_before_tax": project.value_before_tax,
        "value_after_tax": metrics.value_after_tax,
        "carry_over_value": project.carry_over_value,
        "project_manager": project.project_manager,
        "account_manager": project.account_manager,
        "start_date": project.start_date,
        "end_date": project.end_date,
        "total_days": metrics.total_days,
        "remaining_days": metrics.remaining_days,
        "progress_percent": metrics.progress_percent,
        "is_overdue": metrics.is_overdue,
        "project_objective": project.project_objective,
    }


def serialize_portfolio_detail(project: Project, today: date) -> dict:
    """Satu portofolio dengan kelima perspektifnya."""
    return {
        "id": project.id,
        "customer": serialize_customer(project.customer),
        "project": serialize_project(project, today),
        "financial": serialize_financial(project),
        "tech_stack": serialize_tech_stack(project),
        "partners": serialize_partners(project),
        "created_at": project.created_at,
        "updated_at": project.updated_at,
    }


def serialize_portfolio_row(project: Project, today: date) -> dict:
    """Satu baris datar untuk tabel/kartu daftar portofolio, mirip satu baris Excel."""
    metrics = project_metrics(project, today)
    revenue, cogs, operational_costs = _financial_numbers(project)
    tech_stack = serialize_tech_stack(project)

    return {
        "id": project.id,
        "project_code": project.project_code,
        "project_name": project.project_name,
        "opportunity": project.opportunity,
        "project_year": project.project_year,
        "customer_id": project.customer_id,
        "customer_name": project.customer.customer_name,
        "customer_type": ref(project.customer.customer_type, "customer_type"),
        "company_size": ref(project.customer.company_size, "company_size"),
        "industry": ref(project.customer.industry, "industry"),
        "business_unit": ref(project.business_unit, "business_unit"),
        "project_status": ref(project.project_status, "project_status"),
        "value_before_tax": project.value_before_tax,
        "value_after_tax": metrics.value_after_tax,
        "net_profit": calc.net_profit(revenue, cogs, operational_costs),
        "progress_percent": metrics.progress_percent,
        "remaining_days": metrics.remaining_days,
        "is_overdue": metrics.is_overdue,
        "project_manager": project.project_manager,
        "account_manager": project.account_manager,
        "start_date": project.start_date,
        "end_date": project.end_date,
        "products": [entry["name"] for entry in tech_stack["products"]],
        "technologies": [
            entry["name"]
            for category in TECH_STACK_CATEGORIES
            for entry in tech_stack[category]
        ],
        "partners": serialize_partners(project),
        "updated_at": project.updated_at,
    }
