-- Seed data master Portfolio dari Sheet2 Excel "Intern Business Strategic - Dashboard Dummy"
-- (acuan: dokumen Portfolio v3 bagian 1). Jalankan setelah migration portfolio_0001_master.
-- Aman dijalankan berulang: baris yang sudah ada dilewati, perubahan dari admin tidak ditimpa.

BEGIN;

INSERT INTO company_sizes (id, company_size_code, company_size_name, company_size_description, sort_order)
VALUES
    (gen_random_uuid(), 'TIER_1', 'Tier 1 : Strategic/Enterprise (>1T)', 'Asset/annual budget/annual sales di atas 1 trillion', 1),
    (gen_random_uuid(), 'TIER_2', 'Tier 2 : Growth/Valued (100B<1T)', 'Asset/annual budget/annual sales antara 100 billion sampai 1 trillion', 2),
    (gen_random_uuid(), 'TIER_3', 'Tier 3 : Standard/Transactional (50B<100B)', 'Asset/annual budget/annual sales antara 50 billion sampai 100 billion', 3),
    (gen_random_uuid(), 'TIER_4', 'Tier 4 : Standard/Transactional (10B<50B)', 'Asset/annual budget/annual sales antara 10 billion sampai 50 billion', 4),
    (gen_random_uuid(), 'TIER_5', 'Tier 5 : Standard/Transactional (1B<10B)', 'Asset/annual budget/annual sales antara 1 billion sampai 10 billion', 5),
    (gen_random_uuid(), 'TIER_6', 'Tier 6 : Standard/Transactional (<1B)', 'Asset/annual budget/annual sales di bawah 1 billion', 6)
ON CONFLICT DO NOTHING;

INSERT INTO legal_structures (id, legal_structure_code, legal_structure_name, legal_structure_description, sort_order)
VALUES
    (gen_random_uuid(), 'GOVERNMENT_INSTITUTION', 'Goverment Institution', 'Government related entities', 1),
    (gen_random_uuid(), 'STATE_OWNED_ENTERPRISE', 'State-owned Enterprise', NULL, 2),
    (gen_random_uuid(), 'PRIVATE_COMPANY', 'Private Company', 'Privately-owned companies', 3),
    (gen_random_uuid(), 'PUBLIC_SECTOR', 'Public Sector', NULL, 4)
ON CONFLICT DO NOTHING;

INSERT INTO business_units (id, business_unit_code, business_unit_name, business_unit_description, sort_order)
VALUES
    (gen_random_uuid(), 'ITMS', 'ITMS', 'IT Manage Service', 1),
    (gen_random_uuid(), 'CSD', 'CSD', 'Custom Solution Development', 2),
    (gen_random_uuid(), 'SI', 'SI', 'System Integrator', 3)
ON CONFLICT DO NOTHING;

INSERT INTO customer_types (id, customer_type_code, customer_type_name, customer_type_description, sort_order)
VALUES
    (gen_random_uuid(), 'STRATEGIC_CUSTOMER', 'Strategic Customer', NULL, 1),
    (gen_random_uuid(), 'REGULAR_CUSTOMER', 'Regular Customer', NULL, 2)
ON CONFLICT DO NOTHING;

INSERT INTO project_statuses (id, project_status_code, project_status_name, project_status_description, sort_order)
VALUES
    (gen_random_uuid(), 'ON_GOING', 'On Going', 'Project is still running', 1),
    (gen_random_uuid(), 'ON_PROPOSAL', 'On Proposal', 'Project is in negotiation', 2),
    (gen_random_uuid(), 'CLOSED', 'Closed', 'Project is finished', 3),
    (gen_random_uuid(), 'CANCELED', 'Canceled', 'Project is canceled', 4)
ON CONFLICT DO NOTHING;

INSERT INTO product_statuses (id, product_status_code, product_status_name, product_status_description, sort_order)
VALUES
    (gen_random_uuid(), 'READY_TO_SELL', 'Ready to Sell', NULL, 1),
    (gen_random_uuid(), 'UNDER_DEVELOPMENT', 'Under Development', NULL, 2),
    (gen_random_uuid(), 'ON_HOLD', 'On Hold', NULL, 3),
    (gen_random_uuid(), 'DEPRECATED', 'Deprecated', NULL, 4)
ON CONFLICT DO NOTHING;

INSERT INTO industries (id, industry_code, industry_name, industry_description, sort_order)
VALUES
    (gen_random_uuid(), 'GOVERNMENT', 'Government', NULL, 1),
    (gen_random_uuid(), 'AGRICULTURE', 'Agriculture', NULL, 2),
    (gen_random_uuid(), 'MINING_AND_QUARRYING', 'Mining and Quarrying', NULL, 3),
    (gen_random_uuid(), 'OIL_AND_GAS', 'Oil and Gas', NULL, 4),
    (gen_random_uuid(), 'FISHING', 'Fishing', NULL, 5),
    (gen_random_uuid(), 'MANUFACTURING', 'Manufacturing', NULL, 6),
    (gen_random_uuid(), 'CONSTRUCTION', 'Construction', NULL, 7),
    (gen_random_uuid(), 'UTILITIES', 'Utilities', NULL, 8),
    (gen_random_uuid(), 'RETAIL_AND_WHOLESALE_TRADE', 'Retail and Wholesale Trade', NULL, 9),
    (gen_random_uuid(), 'FINANCIAL_SERVICES', 'Financial Services', NULL, 10),
    (gen_random_uuid(), 'TRANSPORTATION_AND_LOGISTICS', 'Transportation and Logistics', NULL, 11),
    (gen_random_uuid(), 'HOSPITALITY_AND_TOURISM', 'Hospitality and Tourism', NULL, 12),
    (gen_random_uuid(), 'HEALTHCARE', 'Healthcare', NULL, 13),
    (gen_random_uuid(), 'EDUCATION', 'Education', NULL, 14),
    (gen_random_uuid(), 'INFORMATION_TECHNOLOGY_AND_SOFTWARE', 'Information Technology (IT) and Software', NULL, 15),
    (gen_random_uuid(), 'TELECOMMUNICATIONS', 'Telecommunications', NULL, 16),
    (gen_random_uuid(), 'RESEARCH_AND_DEVELOPMENT', 'Research and Development (R&D)', NULL, 17),
    (gen_random_uuid(), 'CONSULTING', 'Consulting', NULL, 18),
    (gen_random_uuid(), 'ARTIFICIAL_INTELLIGENCE_AND_MACHINE_LEARNING', 'Artificial Intelligence (AI) and Machine Learning', NULL, 19),
    (gen_random_uuid(), 'RENEWABLE_ENERGY', 'Renewable Energy', NULL, 20),
    (gen_random_uuid(), 'BIOTECHNOLOGY', 'Biotechnology', NULL, 21),
    (gen_random_uuid(), 'FINTECH', 'Fintech', NULL, 22),
    (gen_random_uuid(), 'E_COMMERCE_AND_DIGITAL_MARKETING', 'E-commerce and Digital Marketing', NULL, 23),
    (gen_random_uuid(), 'AEROSPACE_AND_DEFENSE', 'Aerospace and Defense', NULL, 24),
    (gen_random_uuid(), 'REAL_ESTATE_TECHNOLOGY', 'Real Estate Technology (PropTech)', NULL, 25)
ON CONFLICT DO NOTHING;

-- Sheet2 tidak menyebut status tiap product, jadi semua product awal berstatus Ready to Sell.
INSERT INTO products (id, product_name, product_description, product_status_id)
SELECT gen_random_uuid(), seed.product_name, NULL, product_statuses.id
FROM (
    VALUES
        ('Bliv Package'),
        ('Bliv Pipeline'),
        ('Bliv Dashboard'),
        ('Bliv AI'),
        ('Bliv Explore'),
        ('Bliv Data House'),
        ('Bliv MlOps'),
        ('Bliv Monitoring'),
        ('Bliv Technical Support'),
        ('Bliv Professional Services'),
        ('Semeru ERP'),
        ('Semeru Net'),
        ('Zabbix Training'),
        ('Zabbix Professional Services'),
        ('Zabbix Technical Support'),
        ('Teslakom SMA-TV')
) AS seed (product_name)
JOIN product_statuses ON product_statuses.product_status_code = 'READY_TO_SELL'
ON CONFLICT DO NOTHING;

INSERT INTO tech_stacks (id, tech_stack_category, tech_stack_name)
VALUES
    (gen_random_uuid(), 'frontend', 'Vue.js (Vue, Vue2, Vue3)'),
    (gen_random_uuid(), 'frontend', 'React'),
    (gen_random_uuid(), 'frontend', 'Nuxt 3 (JavaScript)'),
    (gen_random_uuid(), 'frontend', 'Flutter 3'),
    (gen_random_uuid(), 'frontend', 'PHP (CI3, CI4)'),
    (gen_random_uuid(), 'frontend', 'PHP (Laravel)'),
    (gen_random_uuid(), 'backend', 'Python (Flask API, FastAPI)'),
    (gen_random_uuid(), 'backend', 'Golang'),
    (gen_random_uuid(), 'backend', 'PHP (CI3, CI4)'),
    (gen_random_uuid(), 'backend', 'Java (for custom NiFi components)'),
    (gen_random_uuid(), 'backend', 'PHP (Laravel)'),
    (gen_random_uuid(), 'data_storage', 'PostgreSQL (Postgres)'),
    (gen_random_uuid(), 'data_storage', 'TimescaleDB'),
    (gen_random_uuid(), 'data_storage', 'MySQL'),
    (gen_random_uuid(), 'data_storage', 'ClickHouse (with CHProxy)'),
    (gen_random_uuid(), 'data_storage', 'DuckDB'),
    (gen_random_uuid(), 'data_storage', 'Redis'),
    (gen_random_uuid(), 'data_storage', 'Hadoop'),
    (gen_random_uuid(), 'data_storage', 'Minio'),
    (gen_random_uuid(), 'data_storage', 'Google Cloud Storage'),
    (gen_random_uuid(), 'data_storage', 'Elasticsearch'),
    (gen_random_uuid(), 'data_storage', 'PGVector'),
    (gen_random_uuid(), 'data_storage', 'Weaviate'),
    (gen_random_uuid(), 'data_storage', 'OpenMetadata')
ON CONFLICT DO NOTHING;

COMMIT;
