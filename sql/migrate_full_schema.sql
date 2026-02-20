-- Full migration: bring existing users table up to date with the current model.
-- Safe to run multiple times (uses ADD COLUMN IF NOT EXISTS).

ALTER TABLE users
    ADD COLUMN IF NOT EXISTS phone_number         TEXT UNIQUE,
    ADD COLUMN IF NOT EXISTS registration_step    INT DEFAULT 0,
    ADD COLUMN IF NOT EXISTS gender_subs          TEXT[],
    ADD COLUMN IF NOT EXISTS show_gender_on_profile BOOLEAN DEFAULT TRUE,
    ADD COLUMN IF NOT EXISTS gender_visible_labels TEXT[],
    ADD COLUMN IF NOT EXISTS email_marketing_opt_in BOOLEAN DEFAULT FALSE,
    ADD COLUMN IF NOT EXISTS mode                 TEXT,
    ADD COLUMN IF NOT EXISTS dating_preferences   TEXT[],
    ADD COLUMN IF NOT EXISTS open_to_everyone     BOOLEAN DEFAULT FALSE,
    ADD COLUMN IF NOT EXISTS dating_intentions    TEXT[],
    ADD COLUMN IF NOT EXISTS height_cm            INT,
    ADD COLUMN IF NOT EXISTS interests            TEXT[],
    ADD COLUMN IF NOT EXISTS drinking_habit       TEXT,
    ADD COLUMN IF NOT EXISTS smoking_habit        TEXT,
    ADD COLUMN IF NOT EXISTS have_kids            TEXT,
    ADD COLUMN IF NOT EXISTS kids_plan            TEXT,
    ADD COLUMN IF NOT EXISTS religion             TEXT,
    ADD COLUMN IF NOT EXISTS politics             TEXT,
    ADD COLUMN IF NOT EXISTS prompts              TEXT[],
    ADD COLUMN IF NOT EXISTS location_latitude    DOUBLE PRECISION,
    ADD COLUMN IF NOT EXISTS location_longitude   DOUBLE PRECISION,
    ADD COLUMN IF NOT EXISTS location_address     TEXT;

-- Make email and password_hash nullable so phone-only accounts work
ALTER TABLE users
    ALTER COLUMN email DROP NOT NULL,
    ALTER COLUMN password_hash DROP NOT NULL;
