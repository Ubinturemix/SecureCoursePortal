# Secure Course Portal - Walkthrough

## Overview
This project implements a secure web portal with Role-Based Access Control (RBAC) for a course environment. It includes Faculty, Student, and Guest roles with specific permissions for file uploads and viewing.

## Features Implemented
1.  **Authentication**: Login system with session management.
2.  **RBAC**:
    - **Faculty**: Full access to materials, assignments, and submissions.
    - **Student**: Read access to materials/assignments; Write access to submissions.
    - **Others**: Read access to public files only.
3.  **Secure File Handling**:
    - Uploads are segregated by category.
    - Filenames are sanitized.
    - Linux permissions (via `setup_permissions.sh`) enforce security at the OS level.

## Verification Results

### Automated Tests
*Note: Automated tests require `flask` to be installed.*
- `test_app.py` is provided to verify:
    - Login/Logout functionality.
    - Role-based access denial (e.g., Students accessing submissions view).
    - Public access controls.

### Manual Verification Steps
1.  **Setup**:
    ```bash
    cd /Users/edgarperez/Desktop/securecourse
    sudo bash setup_permissions.sh
    pip install flask
    python3 app.py
    ```

2.  **Faculty Test**:
    - Login as `faculty1` / `password123`.
    - Upload a file to "Materials".
    - Verify it appears in the list.
    - Check "Submissions" (should be empty initially).

3.  **Student Test**:
    - Login as `student1` / `password123`.
    - Check "Materials" (should see the file uploaded by faculty).
    - Upload a file to "Submissions".
    - Try to view "Submissions" list (should be denied/redirected).

4.  **Guest Test**:
    - Login as `guest1` / `password123`.
    - Verify only "Public" resources are accessible.

## Project Structure
- `app.py`: Main application logic.
- `users.py`: Mock user database.
- `templates/`: HTML interfaces for Login, Dashboard, Upload, and File Listing.
- `setup_permissions.sh`: Script to configure Linux groups and permissions.
