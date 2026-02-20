-- Migration: add phone_number and registration_step to users
-- Run this against an existing database to apply the new columns.

ALTER TABLE users
    ADD COLUMN IF NOT EXISTS phone_number TEXT UNIQUE,
    ADD COLUMN IF NOT EXISTS registration_step INT DEFAULT 0;

-- Make email and password_hash nullable so phone-only accounts work
ALTER TABLE users
    ALTER COLUMN email DROP NOT NULL,
    ALTER COLUMN password_hash DROP NOT NULL;
