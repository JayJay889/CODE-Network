from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__, template_folder='views', static_folder='public')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
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
    stuff = Contact.query.order_by(Contact.id.desc()).limit(5).all()
    return render_template('Homepage.html', recent_contacts=stuff)

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
    app.run(debug=True, port=8080)
