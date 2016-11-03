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
        self.assertEqual(uni.num_undergrads, 4396)

    def test_university_3(self):
        '''
        Test University class
        '''
        uni = University.query.filter_by(name='Marinello School of Beauty-Visalia').first()
        self.assertEqual(uni.num_undergrads, 599)

    def test_university_4(self):
        '''
        Test University class
        '''
        uni = University.query.filter_by(name='Brite Divinity School').first()
        self.assertEqual(uni.num_undergrads, 1110)

    def test_university_5(self):
        '''
        Test University class
        '''
        uni = University.query.filter_by(name='J Renee College').first()
        self.assertEqual(uni.num_undergrads, 83)

    def test_university_6(self):
        '''
        Test University class
        '''
        uni = University.query.filter_by(name='American Sentinel University').first()
        self.assertEqual(uni.num_undergrads, 1701)

    def test_university_7(self):
        '''
        Test University class
        '''
        uni = University.query.filter_by(
            name='Center for Natural Wellness School of Massage Therapy').first()
        self.assertEqual(uni.num_undergrads, 45)

    def test_university_8(self):
        '''
        Test University class
        '''
        uni = University.query.filter_by(name='Trenz Beauty Academy').first()
        self.assertEqual(uni.num_undergrads, 54)

    def test_university_9(self):
        '''
        Test University class
        '''
        uni = University.query.filter_by(name='SOLEX College').first()
        self.assertEqual(uni.num_undergrads, 85)

    def test_university_10(self):
        '''
        Test University class
        '''
        uni = University.query.filter_by(name='Star Career Academy-Audubon').first()
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
        majorcity = MAJORTOCITY.query.filter_by(city_name='Madison', \
            major_name='Visual Performing').first()
        self.assertEqual(majorcity.num_students, 2111)

    def test_majortocity_2(self):
        '''
        Test MAJORTOCITY class
        '''
        majorcity = MAJORTOCITY.query.filter_by(city_name='Pensacola', \
            major_name='Construction').first()
        self.assertEqual(majorcity.num_students, 96)

    def test_majortocity_3(self):
        '''
        Test MAJORTOCITY class
        '''
        majorcity = MAJORTOCITY.query.filter_by(city_name='Warner Robins', \
            major_name='Health').first()
        self.assertEqual(majorcity.num_students, 1124)

    def test_majortocity_4(self):
        '''
        Test MAJORTOCITY class
        '''
        majorcity = MAJORTOCITY.query.filter_by(city_name='New York', \
            major_name='Health').first()
        self.assertEqual(majorcity.num_students, 14801)

    def test_majortocity_5(self):
        '''
        Test MAJORTOCITY class
        '''
        majorcity = MAJORTOCITY.query.filter_by(city_name='Bethlehem', \
            major_name='Construction').first()
        self.assertEqual(majorcity.num_students, 78)

    def test_majortocity_6(self):
        '''
        Test MAJORTOCITY class
        '''
        majorcity = MAJORTOCITY.query.filter_by(city_name='Oklahoma City', \
            major_name='Computer').first()
        self.assertEqual(majorcity.num_students, 946)

    def test_majortocity_7(self):
        '''
        Test MAJORTOCITY class
        '''
        majorcity = MAJORTOCITY.query.filter_by(city_name='Phoenix', \
            major_name='Health').first()
        self.assertEqual(majorcity.num_students, 39500)

    # --------------------
    # majortocity __repr__
    # --------------------

    def test_majortocity_repr_1(self):
        '''
        Test MAJORTOCITY __repr__
        '''
        majorcity = MAJORTOCITY.query.filter_by(city_name='Chicago', \
            major_name='Business Marketing').first()
        self.assertEqual(majorcity.__repr__(), '<City Chicago, Major Business Marketing>')

    def test_majortocity_repr_2(self):
        '''
        Test MAJORTOCITY __repr__
        '''
        majorcity = MAJORTOCITY.query.filter_by(city_name='Perth Amboy', \
            major_name='Health').first()
        self.assertEqual(majorcity.__repr__(), '<City Perth Amboy, Major Health>')

    def test_majortocity_repr_3(self):
        '''
        Test MAJORTOCITY __repr__
        '''
        majorcity = MAJORTOCITY.query.filter_by(city_name='Rockville', \
            major_name='Personal Culinary').first()
        self.assertEqual(majorcity.__repr__(), '<City Rockville, Major Personal Culinary>')

    def test_majortocity_repr_4(self):
        '''
        Test MAJORTOCITY __repr__
        '''
        majorcity = MAJORTOCITY.query.filter_by(city_name='Audubon', \
            major_name='Health').first()
        self.assertEqual(majorcity.__repr__(), '<City Audubon, Major Health>')

    def test_majortocity_repr_5(self):
        '''
        Test MAJORTOCITY __repr__
        '''
        majorcity = MAJORTOCITY.query.filter_by(city_name='Calumet', \
            major_name='Personal Culinary').first()
        self.assertEqual(majorcity.__repr__(), '<City Calumet, Major Personal Culinary>')

    def test_majortocity_repr_6(self):
        '''
        Test MAJORTOCITY __repr__
        '''
        majorcity = MAJORTOCITY.query.filter_by(city_name='Hialeah', \
            major_name='Computer').first()
        self.assertEqual(majorcity.__repr__(), '<City Hialeah, Major Computer>')

    def test_majortocity_repr_7(self):
        '''
        Test MAJORTOCITY __repr__
        '''
        majorcity = MAJORTOCITY.query.filter_by(city_name='Reno', \
            major_name='Health').first()
        self.assertEqual(majorcity.__repr__(), '<City Reno, Major Health>')

    def test_majortocity_repr_8(self):
        '''
        Test MAJORTOCITY __repr__
        '''
        majorcity = MAJORTOCITY.query.filter_by(city_name='Chicago', \
            major_name='Business Marketing').first()
        self.assertEqual(majorcity.__repr__(), '<City Chicago, Major Business Marketing>')

    def test_majortocity_repr_9(self):
        '''
        Test MAJORTOCITY __repr__
        '''
        majorcity = MAJORTOCITY.query.filter_by(city_name='Memphis', \
            major_name='Personal Culinary').first()
        self.assertEqual(majorcity.__repr__(), '<City Memphis, Major Personal Culinary>')

    def test_majortocity_repr_10(self):
        '''
        Test MAJORTOCITY __repr__
        '''
        majorcity = MAJORTOCITY.query.filter_by(city_name='Philadelphia', \
            major_name='Health').first()
        self.assertEqual(majorcity.__repr__(), '<City Philadelphia, Major Health>')

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

    def test_city_repr_4(self):
        '''
        Test City __repr__
        '''
        city = City('Seattle')
        self.assertEqual(city.__repr__(), '<City Seattle>')

    def test_city_repr_5(self):
        '''
        Test City __repr__
        '''
        city = City('Milledgeville')
        self.assertEqual(city.__repr__(), '<City Milledgeville>')

    def test_city_repr_6(self):
        '''
        Test City __repr__
        '''
        city = City('Tampa')
        self.assertEqual(city.__repr__(), '<City Tampa>')

    def test_city_repr_7(self):
        '''
        Test City __repr__
        '''
        city = City('West Palm Beach')
        self.assertEqual(city.__repr__(), '<City West Palm Beach>')

        # # -----------
        # # major class
        # # -----------

    def test_major_1(self):
        '''
        Test Major class
        '''
        maj = Major.query.filter_by(name='Computer').first()
        self.assertEqual(maj.num_undergrads, 533608)
        self.assertEqual(maj.top_city, "Tempe")

    def test_major_2(self):
        '''
        Test Major class
        '''
        maj = Major.query.filter_by(name='Humanities').first()
        self.assertEqual(maj.num_undergrads, 2180469)
        self.assertEqual(maj.top_city, "Miami")

    def test_major_3(self):
        '''
        Test Major class
        '''
        maj = Major.query.filter_by(name='History').first()
        self.assertEqual(maj.num_undergrads, 150196)
        self.assertEqual(maj.top_city, "Los Angeles")

    def test_major_4(self):
        '''
        Test Major class
        '''
        maj = Major.query.filter_by(name='Mathematics').first()
        self.assertEqual(maj.num_undergrads, 110280)
        self.assertEqual(maj.top_city, "Los Angeles")

    def test_major_5(self):
        '''
        Test Major class
        '''
        maj = Major.query.filter_by(name='Social Science').first()
        self.assertEqual(maj.num_undergrads, 748209)
        self.assertEqual(maj.top_city, "New York")

    def test_major_6(self):
        '''
        Test Major class
        '''
        maj = Major.query.filter_by(name='Engineering').first()
        self.assertEqual(maj.num_undergrads, 452359)
        self.assertEqual(maj.top_city, "Atlanta")

    def test_major_7(self):
        '''
        Test Major class
        '''
        maj = Major.query.filter_by(name='Communication').first()
        self.assertEqual(maj.num_undergrads, 452121)
        self.assertEqual(maj.top_city, "New York")

    def test_major_8(self):
        '''
        Test Major class
        '''
        maj = Major.query.filter_by(name='Education').first()
        self.assertEqual(maj.num_undergrads, 598088)
        self.assertEqual(maj.top_city, "Salt Lake City")

    def test_major_9(self):
        '''
        Test Major class
        '''
        maj = Major.query.filter_by(name='Legal').first()
        self.assertEqual(maj.num_undergrads, 93870)
        self.assertEqual(maj.top_city, "Orlando")

    def test_major_10(self):
        '''
        Test Major class
        '''
        maj = Major.query.filter_by(name='Agriculture').first()
        self.assertEqual(maj.num_undergrads, 125860)
        self.assertEqual(maj.top_city, "College Station")

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

    def test_major_repr_4(self):
        '''
        Test Major __repr__
        '''
        major = Major('Computer Science')
        self.assertEqual(major.__repr__(), '<Major Computer Science>')

    def test_major_repr_5(self):
        '''
        Test Major __repr__
        '''
        major = Major('Humanities')
        self.assertEqual(major.__repr__(), '<Major Humanities>')

    # ----------------
    # major attributes
    # ----------------

    def test_major_attr_1(self):
        '''
        Test Major attributes
        '''
        major = Major('Economics')
        self.assertEqual(major.attributes(), {'name': 'Economics'})

    def test_major_attr_2(self):
        '''
        Test Major attributes
        '''
        major = Major('Engineering')
        self.assertEqual(major.attributes(), {'name': 'Engineering'})

    def test_major_attr_3(self):
        '''
        Test Major attributes
        '''
        major = Major('Business')
        self.assertEqual(major.attributes(), {'name': 'Business'})

    def test_major_attr_4(self):
        '''
        Test Major attributes
        '''
        major = Major('Computer Science')
        self.assertEqual(major.attributes(), {'name': 'Computer Science'})

    def test_major_attr_5(self):
        '''
        Test Major attributes
        '''
        major = Major('Humanities')
        self.assertEqual(major.attributes(), {'name': 'Humanities'})

    # ---------------
    # ethnicity class
    # ---------------

# ----
# main
# ----

if __name__ == "__main__":
    main()
