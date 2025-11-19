# Running the Application Locally

## The Problem (SOLVED)

The app was failing to start because it was trying to connect to a Supabase database that wasn't accessible. The error was:

```
psycopg2.OperationalError: could not translate host name "db.evogkfxqtiluxkmkuxpy.supabase.co" to address
```

## The Solution

You now have two ways to run the application:

### Option 1: Run with SQLite (Local Development) - RECOMMENDED

Use the new script that forces SQLite usage:

```bash
./run_local.sh
```

Or manually:

```bash
source venv/bin/activate
export USE_SQLITE=true
python3 app.py
```

### Option 2: Use Supabase

If you want to use Supabase, make sure your `.env` file has the correct database URL and the database is accessible. Then run:

```bash
./run.sh
```

## Accessing the Application

Once running, visit:
- **Local**: http://127.0.0.1:10000
- **Network**: http://192.168.8.251:10000 (accessible from other devices on your network)

## What Changed

The `app.py` file now checks for a `USE_SQLITE` environment variable. When set to `true`, it will use the local SQLite database (`contacts.db`) instead of trying to connect to Supabase.

## Database Files

- **SQLite**: Data is stored in `instance/contacts.db`
- **Supabase**: Data is stored remotely (when configured properly)

## Troubleshooting

If you still have issues:

1. Make sure the virtual environment is activated:
   ```bash
   source venv/bin/activate
   ```

2. Check that all dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```

3. Make sure port 10000 is not already in use:
   ```bash
   lsof -i :10000
   ```

4. Check the `.env` file (if you want to use Supabase, ensure the URL is correct)

