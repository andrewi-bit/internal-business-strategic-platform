BEGIN;

INSERT INTO roles (id, name, code, description, is_active)
VALUES
(
    gen_random_uuid(),
    'Super Admin / Executive',
    'SUPER_ADMIN',
    'Mempunyai hak akses penuh atas pengaturan sistem, manajemen pengguna, serta tampilan Executive Dashboard yang menyajikan ringkasan performa bisnis makro, ROI, revenue pipeline, dan kesehatan portofolio secara keseluruhan.',
    TRUE
),
(
    gen_random_uuid(),
    'User Commercial / Partnership Officer',
    'COMMERCIAL_PARTNERSHIP_OFFICER',
    'Mengelola data mitra, dokumen kemitraan, status kerja sama, serta mengakses Commercial Dashboard yang berfokus pada metrik pipeline penjualan, status prospek kemitraan, dan conversion rate.',
    TRUE
),
(
    gen_random_uuid(),
    'User Engineer / Project Lead',
    'ENGINEER_PROJECT_LEAD',
    'Mengelola data teknis portofolio proyek, meninjau kapabilitas teknis mitra, serta mengakses Engineering / Operations Dashboard yang berfokus pada metrik teknis proyek, status pengerjaan portofolio, dan utilisasi sumber daya internal.',
    TRUE
)
ON CONFLICT (code) DO UPDATE SET
    name = EXCLUDED.name,
    description = EXCLUDED.description,
    is_active = EXCLUDED.is_active,
    updated_at = NOW();

INSERT INTO permissions (id, code, name, description)
VALUES
(
    gen_random_uuid(),
    'role_request.review',
    'Review Role Request',
    'Review and approve or reject role requests.'
),
(
    gen_random_uuid(),
    'user.manage',
    'Manage Users',
    'View, filter, and update user information, roles, and account status.'
),
(
    gen_random_uuid(),
    'role.manage',
    'Manage Roles and Permissions',
    'Create and update roles, manage permission metadata, and assign permissions to roles.'
)
ON CONFLICT (code) DO UPDATE SET
    name = EXCLUDED.name,
    description = EXCLUDED.description,
    updated_at = NOW();

INSERT INTO role_permissions (role_id, permission_id)
SELECT r.id, p.id
FROM roles r
CROSS JOIN permissions p
WHERE r.code = 'SUPER_ADMIN'
  AND p.code IN (
      'role_request.review',
      'user.manage',
      'role.manage'
  )
ON CONFLICT (role_id, permission_id) DO NOTHING;

COMMIT;