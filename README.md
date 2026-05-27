
# Edgar Perez

# Intro to Cybersecurity

# Fall 2025

# Secure Course Portal

This is a small web portal I made to practice Role-Based Access Control (RBAC), secure file uploads, and Linux file permissions. It simulates a simple course site with different permissions for faculty, students, and guests.

## Quick Start (2 Minutes)

```bash
cd "/Users/edgarperez/Downloads/PROJECTS/securecourse_perez"
python3 -m venv .venv_demo
.venv_demo/bin/python -m pip install --upgrade pip flask
.venv_demo/bin/python -m unittest -v
.venv_demo/bin/python app.py
```

Open: `http://127.0.0.1:5000`

## What This Project Does

### Role-Based Access

* Faculty: upload materials/assignments/public files, view all student submissions
* Students: view materials/assignments and upload submissions
* Guests: only see public files

### Secure File Handling

* Sanitized filenames
* Upload restrictions based on user role
* Uses Linux permissions + group ownership + sticky bit

Basically, users can only do what they’re supposed to do, both in the Flask app and on the actual file system.

## Project Structure

```
securecourse/
├── app.py               # Flask app
├── users.py             # Mock user “database”
├── setup_permissions.sh # Script that sets up all Linux groups + permissions
├── templates/           
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── upload.html
│   └── files.html
├── uploads/             
│   ├── materials/       # Faculty R/W, Students R
│   ├── assignments/     # Faculty R/W, Students R
│   ├── submissions/     # Students W, Faculty R
│   └── public/          # Anyone can read
└── README.md
```

## Getting Started

### 1. Requirements

* Python 3
* Flask (`pip install flask`)
* Linux/macOS terminal
* Apache2 (optional for deployment)

### 2. Installing & Setting Up

Open a terminal and navigate to the project folder:

```bash
cd /path/to/securecourse
```

Install Flask:

```bash
pip install flask
```

Set the Linux permissions (important):

```bash
sudo bash setup_permissions.sh
```

This script:

* creates the upload directories
* sets group ownership
* applies chmod (775, 770, sticky bit, etc.)

### 3. Run the App (Local / Dev)

```bash
.venv_demo/bin/python app.py
```

Then visit:
`http://127.0.0.1:5000`



## Verification Commands

Run tests:

```bash
.venv_demo/bin/python -m unittest -v
```

Check app is reachable:

```bash
curl -I http://127.0.0.1:5000/login
curl -I http://127.0.0.1:5000/
```

Expected:

* `/login` returns `200`
* `/` redirects (`302`) to `/login` when not authenticated

## Demo Flow (5-10 Minutes)

1. Login as `faculty1`, show dashboard, upload to `materials` or `assignments`.
2. Open submissions list as faculty and explain faculty-only visibility.
3. Logout and login as `student1`, show student can upload only to `submissions`.
4. Attempt student access to `/files/submissions` and show access denied.
5. Logout and login as `guest1`, show guest access is limited to public files.
6. Close by explaining app-level RBAC + filesystem permissions as defense in depth.

## Apache Setup (Optional Production Deploy)

If you want to deploy on Apache + mod_wsgi:

1. Install packages:

   ```bash
   sudo apt-get update
   sudo apt-get install apache2 libapache2-mod-wsgi-py3
   ```

2. Create `securecourse.wsgi`:

   ```python
   import sys
   sys.path.insert(0, '/var/www/securecourse')
   from app import app as application
   ```

3. Add a VirtualHost config
   (save to `/etc/apache2/sites-available/securecourse.conf`):

   ```apache
   <VirtualHost *:80>
       ServerName securecourse.local
       DocumentRoot /var/www/securecourse

       WSGIDaemonProcess securecourse user=www-data group=www-data threads=5
       WSGIScriptAlias / /var/www/securecourse/securecourse.wsgi

       <Directory /var/www/securecourse>
           WSGIProcessGroup securecourse
           WSGIApplicationGroup %{GLOBAL}
           Order deny,allow
           Allow from all
       </Directory>

       ErrorLog ${APACHE_LOG_DIR}/error.log
       CustomLog ${APACHE_LOG_DIR}/access.log combined
   </VirtualHost>
   ```

4. Enable the site and restart Apache:

   ```bash
   sudo a2ensite securecourse
   sudo systemctl restart apache2
   ```



## How Permissions Work

### Groups

* `faculty`
* `students`

### Directory Permissions

* Materials/Assignments: `775` (Faculty RWX, Students R, Others R)
* Submissions: `770` + sticky bit

  * Students can upload but cannot delete/modify each other’s files

The sticky bit ensures student submissions stay protected even in a shared directory.



## Security Features

1. RBAC (Faculty, Student, Guest)
2. Secure Filenames via `secure_filename`
3. Least Privilege access design
4. Filesystem-level protection (Linux groups, sticky bit, chmod)

Even if the Flask app fails, the OS still enforces security.



## Known Limitations and Next Steps

Current limitations (intentional for a learning/demo project):

* Mock user store in `users.py` instead of a real database
* Demo credentials are plain text (not production-safe)
* Flask development server is used for local demo only
* Automated tests currently focus on core role access paths

Planned improvements:

* Move users/roles to a real DB and hash passwords (e.g., bcrypt/Argon2)
* Move secrets/config to environment variables and secret management
* Add negative/security tests (filename fuzzing, permission edge cases, file size checks)
* Deploy with a production WSGI stack and add structured audit logging

## Troubleshooting

* GitHub push auth uses a Personal Access Token (PAT), not your GitHub password.
* If push returns `403`, verify the authenticated account/token has write access to the target repo.
* If `.DS_Store`/`__pycache__` show up locally, clean before demo:

```bash
git restore .DS_Store __pycache__/app.cpython-314.pyc
rm -f uploads/.DS_Store
```

## Demo Login Accounts

| Role    | Username | Password    | What They Can Do                        |
| ------- | -------- | ----------- | --------------------------------------- |
| Faculty | faculty1 | password123 | Upload everything, view all submissions |
| Student | student1 | password123 | Upload submissions, view materials      |
| Student | student2 | password123 | Same as above                           |
| Guest   | guest1   | password123 | Only public files                       |
