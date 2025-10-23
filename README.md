# CODE Network

A simple web app for managing contacts in the CODE community.

## What it does

- Add contacts
- View all contacts
- Store contact info in a cloud database (Supabase)

## Setup

### 1. Create a Supabase account

1. Go to [supabase.com](https://supabase.com) and sign up
2. Create a new project
3. Wait for the database to be set up

### 2. Get your database credentials

1. Go to Project Settings > Database
2. Find the "Connection String" section
3. Copy the URI connection string (it looks like: `postgresql://postgres.[project-ref]:[password]@...`)

### 3. Configure your environment

Create a `.env` file in the `Project.py` folder:

```bash
SUPABASE_DB_URL=postgresql://postgres.[your-project-ref]:[your-password]@aws-0-[region].pooler.supabase.com:5432/postgres
```

Replace the placeholder values with your actual Supabase credentials.

### 4. Install dependencies

```bash
cd Project.py
source venv/bin/activate
pip install -r requirements.txt
```

### 5. Run the app

```bash
python3 app.py
```

Then go to: http://127.0.0.1:8080

The database tables will be created automatically on first run.

## Technologies used

- Python
- Flask
- Supabase (PostgreSQL)
- SQLAlchemy
- HTML/CSS

## Files

- `app.py` - main application
- `views/` - HTML pages
- `public/css/` - styling
- `.env` - database credentials (not in git)

That's it!
