from flask import Blueprint, render_template, request, redirect, session, flash, abort
from models.property_model import *
from utils.auth_utils import login_required, is_admin, is_viewer, validate_login
from werkzeug.security import generate_password_hash

property_blueprint = Blueprint('property', __name__)

# Home Page
# Home Page with Filters + Sorting
@property_blueprint.route('/', methods=['GET'])
def home():
    filters = {
        'location': request.args.get('location', ''),
        'min_price': request.args.get('min_price', ''),
        'max_price': request.args.get('max_price', ''),
        'type': request.args.get('type', ''),
        'sort': request.args.get('sort', 'newest')  # default sort
    }
    props = get_filtered_properties(filters)
    return render_template("home.html", properties=props, filters=filters)

# Login
@property_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = get_all_users()
        user = validate_login(username, password, users)
        if user:
            session['logged_in'] = True
            session['username'] = user['username']
            session['role'] = user['role']
            return redirect('/')
        flash("Invalid credentials.")
    return render_template("login.html")

# Logout
@property_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# Viewer — Submit Property
@property_blueprint.route('/submit', methods=['GET', 'POST'])
@login_required
def submit_property():
    if not is_viewer():
        abort(403)
    if request.method == 'POST':
        data = {
            'title': request.form['title'],
            'location': request.form['location'],
            'price': request.form['price'],
            'type': request.form['type'],
            'description': request.form['description'],
            'image_url': request.form['image_url'],
            'submitted_by': session.get('username')
        }
        submit_pending_property(data)
        flash("Property submitted for admin approval.")
        return redirect('/')
    return render_template("submit_property.html")

# Admin — View Pending Properties
@property_blueprint.route('/admin/pending')
@login_required
def pending():
    if not is_admin():
        abort(403)
    props = get_pending_properties()
    return render_template("pending_properties.html", pending=props)


@property_blueprint.route('/admin/dashboard')
def admin_dashboard():
    if session.get('role') != 'admin':
        abort(403)

    users = get_all_users()
    properties = get_all_properties()
    pending = get_all_pending_properties()

    return render_template('admin_dashboard.html', users=users, properties=properties, pending=pending)


# Admin — Approve Property
@property_blueprint.route('/admin/approve/<int:id>')
@login_required
def approve(id):
    if not is_admin():
        abort(403)
    approve_property(id)
    flash("Property approved.")
    return redirect('/admin/pending')

# Admin — Delete Property (Pending Only)
@property_blueprint.route('/admin/delete/<int:id>')
@login_required
def delete(id):
    if not is_admin():
        abort(403)
    delete_property(id)
    flash("Property deleted.")
    return redirect('/admin/pending')

# Admin — Add User
@property_blueprint.route('/admin/add-user', methods=['GET', 'POST'])
@login_required
def add_user():
    if not is_admin():
        abort(403)
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        role = request.form['role']
        add_new_user(username, password, role)
        flash("User added successfully.")
        return redirect('/admin/users')
    return render_template("add_user.html")

# ✅ NEW: Admin — View All Users
@property_blueprint.route('/admin/users')
@login_required
def view_users():
    if not is_admin():
        abort(403)
    users = get_all_users()
    return render_template("all_users.html", users=users)

# ✅ NEW: Admin — Delete User
@property_blueprint.route('/admin/delete-user/<int:id>')
@login_required
def delete_user(id):
    if not is_admin():
        abort(403)
    delete_user_by_id(id)
    flash("User deleted.")
    return redirect('/admin/users')

# ✅ NEW: Admin — View All Properties (All Status)
@property_blueprint.route('/admin/properties')
@login_required
def view_all_properties():
    if not is_admin():
        abort(403)
    props = get_all_properties()
    return render_template("all_properties.html", properties=props)

# ✅ NEW: Admin — Delete Any Property (Approved/Pending)
@property_blueprint.route('/admin/delete-property/<int:id>')
@login_required
def delete_any_property(id):
    if not is_admin():
        abort(403)
    delete_property(id)
    flash("Property deleted.")
    return redirect('/admin/properties')

# ✅ NEW: Admin — Add Property Directly
@property_blueprint.route('/admin/add-property', methods=['GET', 'POST'])
@login_required
def add_property_direct():
    if not is_admin():
        abort(403)
    if request.method == 'POST':
        data = {
            'title': request.form['title'],
            'location': request.form['location'],
            'price': request.form['price'],
            'type': request.form['type'],
            'description': request.form['description'],
            'image_url': request.form['image_url'],
            'submitted_by': session.get('username')
        }
        add_property(data)
        flash("Property added directly.")
        return redirect('/')
    return render_template("admin_add_property.html")


@property_blueprint.route('/contact', methods=['GET'])
def contact():
    props = get_approved_properties()
    return render_template("contact.html", properties=props)

# Property Details Page
@property_blueprint.route('/property/<int:id>')
def property_details(id):
    from models.property_model import get_property_by_id
    prop = get_property_by_id(id)
    if not prop:
        abort(404)
    return render_template("property_details.html", property=prop)
    
@property_blueprint.route('/about', methods=['GET'])
def about():
    props = get_approved_properties()
    return render_template("about.html", properties=props)