# app.py
from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__, static_url_path='/static')

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://flask_user:flask_password@db:5432/flask_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120), nullable=True)

    def __repr__(self):
        return f"<Item {self.name}>"

@app.route('/')
def index():
    items = Item.query.all()
    return render_template('index.html', items=items)

@app.route('/item/<int:id>')
def get_item(id):
    item = Item.query.get_or_404(id)
    return render_template('item.html', item=item)

@app.route('/create', methods=['GET', 'POST'])
def create_item():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        new_item = Item(name=name, description=description)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('form.html', form_title="Create Item", item=None)

@app.route('/item/<int:id>/edit', methods=['GET', 'POST'])
def edit_item(id):
    item = Item.query.get_or_404(id)
    if request.method == 'POST':
        item.name = request.form['name']
        item.description = request.form['description']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('form.html', form_title="Edit Item", item=item)

@app.route('/item/<int:id>/delete', methods=['POST'])
def delete_item(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/file/<filename>')
def get_file(filename):
    UPLOAD_FOLDER = '/data'
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/reinitialize_db', methods=['POST'])
def reinitialize_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        # Read initial data from sample.txt and populate the database
        with open('/data/sample.txt', 'r') as file:
            for line in file:
                name, description = line.strip().split(',')
                item = Item(name=name, description=description)
                db.session.add(item)
            db.session.commit()
    return "Database reinitialized with sample data.", 200
@app.route('/people')
def people():
    return render_template('people.html')

def initialize_database():
    with app.app_context():
        db.create_all()
        # Read initial data from sample.txt and populate the database
        if not Item.query.first():  # Only add sample data if the table is empty
            with open('/data/sample.txt', 'r') as file:
                for line in file:
                    name, description = line.strip().split(',')
                    item = Item(name=name, description=description)
                    db.session.add(item)
                db.session.commit()
            print("Database initialized and sample data added.")

if __name__ == '__main__':
    initialize_database()  # Initialize the database on startup
    app.run(host='0.0.0.0', port=5000, debug=True)
