from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import socket
import dns.resolver
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode

load_dotenv()

port = int(os.getenv("PORT", 10000))

def resolve_supabase_ipv4(url):
    """
    Helper to force IPv4 resolution for Supabase URLs to avoid 'Network is unreachable'
    errors on environments that default to IPv6 (like Render/Vercel) but can't route to it.
    """
    try:
        if url and ("supabase.co" in url or "supabase.in" in url):
            parsed = urlparse(url)
            hostname = parsed.hostname
            if hostname:
                # Force IPv4 resolution using public DNS (Google/Cloudflare)
                # This bypasses local DNS issues where A records might be missing
                try:
                    resolver = dns.resolver.Resolver()
                    resolver.nameservers = ['8.8.8.8', '1.1.1.1']
                    answer = resolver.resolve(hostname, 'A')
                    if answer:
                        ip = answer[0].to_text()
                        # Add hostaddr parameter to connection string
                        query = parse_qs(parsed.query)
                        query['hostaddr'] = [ip]
                        new_query = urlencode(query, doseq=True)
                        new_url = parsed._replace(query=new_query)
                        return urlunparse(new_url)
                except Exception as dns_error:
                    print(f"DNS resolution failed with dnspython: {dns_error}")
                    # Fallback to socket.getaddrinfo if dnspython fails
                    addr_info = socket.getaddrinfo(hostname, None, socket.AF_INET)
                    if addr_info:
                        ip = addr_info[0][4][0]
                        query = parse_qs(parsed.query)
                        query['hostaddr'] = [ip]
                        new_query = urlencode(query, doseq=True)
                        new_url = parsed._replace(query=new_query)
                        return urlunparse(new_url)
    except Exception as e:
        print(f"Warning: Failed to resolve Supabase IPv4: {e}")
    return url

# Use Supabase if available, otherwise use SQLite for local development
raw_db_url = os.getenv("SUPABASE_DB_URL")
database_url = resolve_supabase_ipv4(raw_db_url) or 'sqlite:///contacts.db'

# Check if we should use SQLite instead (for local dev or if Supabase fails)
use_sqlite = os.getenv("USE_SQLITE", "false").lower() == "true"
if use_sqlite:
    database_url = 'sqlite:///contacts.db'

app = Flask(__name__, template_folder='views', static_folder='public')

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# Database maybe add more fields?
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    company = db.Column(db.String(100))
    position = db.Column(db.String(100))
    linkedin_url = db.Column(db.String(200))
    value_description = db.Column(db.Text)
    tags = db.Column(db.String(200))

@app.route('/')
def home():
    # last 5 people in Database
    try:
        stuff = Contact.query.order_by(Contact.id.desc()).limit(5).all()
        return render_template('Homepage.html', recent_contacts=stuff)
    except Exception as e:
        return f"Database error: {str(e)}", 500

@app.route('/network')
def network():
    all_contacts = Contact.query.all()
    return render_template('Network.html', contacts=all_contacts)

@app.route('/guide')
def guide():
    return render_template('Guide-on-how-to-use-it.html')

@app.route('/add-contact')
def add_contact_form():
    return render_template('add-contact.html')

@app.route('/add-contact', methods=['POST'])
def add_contact_submit():
    fname = request.form.get('first_name')
    lname = request.form.get('last_name')
    mail = request.form.get('email')
    phonenumber = request.form.get('phone')
    comp = request.form.get('company')
    pos = request.form.get('position')
    linkedin = request.form.get('linkedin_url')
    description = request.form.get('value_description')
    
    
    tag_list = request.form.getlist('tags')
    tags_str = ','.join(tag_list)
    
    # todo fix lter (should validate email maybe??
    person = Contact(
        first_name=fname,
        last_name=lname,
        email=mail,
        phone=phonenumber,
        company=comp,
        position=pos,
        linkedin_url=linkedin,
        value_description=description,
        tags=tags_str
    )
    
    db.session.add(person)
    db.session.commit()
    
    return redirect(url_for('network'))

@app.route('/edit-contact/<int:contact_id>')
def edit_contact_form(contact_id):
    person = Contact.query.get_or_404(contact_id)
    return render_template('edit-contact.html', contact=person)

@app.route('/edit-contact/<int:contact_id>', methods=['POST'])
def edit_contact_submit(contact_id):
    person = Contact.query.get_or_404(contact_id)
    
    person.first_name = request.form.get('first_name')
    person.last_name = request.form.get('last_name')
    person.email = request.form.get('email')
    person.phone = request.form.get('phone')
    person.company = request.form.get('company')
    person.position = request.form.get('position')
    person.linkedin_url = request.form.get('linkedin_url')
    person.value_description = request.form.get('value_description')
    
    
    tag_list = request.form.getlist('tags')
    person.tags = ','.join(tag_list)
    
    db.session.commit()
    
    return redirect(url_for('network'))

@app.route('/delete-contact/<int:contact_id>')
def delete_contact(contact_id):
    person = Contact.query.get_or_404(contact_id)
    
    # todo fix later ( add confirmation popup)
    db.session.delete(person)
    db.session.commit()
    
    return redirect(url_for('network'))

# Routing

@app.route('/contact/<int:id>')
def view_contact(id):

    person = Contact.query.get_or_404(id)
    return render_template('contact-detail.html', contact=person)




@app.route('/person/<int:contact_id>')
def show_person(contact_id):
    p = Contact.query.get_or_404(contact_id)
    return render_template('contact-detail.html', contact=p)





if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=port)
