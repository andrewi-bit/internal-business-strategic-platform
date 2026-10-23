INSERT INTO divisions (id, name, code, is_active)
VALUES
    (gen_random_uuid(), 'Business Strategic', 'BUSINESS_STRATEGIC', TRUE),
    (gen_random_uuid(), 'Commercial & Marketing', 'COMMERCIAL_MARKETING', TRUE),
    (gen_random_uuid(), 'Business Consultant', 'BUSINESS_CONSULTANT', TRUE),
    (gen_random_uuid(), 'Operation', 'OPERATION', TRUE),
    (gen_random_uuid(), 'Product Ecosystem', 'PRODUCT_ECOSYSTEM', TRUE),
    (gen_random_uuid(), 'IT Engineering', 'IT_ENGINEERING', TRUE),
    (gen_random_uuid(), 'Finance & Accounting', 'FINANCE_ACCOUNTING', TRUE),
    (gen_random_uuid(), 'People & Culture', 'PEOPLE_CULTURE', TRUE)
ON CONFLICT (code) DO UPDATE SET
    name = EXCLUDED.name,
    is_active = EXCLUDED.is_active,
    updated_at = NOW();
