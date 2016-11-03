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
        uni = University.query.filter_by('name=University of East-West Medicine').first()
        self.assertEqual(uni.num_undergrads, 2460)

    def test_university_2(self):
        '''
        Test University class
        '''
        uni = University.query.filter_by('name=Charlotte School of Law').first()
        self.assertEqual(uni.num_undergrads, 3764)

    def test_university_3(self):
        '''
        Test University class
        '''
        uni = University.query.filter_by('name=Marinello School of Beauty-Visalia').first()
        self.assertEqual(uni.num_undergrads, 2185)

    def test_university_4(self):
        '''
        Test University class
        '''
        uni = University.query.filter_by('name=Brite Divinity School').first()
        self.assertEqual(uni.num_undergrads, 3357)

    def test_university_5(self):
        '''
        Test University class
        '''
        uni = University.query.filter_by('name=J Renee College').first()
        self.assertEqual(uni.num_undergrads, 83)

    def test_university_6(self):
        '''
        Test University class
        '''
        uni = University.query.filter_by('name=American Sentinel University').first()
        self.assertEqual(uni.num_undergrads, 1701)

    def test_university_7(self):
        '''
        Test University class
        '''
        uni = University.query.filter_by('name=Center for Natural Wellness School of Massage Therapy').first()
        self.assertEqual(uni.num_undergrads, 45)

    def test_university_8(self):
        '''
        Test University class
        '''
        uni = University.query.filter_by('name=Trenz Beauty Academy').first()
        self.assertEqual(uni.num_undergrads, 54)

    def test_university_9(self):
        '''
        Test University class
        '''
        uni = University.query.filter_by('name=SOLEX College').first()
        self.assertEqual(uni.num_undergrads, 85)

    def test_university_10(self):
        '''
        Test University class
        '''
        uni = University.query.filter_by('name=Star Career Academy-Audubon').first()
        self.assertEqual(uni.num_undergrads, 221)

    # -------------------
    # university __repr__
    # -------------------

    def test_university_repr_1(self):
        '''
        Test University __repr__
        '''
        university = University('UT', 0, 0, 0, '')
        self.assertEqual(university.__repr__(), '<University UT>')

    def test_university_repr_2(self):
        '''
        Test University __repr__
        '''
        university = University('A&M', 0, 0, 0, '')
        self.assertEqual(university.__repr__(), '<University A&M>')

    def test_university_repr_3(self):
        '''
        Test University __repr__
        '''
        university = University('Rice', 0, 0, 0, '')
        self.assertEqual(university.__repr__(), '<University Rice>')

    def test_university_repr_4(self):
        '''
        Test University __repr__
        '''
        university = University('Southwestern', 0, 0, 0, '')
        self.assertEqual(university.__repr__(), '<University Southwestern>')

    def test_university_repr_5(self):
        '''
        Test University __repr__
        '''
        university = University('MD Anderson', 0, 0, 0, '')
        self.assertEqual(university.__repr__(), '<University MD Anderson>')

    def test_university_repr_6(self):
        '''
        Test University __repr__
        '''
        university = University('UTMB', 0, 0, 0, '')
        self.assertEqual(university.__repr__(), '<University UTMB>')

    def test_university_repr_7(self):
        '''
        Test University __repr__
        '''
        university = University('McGovern Medical School', 0, 0, 0, '')
        self.assertEqual(university.__repr__(), '<University McGovern Medical School>')

    # -----------------
    # MAJORTOCITY class
    # -----------------

    def test_majortocity_1(self):
        '''
        Test MAJORTOCITY class
        '''
        mc = MAJORTOCITY.query.filter_by(city_name='Madison', major_name='Visual Performing')
        self.assertEqual(mc.num_students, 14)

    def test_majortocity_2(self):
        '''
        Test MAJORTOCITY class
        '''
        mc = MAJORTOCITY.query.filter_by(city_name='Pensacola', major_name='Construction')
        self.assertEqual(mc.num_students, 7)

    def test_majortocity_3(self):
        '''
        Test MAJORTOCITY class
        '''
        mc = MAJORTOCITY.query.filter_by(city_name='Warner Robins', major_name='Health')
        self.assertEqual(mc.num_students, 1124)

    def test_majortocity_4(self):
        '''
        Test MAJORTOCITY class
        '''
        mc = MAJORTOCITY.query.filter_by(city_name='New York', major_name='Health')
        self.assertEqual(mc.num_students, 1221)

    def test_majortocity_5(self):
        '''
        Test MAJORTOCITY class
        '''
        mc = MAJORTOCITY.query.filter_by(city_name='Bethlehem', major_name='Construction')
        self.assertEqual(mc.num_students, 73)

    def test_majortocity_6(self):
        '''
        Test MAJORTOCITY class
        '''
        mc = MAJORTOCITY.query.filter_by(city_name='Oklahoma City', major_name='Computer')
        self.assertEqual(mc.num_students, 8)

    def test_majortocity_7(self):
        '''
        Test MAJORTOCITY class
        '''
        mc = MAJORTOCITY.query.filter_by(city_name='Phoenix', major_name='Health')
        self.assertEqual(mc.num_students, 542)

    # -------------
    # city __repr__
    # -------------

    def test_city_repr_1(self):
        '''
        Test City __repr__
        '''
        city = City('Austin')
        self.assertEqual(city.__repr__(), '<City Austin>')

    def test_city_repr_2(self):
        '''
        Test City __repr__
        '''
        city = City('Salt Lake City')
        self.assertEqual(city.__repr__(), '<City Salt Lake City>')

    def test_city_repr_3(self):
        '''
        Test City __repr__
        '''
        city = City('New York')
        self.assertEqual(city.__repr__(), '<City New York>')

        # # -----------
        # # major class
        # # -----------



        # # -------------
        # # major __repr__
        # # -------------

    def test_major_repr_1(self):
        '''
        Test Major __repr__
        '''
        major = Major('Economics')
        self.assertEqual(major.__repr__(), '<Major Economics>')

    def test_major_repr_2(self):
        '''
        Test Major __repr__
        '''
        major = Major('Engineering')
        self.assertEqual(major.__repr__(), '<Major Engineering>')

    def test_major_repr_3(self):
        '''
        Test Major __repr__
        '''
        major = Major('Business')
        self.assertEqual(major.__repr__(), '<Major Business>')

        # # ---------------
        # # ethnicity class
        # # ---------------

    

# ----
# main
# ----

if __name__ == "__main__":
    main()
