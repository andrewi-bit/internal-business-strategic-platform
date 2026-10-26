-- Permission modul Portfolio. Dipakai oleh require_permission("portfolio.view" / "portfolio.manage")
-- di /partners, /products, /tech-stacks, /master-data, /customers dan /portfolios.
-- Jalankan setelah seed_roles_permissions.sql. Aman dijalankan berulang.
--
-- ASUMSI (mohon dikonfirmasi mentor): view untuk ketiga role, manage untuk SUPER_ADMIN dan ENGINEER_PROJECT_LEAD.
BEGIN;

INSERT INTO permissions (id, code, name, description)
VALUES
    (gen_random_uuid(), 'portfolio.view', 'View Portfolio',
     'Melihat portofolio, customer, dashboard portofolio, dan master data portofolio.'),
    (gen_random_uuid(), 'portfolio.manage', 'Manage Portfolio',
     'Menambah, mengubah, dan menghapus portofolio, customer, serta master data portofolio.')
ON CONFLICT (code) DO UPDATE SET
    name = EXCLUDED.name,
    description = EXCLUDED.description,
    updated_at = NOW();

INSERT INTO role_permissions (role_id, permission_id)
SELECT r.id, p.id
FROM roles r
JOIN permissions p ON p.code = 'portfolio.view'
WHERE r.code IN ('SUPER_ADMIN', 'COMMERCIAL_PARTNERSHIP_OFFICER', 'ENGINEER_PROJECT_LEAD')
ON CONFLICT (role_id, permission_id) DO NOTHING;

INSERT INTO role_permissions (role_id, permission_id)
SELECT r.id, p.id
FROM roles r
JOIN permissions p ON p.code = 'portfolio.manage'
WHERE r.code IN ('SUPER_ADMIN', 'ENGINEER_PROJECT_LEAD')
ON CONFLICT (role_id, permission_id) DO NOTHING;

COMMIT;
