
# Edgar Perez

# Intro to Cybersecurity

# Fall 2025

# Secure Course Portal

This is a small web portal I made to practice Role-Based Access Control (RBAC), secure file uploads, and Linux file permissions. It simulates a simple course site with different permissions for faculty, students, and guests.

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
python3 app.py
```

Then visit:
`http://127.0.0.1:5000`



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



## Demo Login Accounts

| Role    | Username | Password    | What They Can Do                        |
| ------- | -------- | ----------- | --------------------------------------- |
| Faculty | faculty1 | password123 | Upload everything, view all submissions |
| Student | student1 | password123 | Upload submissions, view materials      |
| Student | student2 | password123 | Same as above                           |
| Guest   | guest1   | password123 | Only public files                       |
