---
title: CODE Network App
emoji: 🌐
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
app_port: 7860
---

# CODE Network

A contact management web application for the CODE community. Built with Python Flask and SQLite.

## Features

✨ **Full CRUD Operations**

- ➕ Add new contacts with detailed information
- 📋 View all contacts in a searchable directory
- ✏️ Edit existing contact information
- 🗑️ Delete contacts with confirmation

🏷️ **Tags System**

- Categorize contacts (Speaker, Mentor, Sponsor, Alumni, Partner)
- Multiple tags per contact
- Color-coded tag badges

📱 **Responsive Design**

- Mobile-friendly layout
- Adapts to phone, tablet, and desktop screens
- CSS Grid and Flexbox layouts

🎯 **Additional Features**

- Recent contacts display on homepage
- LinkedIn and email links
- Professional, clean UI

## Quick Start

### 1. Install dependencies

```bash
cd Project.py
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Run the app

```bash
bash run.sh
```

Or manually:

```bash
python3 app.py
```

### 3. Open in browser

Visit: http://localhost:8080

The SQLite database will be created automatically on first run.

## Project Structure

```
Project.py/
├── app.py              # Main Flask application
├── views/              # HTML templates
│   ├── Homepage.html
│   ├── Network.html
│   ├── add-contact.html
│   └── edit-contact.html
├── public/
│   ├── css/style.css   # Responsive styling
│   └── images/         # Image assets
├── contacts.db         # SQLite database (auto-generated)
├── requirements.txt    # Python dependencies
└── run.sh             # Startup script
```

## Technologies Used

**Backend:**

- Python 3.13
- Flask 3.1.2 (Web framework)
- SQLAlchemy 2.0.44 (ORM)
- SQLite (Database)

**Frontend:**

- HTML5
- CSS3 (Grid, Flexbox, Media Queries)
- Jinja2 (Template engine)

**Development:**

- python-dotenv (Environment variables)
- Virtual environment (venv)

## Database Schema

```python
Contact:
  - id (Primary Key)
  - first_name (String, required)
  - last_name (String, required)
  - email (String, unique, required)
  - phone (String)
  - company (String)
  - position (String)
  - linkedin_url (String)
  - value_description (Text)
  - tags (String, comma-separated)
```

## Usage

1. **Homepage** - Overview with recent contacts
2. **View Network** - Browse all contacts with filtering
3. **Add Contact** - Form to create new contacts
4. **Edit Contact** - Update existing contact information
5. **Delete Contact** - Remove contacts (with confirmation)

## Development Notes

- Uses SQLite for simplicity (easy setup, no external database needed)
- Responsive breakpoints: 600px (mobile), 768px (tablet), 1024px+ (desktop)
- Tags stored as comma-separated strings for simplicity
- Auto-creates database tables on first run

## Future Improvements

- Search functionality
- Pagination for large datasets
- User authentication (Flask-Login)
- Export contacts to CSV
- Database migrations (Flask-Migrate)
- API endpoints for mobile app

---

Built for the CODE community 🚀
