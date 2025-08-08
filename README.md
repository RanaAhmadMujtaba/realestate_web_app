# realestate_web_app
**Status:**  Work in Progress  
This project is currently under active development. Some features may be incomplete or subject to change.
A role-based real estate management web application built with Flask.  
Admins can manage users and properties; viewers can submit property listings for admin approval.

## Features

### Admin
- View, add and delete users
- View, add, approve and delete properties
- See pending submissions
- Dashboard with quick stats

### Viewer
- Submit property listings (pending admin approval)
- View approved property listings

### Security & quality
- Passwords stored as hashes (Werkzeug)
- Role-based access control and session management
- Parameterized SQL queries to prevent injection
- Centralized styles and responsive UI

## Project structure

realestate/
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── controllers/
│ └── property_controller.py
├── models/
│ └── property_model.py
├── utils/
│ └── auth_utils.py
├── static/
│ ├── css/
│ │ └── style.css
│ └── images/
├── templates/
│ ├── layout.html
│ ├── login.html
│ ├── home.html
│ ├── submit_property.html
│ ├── pending_properties.html
│ ├── all_users.html
│ ├── all_properties.html
│ ├── admin_dashboard.html
│ └── add_user.html
└── database/
└── schema.sql


## Prerequisites

- Python 3.10+ (3.11 recommended)
- MySQL or MariaDB server (if using Flask-MySQL)
- Recommended: create and use a virtual environment

## Installation

1. Clone the repository:

git clone https://github.com/RanaAhmadMujtaba/realestate_web_app.git
cd realestate_web_app

## Create and activate a virtual environment:

python -m venv venv
# Mac/Linux
source venv/bin/activate
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1
# Windows (cmd)
venv\Scripts\activate

## Install requirements 
pip install -r requirements.txt

## Configure environment / database:

Copy or create config.py (or .env) with your DB credentials and SECRET_KEY.

Ensure the database exists and run the SQL schema in database/schema.sql (or use MySQL Workbench/phpMyAdmin).

## Run the app:

python app.py

The app will be available at http://127.0.0.1:5000.

Usage
Default admin and viewer credentials — see /database/seed.sql or insert via admin UI.

Admin pages: /admin/dashboard, /admin/users, /admin/properties, /admin/pending

Login: /login

Viewer submit: /submit (or configured route)

Security notes & recommendations
Always use environment variables for secrets (do not commit SECRET_KEY or DB passwords).

Use HTTPS in production.

Use a production WSGI server (Gunicorn, uWSGI) behind a reverse proxy in production.

Regularly update dependencies and run security scans.

Contributing
Fork the repo

Create a feature branch

Commit and push

Open a Pull Request

License
This project is released under the MIT License. See the LICENSE file for details.

Contact
Author: Rana Ahmad Mujtaba
GitHUB: https://github.com/RanaAhmadMujtaba

### Notes:

If you used flask_mysqldb in your app, keep Flask-MySQLdb. If you used PyMySQL or mysql-connector-python, replace accordingly.

Pin exact versions if you want reproducible installs (e.g. Flask==2.2.5). The lines above are intentionally flexible.
