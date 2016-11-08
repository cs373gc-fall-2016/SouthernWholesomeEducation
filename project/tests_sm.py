# pylint: disable=W0401,W0614,R0904,E1101
#!/usr/bin/env python3
# 24 * 3 tests
'''
Unit tests for models.py
'''

# -------
# imports
# -------

from unittest import main, TestCase
from models import *

# ----
# test
# ----


class Tests(TestCase):
    '''
        Unit tests for models.py
        '''

    # ----------------
    # university query
    # ----------------

    def test_university_1(self):
        '''
        Test University class
        '''
        uni = University.query.filter_by(name='University of East-West Medicine').first()
        self.assertEqual(uni.num_undergrads, 2426)

    def test_university_2(self):
        '''
        Test University class
        '''
        uni = University.query.filter_by(name='Charlotte School of Law').first()
        self.assertEqual(uni.num_undergrads, 4355)

    def test_university_3(self):
        '''
        Test University class
        '''
        uni = University.query.filter_by(name='Marinello School of Beauty-Visalia').first()
        self.assertEqual(uni.num_undergrads, 3780)

    def test_university_4(self):
        '''
        Test University class
        '''
        uni = University.query.filter_by(name='Brite Divinity School').first()
        self.assertEqual(uni.num_undergrads, 2853)

    def test_university_5(self):
        '''
        Test University class
        '''
        uni = University.query.filter_by(name='J Renee College').first()
        self.assertEqual(uni.num_undergrads, 83)



# ----
# main
# ----

if __name__ == "__main__":
    main()

