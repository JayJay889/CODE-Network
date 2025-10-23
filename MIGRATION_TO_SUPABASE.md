# Migration from SQLite to Supabase

This guide will help you complete the migration from SQLite to Supabase PostgreSQL.

## What Changed

1. **Database**: SQLite → Supabase (PostgreSQL)
2. **New Dependencies**: Added `psycopg2-binary` and `python-dotenv`
3. **Configuration**: Database credentials now stored in `.env` file
4. **Connection String**: Updated from `sqlite:///contacts.db` to PostgreSQL URI

## Step-by-Step Migration

### Step 1: Create a Supabase Project

1. Visit [supabase.com](https://supabase.com)
2. Sign up or log in
3. Click "New Project"
4. Fill in:
   - **Name**: CODE Network (or your preferred name)
   - **Database Password**: Create a strong password (SAVE THIS!)
   - **Region**: Choose closest to you
5. Click "Create new project" and wait ~2 minutes for setup

### Step 2: Get Your Database Connection String

1. In your Supabase dashboard, go to **Project Settings** (gear icon)
2. Click **Database** in the left sidebar
3. Scroll to **Connection String** section
4. Select **URI** tab
5. Copy the connection string (it looks like this):
   ```
   postgresql://postgres.xxxxxxxxxxxxx:[YOUR-PASSWORD]@aws-0-us-west-1.pooler.supabase.com:5432/postgres
   ```
6. **Important**: Replace `[YOUR-PASSWORD]` with the database password you created in Step 1

### Step 3: Create Your .env File

1. In the `Project.py` folder, create a file named `.env` (no extension)
2. Add this line (replace with your actual connection string):
   ```
   SUPABASE_DB_URL=postgresql://postgres.xxxxxxxxxxxxx:your-password@aws-0-us-west-1.pooler.supabase.com:5432/postgres
   ```
3. Save the file

**Security Note**: The `.env` file is already added to `.gitignore` so your credentials won't be committed to git.

### Step 4: Install New Dependencies

```bash
cd Project.py
source venv/bin/activate
pip install -r requirements.txt
```

This will install:
- `psycopg2-binary` - PostgreSQL adapter for Python
- `python-dotenv` - Environment variable management

### Step 5: Run Your App

```bash
python3 app.py
```

The app will:
1. Connect to Supabase
2. Automatically create the `contact` table
3. Start the server on http://127.0.0.1:8080

### Step 6: Verify in Supabase

1. Go back to your Supabase dashboard
2. Click **Table Editor** in the left sidebar
3. You should see a `contact` table with all your columns:
   - id
   - first_name
   - last_name
   - email
   - phone
   - company
   - position
   - linkedin_url
   - value_description

## Migrating Existing Data (Optional)

If you have existing contacts in your SQLite database that you want to migrate:

### Option 1: Manual Entry
Just re-add your contacts through the web interface.

### Option 2: Export/Import via Python
Create a migration script `migrate_data.py`:

```python
import sqlite3
from app import app, db, Contact

# Read from SQLite
conn = sqlite3.connect('contacts.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM contact')
old_contacts = cursor.fetchall()
conn.close()

# Write to Supabase
with app.app_context():
    for contact in old_contacts:
        new_contact = Contact(
            first_name=contact[1],
            last_name=contact[2],
            email=contact[3],
            phone=contact[4],
            company=contact[5],
            position=contact[6],
            linkedin_url=contact[7],
            value_description=contact[8]
        )
        db.session.add(new_contact)
    db.session.commit()
    print(f"Migrated {len(old_contacts)} contacts!")
```

Run it once: `python3 migrate_data.py`

## Troubleshooting

### Error: "No module named 'psycopg2'"
**Solution**: Run `pip install -r requirements.txt`

### Error: "None" is not a valid database URL
**Solution**: Check that your `.env` file exists and has the correct `SUPABASE_DB_URL` variable

### Error: Connection refused
**Solution**: 
- Verify your connection string is correct
- Check that you replaced `[YOUR-PASSWORD]` with your actual password
- Make sure your Supabase project is fully initialized

### Error: Password authentication failed
**Solution**: 
- Double-check your database password
- Try resetting your database password in Supabase Project Settings > Database

## Benefits of Supabase

✅ **Cloud-hosted** - No local database files  
✅ **Scalable** - Handles more users and data  
✅ **Backups** - Automatic daily backups  
✅ **Real-time** - Can add real-time features later  
✅ **Dashboard** - View/edit data in Supabase UI  
✅ **Free tier** - 500MB database, plenty for contacts  

## Need Help?

- [Supabase Documentation](https://supabase.com/docs)
- [Supabase Discord](https://discord.supabase.com)
- Check the logs in your terminal for error messages

---

That's it! Your app is now using Supabase! 🎉

