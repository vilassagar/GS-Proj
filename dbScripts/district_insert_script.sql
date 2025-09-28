-- PostgreSQL Script to Insert Distinct Districts
-- Based on the districts table structure provided

-- First, let's ensure we're working with the correct table structure
-- This script assumes the table already exists as per your definition

-- Begin transaction for data integrity
BEGIN;

-- Insert distinct districts with proper error handling
-- Replace the VALUES section with your actual district data

INSERT INTO public.districts (name, created_at, updated_at, is_active, code)
VALUES 
    ('नंदुरबार', NOW(), NOW(), true, '497'),
    ('धुळे', NOW(), NOW(), true, '498'),
    ('जळगाव', NOW(), NOW(), true, '499'),
    ('बुलढाणा', NOW(), NOW(), true, '500'),
    ('अकोला', NOW(), NOW(), true, '501'),
    ('वाशीम', NOW(), NOW(), true, '502'),
    ('अमरावती', NOW(), NOW(), true, '503'),
    ('वर्धा', NOW(), NOW(), true, '504'),
    ('नागपूर', NOW(), NOW(), true, '505'),
    ('भंडारा', NOW(), NOW(), true, '506'),
    ('गोंदिया', NOW(), NOW(), true, '507'),
    ('गडचिरोली', NOW(), NOW(), true, '508'),
    ('चंद्रपुर', NOW(), NOW(), true, '509'),
    ('यवतमाळ', NOW(), NOW(), true, '510'),
    ('नांदेड', NOW(), NOW(), true, '511'),
    ('हिंगोली', NOW(), NOW(), true, '512'),
    ('परभाणी', NOW(), NOW(), true, '513'),
    ('जालना', NOW(), NOW(), true, '514'),
    ('औरंगाबाद', NOW(), NOW(), true, '515'),
    ('नाशिक', NOW(), NOW(), true, '516'),
    ('ठाणे', NOW(), NOW(), true, '517'),
    ('रायगड', NOW(), NOW(), true, '520'),
    ('पुणे', NOW(), NOW(), true, '521'),
    ('अहमदनगर', NOW(), NOW(), true, '522'),
    ('बीड', NOW(), NOW(), true, '523'),
    ('लातूर', NOW(), NOW(), true, '524'),
    ('उस्मानाबाद', NOW(), NOW(), true, '525'),
    ('सोलापूर', NOW(), NOW(), true, '526'),
    ('सातारा', NOW(), NOW(), true, '527'),
    ('रत्नागिरी', NOW(), NOW(), true, '528'),
    ('सिंधुदुर्ग', NOW(), NOW(), true, '529'),
    ('कोल्हापूर', NOW(), NOW(), true, '530'),
    ('सांगली', NOW(), NOW(), true, '531'),
    ('पालघर', NOW(), NOW(), true, '532')
ON CONFLICT (code) DO NOTHING;  -- Prevents duplicate entries based on unique code constraint

-- Alternative approach using ON CONFLICT with code if you want to update existing records
-- ON CONFLICT (code) DO UPDATE SET 
--     name = EXCLUDED.name,
--     updated_at = NOW(),
--     is_active = EXCLUDED.is_active;

-- Commit the transaction
COMMIT;

-- Verification query to check inserted data
SELECT 
    id,
    name,
    code,
    created_at,
    updated_at,
    is_active
FROM public.districts 
ORDER BY name;

-- Additional utility queries

-- Count total districts
SELECT COUNT(*) as total_districts FROM public.districts;

-- Check for any duplicate names (should return 0 if unique constraint is working)
SELECT name, COUNT(*) as count
FROM public.districts 
GROUP BY name 
HAVING COUNT(*) > 1;

-- Check for any duplicate codes (should return 0 if unique constraint is working)
SELECT code, COUNT(*) as count
FROM public.districts 
GROUP BY code 
HAVING COUNT(*) > 1;

-- Query to find districts with null or empty codes
SELECT * FROM public.districts WHERE code IS NULL OR code = '';

-- Query to deactivate specific districts if needed
-- UPDATE public.districts SET is_active = false, updated_at = NOW() 
-- WHERE name IN ('District Name to Deactivate');

-- Sample bulk insert template for large datasets
-- If you have a CSV file, you can use COPY command:
-- COPY public.districts (name, code, is_active) 
-- FROM '/path/to/your/districts.csv' 
-- WITH (FORMAT csv, HEADER true)
-- ON CONFLICT (name) DO NOTHING;

-- Generate district codes automatically if not provided
-- UPDATE public.districts 
-- SET code = 'DIST' || LPAD(id::text, 3, '0'), updated_at = NOW()
-- WHERE code IS NULL;