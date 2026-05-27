import os
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, flash
from users import USERS
import werkzeug.utils

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_session_management' # Change this in production!

# Configuration
# Use env override when provided; default to repo-local uploads for portability.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', os.path.join(BASE_DIR, 'uploads'))
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'py', 'zip'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload directories exist (though setup_permissions.sh handles this too)
for subfolder in ['materials', 'assignments', 'submissions', 'public']:
    os.makedirs(os.path.join(UPLOAD_FOLDER, subfolder), exist_ok=True)

def get_role():
    return session.get('role')

def is_logged_in():
    return 'username' in session

@app.route('/')
def index():
    if is_logged_in():
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in USERS and USERS[username]['password'] == password:
            session['username'] = username
            session['role'] = USERS[username]['role']
            session['name'] = USERS[username]['name']
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if not is_logged_in():
        return redirect(url_for('login'))
    return render_template('dashboard.html', user=session)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if not is_logged_in():
        return redirect(url_for('login'))
    
    role = session.get('role')
    
    # Determine allowed upload categories based on role
    allowed_categories = []
    if role == 'Faculty':
        allowed_categories = ['materials', 'assignments', 'public']
    elif role == 'Student':
        allowed_categories = ['submissions']
    else:
        flash("You do not have permission to upload files.")
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        category = request.form.get('category')
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
            
        if category not in allowed_categories:
            flash('Invalid category for your role.')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = werkzeug.utils.secure_filename(file.filename)
            # Prepend username to filename for submissions to avoid collisions/identify student
            if category == 'submissions':
                filename = f"{session['username']}_{filename}"
                
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], category, filename))
            flash(f'File uploaded successfully to {category}!')
            return redirect(url_for('dashboard'))
        else:
            flash('File type not allowed.')

    return render_template('upload.html', categories=allowed_categories)

@app.route('/files/<file_type>')
def list_files(file_type):
    if not is_logged_in():
        return redirect(url_for('login'))
    
    role = session.get('role')
    
    # Access Control Logic
    # Public: Everyone
    # Materials/Assignments: Faculty, Student
    # Submissions: Faculty (all), Student (own only? or none? Prompt says "Student View materials/assignments, submit assignments". Usually students can't see others' submissions.)
    
    if file_type == 'public':
        pass # Everyone allowed
    elif file_type in ['materials', 'assignments']:
        if role not in ['Faculty', 'Student']:
            flash('Access denied.')
            return redirect(url_for('dashboard'))
    elif file_type == 'submissions':
        if role != 'Faculty':
            flash('Access denied. Only Faculty can view all submissions.')
            return redirect(url_for('dashboard'))
    else:
        flash('Invalid file type.')
        return redirect(url_for('dashboard'))

    directory = os.path.join(app.config['UPLOAD_FOLDER'], file_type)
    try:
        files = os.listdir(directory)
        # Filter out hidden files
        files = [f for f in files if not f.startswith('.')]
    except FileNotFoundError:
        files = []
        
    show_upload = False
    if role == 'Faculty' and file_type in ['materials', 'assignments', 'public']:
        show_upload = True
    if role == 'Student' and file_type == 'submissions':
        show_upload = True # Though usually they upload via the main upload button, this context flag is for the view

    return render_template('files.html', files=files, file_type=file_type, show_upload=show_upload)

@app.route('/download/<file_type>/<filename>')
def download_file(file_type, filename):
    if not is_logged_in():
        return redirect(url_for('login'))
        
    role = session.get('role')
    
    # Re-verify access rights before serving file
    if file_type == 'public':
        pass
    elif file_type in ['materials', 'assignments']:
        if role not in ['Faculty', 'Student']:
            return "Access Denied", 403
    elif file_type == 'submissions':
        if role != 'Faculty':
            return "Access Denied", 403
    else:
        return "Invalid type", 400

    # Secure filename check again just in case
    filename = werkzeug.utils.secure_filename(filename)
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], file_type), filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
