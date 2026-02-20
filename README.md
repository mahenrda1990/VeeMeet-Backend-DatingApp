# Dating App Backend API

This is a comprehensive dating app backend built with FastAPI that implements all the features defined in the database schema.

## Features

### Authentication
- User registration
- User login (basic password authentication)

### User Profile Management
- Get user profile (own and others)
- Update profile information
- Manage profile photos (add, delete, reorder)
- Manage user attributes (education, smoking, drinking, etc.)

### Filtering System
- Set filter preferences with JSONB values
- Fallback options for filters
- Delete filter preferences

### Discovery System
- Daily curation batches for users
- Ranked candidate recommendations
- Date-specific discovery

### Likes & Matches
- Like other users
- Automatic match creation on mutual likes
- View like history
- View matches

### Spotlight System
- Spotlight balance management
- Activate spotlight sessions with multipliers
- View active and historical spotlight sessions

## API Endpoints

### Authentication (`/auth`)
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user

### Profile Management (`/profile`)
- `GET /profile/me` - Get current user's profile
- `PUT /profile/me` - Update current user's profile
- `GET /profile/{user_id}` - Get another user's profile
- `POST /profile/photos` - Add profile photo
- `GET /profile/photos` - Get user's photos
- `DELETE /profile/photos/{photo_id}` - Delete photo
- `PUT /profile/photos/reorder` - Reorder photos
- `POST /profile/attributes` - Add/update attribute
- `GET /profile/attributes` - Get user attributes
- `DELETE /profile/attributes/{key}` - Delete attribute

### Filters (`/filters`)
- `GET /filters/` - Get filter preferences
- `POST /filters/` - Save filter preference
- `DELETE /filters/{filter_key}` - Delete filter

### Discovery (`/discover`)
- `GET /discover/` - Get today's discover candidates
- `GET /discover/{date}` - Get candidates for specific date

### Likes & Matches (`/likes`)
- `POST /likes/{target_id}` - Like a user
- `GET /likes/history` - Get like history
- `GET /likes/matches` - Get matches

### Spotlight (`/spotlight`)
- `GET /spotlight/balance` - Get spotlight balance
- `POST /spotlight/activate` - Activate spotlight
- `GET /spotlight/active` - Get active session
- `GET /spotlight/history` - Get session history
- `POST /spotlight/add-balance/{amount}` - Add balance (admin)

### Users (`/users`)
- `POST /users/` - Register user (alternative endpoint)

## Database Models

The API implements all tables from the schema:
- `users` - User accounts
- `profile_photos` - User profile photos
- `user_attributes` - User attributes (education, etc.)
- `user_filter_preferences` - Filter preferences with JSONB
- `likes` - User likes
- `matches` - Mutual matches
- `discover_batches` - Daily curation batches
- `discover_candidates` - Curated candidates
- `user_spotlights` - Spotlight balances
- `spotlight_sessions` - Active/historical spotlight sessions

## Setup

1. Create and activate a virtual environment, then install dependencies:
```bash
cd VeeMeet-Backend

# create venv (only once)
python3 -m venv app/venv

# activate venv (every time you work on the backend)
source app/venv/bin/activate

# install dependencies into this venv
pip install -r app/requirements.txt
```

2. Create local Postgres role & database

Make sure PostgreSQL is running locally, then as a superuser (e.g. `postgres`):

```bash
cd VeeMeet-Backend
psql -U postgres -f sql/init_db.sql
```

This will create:
- role: `veemeet_user` (password `veemeet_password`)
- database: `veemeet_local` owned by `veemeet_user`

3. Apply schema and seed data

```bash
psql -U veemeet_user -d veemeet_local -f sql/schema.sql
psql -U veemeet_user -d veemeet_local -f sql/seed_users.sql
```

`schema.sql` creates all tables (users, photos, attributes, filters, likes, matches, discover, spotlight, etc.) and includes extra columns on `users` for the full onboarding flow (mode, preferences, lifestyle, values, prompts, location, etc.).

`seed_users.sql` inserts a handful of fully-onboarded dummy users from different cities and with varied interests and habits, so the app can show realistic lists immediately.

4. Configure database URL

The application reads `DATABASE_URL` from `app/.env`. By default it is set to:

```dotenv
DATABASE_URL=postgresql://veemeet_user:veemeet_password@localhost:5432/veemeet_local
```

Update this if your local Postgres details differ.

5. Run the application (with the venv still activated):

```bash
cd VeeMeet-Backend
uvicorn app.main:app --reload
```

6. Access API documentation at `http://localhost:8000/docs`

## Authentication Note

Currently uses a temporary hardcoded user ID for development. In production, this should be replaced with proper JWT token authentication middleware.

## Testing
All endpoints support automatic validation via FastAPI and include comprehensive error handling. The API returns appropriate HTTP status codes and detailed error messages.

For a quick local smoke test once the server is running on `localhost:8000`:

```bash
# Check that the app is up
curl http://localhost:8000/docs

# Fetch the (temporary) current user's profile
curl http://localhost:8000/profile/me

# List likes and matches for the hardcoded dev user
curl http://localhost:8000/likes/history
curl http://localhost:8000/likes/matches
```

The `profile/me` response should include the extended onboarding fields on the `users` table, and the `users` table should contain the seeded demo users from `sql/seed_users.sql`.