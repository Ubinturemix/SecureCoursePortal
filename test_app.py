import unittest
from app import app

class SecureCourseTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        rv = self.login('faculty1', 'password123')
        self.assertIn(b'Dashboard', rv.data)
        self.assertIn(b'Faculty', rv.data)
        rv = self.logout()
        self.assertIn(b'Login', rv.data)

    def test_faculty_access(self):
        self.login('faculty1', 'password123')
        rv = self.app.get('/files/submissions')
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Submissions', rv.data)

    def test_student_access_denied(self):
        self.login('student1', 'password123')
        rv = self.app.get('/files/submissions', follow_redirects=True)
        # Should redirect to dashboard with flash message or show access denied
        self.assertIn(b'Access denied', rv.data)

    def test_guest_access(self):
        self.login('guest1', 'password123')
        rv = self.app.get('/files/public')
        self.assertEqual(rv.status_code, 200)
        rv = self.app.get('/files/materials', follow_redirects=True)
        self.assertIn(b'Access denied', rv.data)

if __name__ == '__main__':
    unittest.main()
