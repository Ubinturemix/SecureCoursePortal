# Mock user database
# In a real application, this would be a database.
# Passwords should be hashed, but for this part of the project, simple strings are used as per requirements.

USERS = {
    "faculty1": {
        "password": "password123",
        "role": "Faculty",
        "name": "Dr. Smith"
    },
    "student1": {
        "password": "password123",
        "role": "Student",
        "name": "Alice Student"
    },
    "student2": {
        "password": "password123",
        "role": "Student",
        "name": "Bob Student"
    },
    "guest1": {
        "password": "password123",
        "role": "Others",
        "name": "Guest User"
    }
}
