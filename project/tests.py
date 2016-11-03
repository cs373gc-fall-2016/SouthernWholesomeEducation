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
    # university class
    # ----------------

    def test_university_1(self):
        '''
        Test University class
        '''
        university = create_unique(University, name='UT', num_undergrads=10, \
            cost_to_attend=100, grad_rate=0.8, public_or_private='public')
        university.add_major(500, name='Engineering')
        university.add_major(700, name='Computer Science')
        university.add_ethnicity(1000, name='White')

        name = university.name
        num_undergrads = university.num_undergrads
        cost_to_attend = university.cost_to_attend
        grad_rate = university.grad_rate
        public_or_private = university.public_or_private
        major_list = university.major_list
        ethnicity_list = university.ethnicity_list

        self.assertEqual(name, "UT")
        self.assertEqual(num_undergrads, 10)
        self.assertEqual(cost_to_attend, 100)
        self.assertEqual(grad_rate, .80)
        self.assertEqual(public_or_private, "public")
        self.assertEqual(major_list[0].__repr__(), '<University UT, Major Engineering>')
        self.assertEqual(ethnicity_list[0].__repr__(), '<University UT, Ethnicity White>')
        DB.session.commit()
        entries = University.query.filter_by(name='UT', cost_to_attend=100).first()
        self.assertEqual(entries.num_undergrads, 10)

    def test_update(self):
        """
        Test update database
        """
        assoc = get_association(MAJORTOUNIVERSITY, major_name='Engineering', university_name='UT')
        assoc.num_students = 70000
        DB.session.commit()
        self.assertEqual(assoc.num_students, 70000)

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

        # -------------------
        # university addMajor
        # -------------------

    def test_university_add_major_1(self):
        '''
        Test University addMajor
        '''
        university = University('UT', 0, 0, 0, '')
        university.add_major(1000, name='Physics')
        self.assertEqual(university.major_list[0].__repr__(), '<University UT, Major Physics>')

    def test_university_add_major_2(self):
        '''
        Test University addMajor
        '''
        university = University('A&M', 0, 0, 0, '')
        university.add_major(1000, name='Chemistry')
        self.assertEqual(university.major_list[0].__repr__(), '<University A&M, Major Chemistry>')

    def test_university_add_major_3(self):
        '''
        Test University addMajor
        '''
        university = University('Rice', 0, 0, 0, '')
        university.add_major(1000, name='Biology')
        self.assertEqual(university.major_list[0].__repr__(), '<University Rice, Major Biology>')

        # # -----------------------
        # # university addEthnicity
        # # -----------------------

    def test_university_add_ethnicity_1(self):
        '''
        Test University addEthnicity
        '''
        university = University('UT', 0, 0, 0, '')
        university.add_ethnicity(100, name='Asian')
        self.assertEqual(university.ethnicity_list[0].__repr__(), \
            '<University UT, Ethnicity Asian>')

    def test_university_add_ethnicity_2(self):
        '''
        Test University addEthnicity
        '''
        university = University('A&M', 0, 0, 0, '')
        university.add_ethnicity(1000, name='White')
        self.assertEqual(university.ethnicity_list[0].__repr__(), \
            '<University A&M, Ethnicity White>')

    def test_university_add_ethnicity_3(self):
        '''
        Test University addEthnicity
        '''
        university = University('Rice', 0, 0, 0, '')
        university.add_ethnicity(400, name='African American')
        self.assertEqual(university.ethnicity_list[0].__repr__(), \
            '<University Rice, Ethnicity African American>')

        # # ----------
        # # city class
        # # ----------

    def test_city_1(self):
        '''
        Test City class
        '''
        city = create_unique(City, name='Austin')
        university = create_unique(University, name='UT', num_undergrads=0, \
            cost_to_attend=0, grad_rate=0, public_or_private='')
        city.add_university(university)
        city.add_major(1000, name='Business')
        city.add_ethnicity(300, name='Asian')
        city.add_ethnicity(300, name='White')

        name = city.name
        population = city.population
        university_list = city.university_list
        major_list = city.major_list
        ethnicity_list = city.ethnicity_list
        avg_tuition = city.avg_tuition

        self.assertEqual(name, 'Austin')
        self.assertEqual(population, 42905)
        self.assertEqual(university_list[0].__repr__(), '<University UT>')
        self.assertEqual(major_list[0].__repr__(), '<City Austin, Major Business>')
        self.assertEqual(ethnicity_list[0].__repr__(), '<City Austin, Ethnicity Asian>')
        self.assertEqual(avg_tuition, 17357)
        DB.session.commit()
        assoc = get_association(ETHNICITYTOCITY, ethnicity_name='White', city_name='Austin')
        self.assertEqual(assoc.num_students, 5000)

        # # -------------
        # # city __repr__
        # # -------------

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

        # # ------------------
        # # city addUniversity
        # # ------------------

    def test_city_add_university_1(self):
        '''
        Test City addUniversity
        '''
        city = City('Austin')
        university = University('UT', 0, 0, 0, '')
        city.add_university(university)
        self.assertEqual(city.__repr__(), '<City Austin>')

    def test_city_add_university_2(self):
        '''
        Test City addUniversity
        '''
        city = City('Salt Lake City')
        university = University('SLC', 0, 0, 0, '')
        city.add_university(university)
        self.assertEqual(city.__repr__(), '<City Salt Lake City>')

    def test_city_add_university_3(self):
        '''
        Test City addUniversity
        '''
        city = City('New York')
        university = University('NY', 0, 0, 0, '')
        city.add_university(university)
        self.assertEqual(city.__repr__(), '<City New York>')

        # # -------------
        # # city addMajor
        # # -------------

    def test_city_add_major_1(self):
        '''
        Test city addMajor
        '''
        city = City('Austin')
        city.add_major(1000, name='Physics')
        self.assertEqual(city.major_list[0].__repr__(), '<City Austin, Major Physics>')

    def test_city_add_major_2(self):
        '''
        Test city addMajor
        '''
        city = City('Salt Lake City')
        city.add_major(1000, name='Chemistry')
        self.assertEqual(city.major_list[0].__repr__(), '<City Salt Lake City, Major Chemistry>')

    def test_city_add_major_3(self):
        '''
        Test city addMajor
        '''
        city = City('New York')
        city.add_major(500, name='Biology')
        self.assertEqual(city.major_list[0].__repr__(), '<City New York, Major Biology>')

        # # -----------------------
        # # city addEthnicity
        # # -----------------------

    def test_city_add_ethnicity_1(self):
        '''
        Test University addEthnicity
        '''
        city = City('Austin')
        city.add_ethnicity(300, name='Asian')
        self.assertEqual(city.ethnicity_list[0].__repr__(), '<City Austin, Ethnicity Asian>')

    def test_city_add_ethnicity_2(self):
        '''
        Test University addEthnicity
        '''
        city = City('Salt Lake City')
        city.add_ethnicity(200, name='White')
        self.assertEqual(city.ethnicity_list[0].__repr__(), \
            '<City Salt Lake City, Ethnicity White>')

    def test_city_add_ethnicity_3(self):
        '''
        Test University addEthnicity
        '''
        city = City('New York')
        city.add_ethnicity(600, name='African American')
        self.assertEqual(city.ethnicity_list[0].__repr__(), \
            '<City New York, Ethnicity African American>')

        # # -----------
        # # major class
        # # -----------

    def test_major_1(self):
        '''
        Test Major class
        '''
        major = Major('Economics')

        name = major.name

        self.assertEqual(name, 'Economics')

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

    def test_ethnicity_1(self):
        '''
        Test Ethnicity class
        '''
        ethnicity = Ethnicity('Alaskan Indian')

        name = ethnicity.name
        total_count = ethnicity.total_count

        self.assertEqual(name, 'Alaskan Indian')
        self.assertEqual(total_count, 0)

        # # -------------
        # # ethnicity __repr__
        # # -------------

    def test_ethnicity_repr_1(self):
        '''
        Test Ethnicity __repr__
        '''
        ethnicity = Ethnicity('Alaskan Indian')
        self.assertEqual(ethnicity.__repr__(), '<Ethnicity Alaskan Indian>')

    def test_ethnicity_repr_2(self):
        '''
        Test Ethnicity __repr__
        '''
        ethnicity = Ethnicity('Native American')
        self.assertEqual(ethnicity.__repr__(), '<Ethnicity Native American>')

    def test_ethnicity_repr_3(self):
        '''
        Test Ethnicity __repr__
        '''
        ethnicity = Ethnicity('African American')
        self.assertEqual(ethnicity.__repr__(), '<Ethnicity African American>')

# ----
# main
# ----

if __name__ == "__main__":
    main()
