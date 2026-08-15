import unittest
from app import app, db, Students

class StudentAppTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_01_show_all_screen(self):
        """Test GET / renders table with Phone Number column, existing student records, and User ID footnote."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn('nmonfort577', html)
        self.assertIn('User ID:', html)
        self.assertIn('<th>Phone Number</th>', html)
        self.assertIn('Hassan Ali', html)
        self.assertIn('555-754-2824', html)
        self.assertIn('Anisa Hussen Salad', html)
        self.assertIn('555-125-5506', html)

    def test_02_new_student_screen_get(self):
        """Test GET /new renders form with Phone Number input field and User ID footnote."""
        response = self.client.get('/new')
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn('nmonfort577', html)
        self.assertIn('User ID:', html)
        self.assertIn('Phone Number:', html)
        self.assertIn('name="phone"', html)

    def test_03_create_new_student_post(self):
        """Test POST /new successfully adds a new student with phone number."""
        payload = {
            'name': 'Amina Nur',
            'city': 'Mogadishu',
            'addr': 'Waberi',
            'pin': '54321',
            'phone': '555-890-1234'
        }
        response = self.client.post('/new', data=payload, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn('Record was successfully added', html)
        self.assertIn('Amina Nur', html)
        self.assertIn('555-890-1234', html)

        # Direct DB verification
        with app.app_context():
            student = Students.query.filter_by(name='Amina Nur').first()
            self.assertIsNotNone(student)
            self.assertEqual(student.phone, '555-890-1234')
            self.assertEqual(student.city, 'Mogadishu')
            self.assertEqual(student.addr, 'Waberi')
            self.assertEqual(student.pin, '54321')

    def test_04_validation_error(self):
        """Test POST /new with missing required fields shows flash error."""
        payload = {
            'name': '',
            'city': 'Mogadishu',
            'addr': '',
            'pin': '12345',
            'phone': '555-000-1111'
        }
        response = self.client.post('/new', data=payload, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn('Please enter all the fields', html)

if __name__ == '__main__':
    unittest.main()
