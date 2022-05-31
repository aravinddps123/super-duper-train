"""sample_ tests for application"""

from django.test import SimpleTestCase

from app import calc

class Test(SimpleTestCase):
    """Test the calc module"""

    
    def test_add_number(self):
        """Test the adding the number totgether"""
        res = calc.add(5, 6)
        self.assertEqual(res, 11)

    
    def test_subtract_number(self):
        """Test the subtract the number totgether"""
        res = calc.subtract(10, 16)
        self.assertEqual(res, 6)




