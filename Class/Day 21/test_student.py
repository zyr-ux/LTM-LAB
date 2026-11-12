import unittest
from unittest import mock
import student

def setUpModule():
    print('This is module level')

class TestStudent(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('This is class level')

    def setUp(self):
        self.sid = student.Student(1,'Sid',23)

    def test_student_id(self):
        self.assertEqual(2,self.sid.id,'id not equal')

    def test_student_name(self):
        assert 'Sid' == self.sid.name

    def test_student_age(self):
        assert 23 == self.sid.age

    # def tearDown(self):
    #     print('Ran after each test method')

    def test_student_age_negative(self):
        with self.assertRaises(student.AgeException):
            student.Student(1,'Sid',-22)

    def test_student_password(self):
        student.random.randint = mock.Mock()
        student.random.randint.return_value = 1
        hp = student.Student(1,'hp',25)
        self.assertEqual(hp.get_password(),5253)

# if __name__ == '__main__':
#     unittest.main(verbosity=2)
