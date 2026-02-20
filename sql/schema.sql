CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =========================
-- USERS
-- =========================
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    phone_number TEXT UNIQUE,
    email TEXT UNIQUE,
    password_hash TEXT,
    first_name TEXT,
    birth_date DATE,
    gender TEXT,
    profile_completion INT DEFAULT 0,
    registration_step INT DEFAULT 0,
    hide_name BOOLEAN DEFAULT FALSE,
    snoozed_until TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT now(),
    -- Onboarding / profile fields derived from the mobile flow
    gender_subs TEXT[],
    show_gender_on_profile BOOLEAN DEFAULT TRUE,
    gender_visible_labels TEXT[],
    email_marketing_opt_in BOOLEAN DEFAULT FALSE,
    mode TEXT,
    dating_preferences TEXT[],
    open_to_everyone BOOLEAN DEFAULT FALSE,
    dating_intentions TEXT[],
    height_cm INT,
    interests TEXT[],
    drinking_habit TEXT,
    smoking_habit TEXT,
    have_kids TEXT,
    kids_plan TEXT,
    religion TEXT,
    politics TEXT,
    prompts TEXT[],
    location_latitude DOUBLE PRECISION,
    location_longitude DOUBLE PRECISION,
    location_address TEXT
);

-- =========================
-- PROFILE PHOTOS
-- =========================
CREATE TABLE profile_photos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    photo_url TEXT NOT NULL,
    position INT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- =========================
-- USER ATTRIBUTES
-- (education, smoking, drinking, exercise, star_sign, etc.)
-- =========================
CREATE TABLE user_attributes (
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    attribute_key VARCHAR(50),
    attribute_value VARCHAR(100),
    PRIMARY KEY (user_id, attribute_key)
);

-- =========================
-- FILTER PREFERENCES
-- =========================
CREATE TABLE user_filter_preferences (
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    filter_key VARCHAR(50),
    filter_values JSONB,
    allow_fallback BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (user_id, filter_key)
);

-- =========================
-- LIKES
-- =========================
CREATE TABLE likes (
    liker_id UUID REFERENCES users(id) ON DELETE CASCADE,
    liked_id UUID REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT now(),
    PRIMARY KEY (liker_id, liked_id)
);

-- =========================
-- MATCHES
-- =========================
CREATE TABLE matches (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_1 UUID REFERENCES users(id),
    user_2 UUID REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE (user_1, user_2)
);

-- =========================
-- DISCOVER (DAILY CURATION)
-- =========================
CREATE TABLE discover_batches (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    generated_for DATE,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE discover_candidates (
    batch_id UUID REFERENCES discover_batches(id) ON DELETE CASCADE,
    candidate_user_id UUID REFERENCES users(id),
    rank INT,
    reason TEXT
);

-- =========================
-- SPOTLIGHT
-- =========================
CREATE TABLE user_spotlights (
    user_id UUID PRIMARY KEY REFERENCES users(id),
    balance INT DEFAULT 0
);

CREATE TABLE spotlight_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    started_at TIMESTAMPTZ,
    ends_at TIMESTAMPTZ,
    multiplier FLOAT DEFAULT 1.0
);
