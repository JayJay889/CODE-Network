# Running the Application Locally

The application now uses MongoDB (Atlas or self-hosted) for all persistence, so there is no longer any SQLite or Supabase dependency.

## 1. Prerequisites

1. Python 3.13 (see `requirements.txt`)
2. A running MongoDB instance:
   - **Recommended:** MongoDB Atlas free-tier cluster
   - **Local Dev:** `mongodb://127.0.0.1:27017/contacts_db` (start the Mongo daemon with Homebrew, Docker, etc.)

## 2. Configure Environment Variables

Create a `.env` file (or export variables in your shell) with at least:

```
MONGO_URI="your-mongodb-connection-string"
PORT=10000  # optional; defaults to 10000 locally and the value Render supplies in production
```

If you just want to run against a local MongoDB instance, you can skip `MONGO_URI` entirely—the app (and `run_local.sh`) default to `mongodb://127.0.0.1:27017/contacts_db`.

## 3. Install Dependencies

```bash
cd Project.py
source venv/bin/activate
pip install -r requirements.txt
```

## 4. Start the Application

Use the helper script (auto-sets a sensible local `MONGO_URI`):

```bash
./run_local.sh
```

Or run manually:

```bash
python3 app.py
```

## 5. Access the UI

- Local machine: http://127.0.0.1:10000
- LAN (replace with your IP): http://<your-ip>:10000

## Troubleshooting

1. **Cannot connect to MongoDB**
   - Verify `MONGO_URI` is correct and network-accessible.
   - For Atlas, allow your IP in the Network Access tab and confirm the username/password.
2. **Dependencies missing**
   - Re-run `pip install -r requirements.txt` inside the virtual env.
3. **Port already in use**
   - `lsof -i :10000` and stop the conflicting process, or set `PORT` to an open port.
4. **Auth/index errors**
   - The app auto-creates a unique index on `contacts.email`. Drop/rename any conflicting documents before restarting if duplicates exist.

