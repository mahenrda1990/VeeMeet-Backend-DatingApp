-- Initialize local Postgres role and database for VeeMeet
-- Run this as a superuser (e.g. postgres):
--   psql -U postgres -f sql/init_db.sql

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_roles WHERE rolname = 'veemeet_user'
    ) THEN
        CREATE ROLE veemeet_user LOGIN PASSWORD 'veemeet_password';
    END IF;
END
$$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_database WHERE datname = 'veemeet_local'
    ) THEN
        CREATE DATABASE veemeet_local OWNER veemeet_user;
    END IF;
END
$$;

-- Ensure veemeet_user can create extensions in veemeet_local
ALTER DATABASE veemeet_local OWNER TO veemeet_user;
GRANT ALL PRIVILEGES ON DATABASE veemeet_local TO veemeet_user;
