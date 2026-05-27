#!/bin/bash

# Project directory
PROJECT_DIR="/Users/edgarperez/Desktop/securecourse"
UPLOADS_DIR="$PROJECT_DIR/uploads"

echo "Setting up directories and permissions for Secure Course Portal..."

# Create directories if they don't exist
mkdir -p "$UPLOADS_DIR/materials"
mkdir -p "$UPLOADS_DIR/assignments"
mkdir -p "$UPLOADS_DIR/submissions"
mkdir -p "$UPLOADS_DIR/public"

# Note: On macOS, creating groups programmatically can be different than Linux.
# This script assumes a standard Linux environment as per the prompt requirements (sudo groupadd).
# For macOS local development, we might skip actual group creation if it fails, 
# or the user might need to do it manually via System Preferences or dscl.
# I will include the standard Linux commands but wrapped in a check or just echo them if on Mac 
# where sudo might be tricky for the agent to handle interactively.

# However, the prompt asked for these specific commands.
# I will write them out. The user will run this script with sudo.

# 1. Create Groups (Ignore if they exist)
# || true prevents script exit if group exists
groupadd faculty 2>/dev/null || true
groupadd students 2>/dev/null || true

echo "Groups 'faculty' and 'students' ensured."

# 2. Set Ownership and Permissions

# General Web Server User (often www-data on Linux, _www on macOS)
# We'll try to detect or default to the current user for local dev if www-data doesn't exist
WEB_USER="www-data"
if ! id "$WEB_USER" &>/dev/null; then
    WEB_USER=$(whoami)
    echo "User 'www-data' not found, using current user '$WEB_USER' for ownership."
fi

# Change ownership
# Materials: Faculty (rw), Students (r), Others (public only)
# We set group to faculty for materials
chown -R $WEB_USER:faculty "$UPLOADS_DIR/materials"
chown -R $WEB_USER:faculty "$UPLOADS_DIR/assignments"
chown -R $WEB_USER:faculty "$UPLOADS_DIR/public"

# Submissions: Students need to write here. Faculty needs to read.
chown -R $WEB_USER:students "$UPLOADS_DIR/submissions"

# 3. Set Permissions (chmod)

# Materials/Assignments: Faculty rw, Group(faculty) rw, Others r (or restricted?)
# Requirement: Faculty upload, Student view.
# So: Owner(web) rw, Group(faculty) rw, Others(students?) r
# Actually, if we want Students to view, they need read access.
# If we use groups strictly:
# Materials: Group=faculty (rw), Others=read? No, students are in students group.
# We might need to use ACLs for complex multi-group, OR just rely on the application logic 
# and keep the folders readable by the web server user.
# The PROMPT specifically asked for:
# sudo chown -R www-data:faculty .../materials
# sudo chown -R www-data:students .../submissions
# sudo chmod 770 .../submissions
# sudo chmod +t .../submissions

# Let's follow the prompt's example for permissions.

# Materials & Assignments
# Owned by faculty group. 
# If we want students to read via the web app, the web app user ($WEB_USER) needs read access.
# $WEB_USER is the owner, so that's fine.
chmod -R 775 "$UPLOADS_DIR/materials"
chmod -R 775 "$UPLOADS_DIR/assignments"
chmod -R 775 "$UPLOADS_DIR/public"

# Submissions
# Owned by students group.
# chmod 770 means: Owner(web) rwx, Group(students) rwx, Others ---
# Sticky bit (+t) ensures users can only delete their own files (mostly relevant for shared directories).
chmod -R 770 "$UPLOADS_DIR/submissions"
chmod +t "$UPLOADS_DIR/submissions"

echo "Permissions set."
echo "  - Materials/Assignments/Public: 775 (Owner/Group RWX, Others RX)"
echo "  - Submissions: 770 + Sticky Bit (Owner/Group RWX, Others None)"

ls -ld "$UPLOADS_DIR/"*
