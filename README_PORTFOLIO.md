# Modul Portofolio (Customer, Project, Financial, Tech Stack, Partner)

Satu baris Excel "Dashboard Dummy" = satu portofolio = satu baris `projects`. Tiap perspektif punya tabel sendiri
yang terhubung lewat foreign key.

| Perspektif | Tabel | Relasi |
|---|---|---|
| Customer | `customers` | 1 customer → banyak `projects` (`projects.customer_id`, RESTRICT) |
| Project | `projects` | inti portofolio; FK ke `customers`, `business_units`, `project_statuses` |
| Financial | `project_financials` | 1:1 ke `projects` (CASCADE) |
| Tech Stack | `project_products` (Product Use), `project_tech_stacks` (Frontend/Backend/Data & Storage) | N:M ke `products` / `tech_stacks` |
| Partner | `project_partners` (+ `partner_role`, mis. Principal/Vendor) | N:M ke `partners` |

Nilai formula Excel **tidak disimpan**, dihitung saat dibaca: value after tax (`× 1,11`, `PORTFOLIO_VAT_RATE`),
total days, remaining days, progress, net profit, net margin. "Hari ini" memakai WIB.
Project **aktif** = status `ON_GOING`.

## Setup
```bash
cd src/backend
alembic upgrade head                      # termasuk portfolio_0002_perspectives
psql "$DB" -f ../../seed_roles_permissions.sql
psql "$DB" -f ../../seed_portfolio_permissions.sql   # BARU: portfolio.view / portfolio.manage
psql "$DB" -f ../../seed_portfolio_master.sql
```
Tanpa `seed_portfolio_permissions.sql`, semua user mendapat 403 di `/partners`, `/products`, `/master-data`,
`/customers`, `/portfolios` (permission-nya sebelumnya tidak pernah di-seed).

## Endpoint (prefix `/api/v1`)
Semua GET butuh `portfolio.view`; POST/PATCH/DELETE butuh `portfolio.manage`.

- `GET /portfolios` — filter: `search`, `customer_id`, `customer_name`, `industry_id`, `company_size_id`,
  `customer_type_id`, `business_unit_id`, `project_status_id` (boleh berulang), `active_only`, `year`, `product_id`,
  `tech_stack_id`, `partner_id`, `project_manager`, `account_manager`; `sort_by`, `sort_order`, `page`, `page_size`.
- `GET /portfolios/summary` — angka dashboard: total & aktif, nilai, net profit, per status / business unit /
  industri / ukuran perusahaan / tahun / produk, dan 5 project aktif yang segera berakhir (≤ 90 hari).
- `GET /portfolios/{id}` — kelima perspektif sekaligus.
- `POST /portfolios` — `customer_id` (yang ada) **atau** `customer` (buat baru), plus `project`, `financial`,
  `product_ids`, `tech_stack_ids`, `partners`. `financial.revenue` kosong = `value_before_tax`.
- `PATCH /portfolios/{id}` — hanya bagian yang dikirim yang berubah; list yang dikirim menggantikan list lama.
- `DELETE /portfolios/{id}`
- `GET/POST /customers`, `GET/PATCH/DELETE /customers/{id}` (hapus ditolak 409 bila masih punya project),
  `GET /customers/{id}/portfolios` — "filter by customer": semua project milik satu customer.

Error referensi (id master tidak ada / nonaktif) → `422` dengan `error.code = "INVALID_REFERENCE"`.

## Import Excel
```bash
cd src/backend
python -m app.scripts.import_portfolio_excel "Intern Business Strategic - Dashboard Dummy.xlsx" --dry-run
python -m app.scripts.import_portfolio_excel "Intern Business Strategic - Dashboard Dummy.xlsx"
```
Idempotent (kunci: Project ID). Nilai master yang tidak dikenal dilaporkan per baris dan **tidak ada yang disimpan**
kecuali memakai `--skip-invalid`. Customer Size dicocokkan lewat nomor tier (jadi "100M" vs "100B" tidak masalah).
Partner baru dibuat otomatis.

## Test
```bash
createdb ibsp_test   # kosong; migrasi & seed dijalankan otomatis oleh conftest
TEST_DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/ibsp_test pytest
```
Butuh Postgres sungguhan (ILIKE, FILTER, constraint). Redis dipalsukan. `openpyxl` (dependency) dipakai import Excel dan test-nya
(sudah masuk dependency).
