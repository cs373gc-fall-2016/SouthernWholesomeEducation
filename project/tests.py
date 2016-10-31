# pylint: disable=W0401,W0614,R0904,E1101
#!/usr/bin/env python3
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
        university = University('UT', 10, 100, .80, 'public')
        university.add_major('Engineering')
        university.add_ethnicity('White')

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
        self.assertEqual(major_list[0].__repr__(), '<Major Engineering>')
        self.assertEqual(ethnicity_list[0].__repr__(), '<Ethnicity White>')
        add_unique(university)
        entries = University.query.filter_by(name='UT',cost_to_attend=100).first()
        print(entries.ethnicity_list)
        self.assertEqual(entries.num_undergrads, 10)

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
        university.add_major('Physics')
        self.assertEqual(university.major_list[0].__repr__(), '<Major Physics>')

    def test_university_add_major_2(self):
        '''
        Test University addMajor
        '''
        university = University('A&M', 0, 0, 0, '')
        university.add_major('Chemistry')
        self.assertEqual(university.major_list[0].__repr__(), '<Major Chemistry>')

    def test_university_add_major_3(self):
        '''
        Test University addMajor
        '''
        university = University('Rice', 0, 0, 0, '')
        university.add_major('Biology')
        self.assertEqual(university.major_list[0].__repr__(), '<Major Biology>')

        # # -----------------------
        # # university addEthnicity
        # # -----------------------

    def test_university_add_ethnicity_1(self):
        '''
        Test University addEthnicity
        '''
        university = University('UT', 0, 0, 0, '')
        university.add_ethnicity('Asian')
        self.assertEqual(university.ethnicity_list[0].__repr__(), '<Ethnicity Asian>')

    def test_university_add_ethnicity_2(self):
        '''
        Test University addEthnicity
        '''
        university = University('A&M', 0, 0, 0, '')
        university.add_ethnicity('White')
        self.assertEqual(university.ethnicity_list[0].__repr__(), '<Ethnicity White>')

    def test_university_add_ethnicity_3(self):
        '''
        Test University addEthnicity
        '''
        university = University('Rice', 0, 0, 0, '')
        university.add_ethnicity('African American')
        self.assertEqual(university.ethnicity_list[0].__repr__(), '<Ethnicity African American>')

        # # ----------
        # # city class
        # # ----------

    def test_city_1(self):
        '''
        Test City class
        '''
        city = City('Austin', 'urban')
        university = University('UT', 0, 0, 0, '')
        city.add_university(university)
        city.add_major('Business')
        city.add_ethnicity('Asian')

        name = city.name
        population = city.population
        university_list = city.university_list
        major_list = city.major_list
        ethnicity_list = city.ethnicity_list
        avg_tuition = city.avg_tuition
        urban_or_rural = city.urban_or_rural

        self.assertEqual(name, 'Austin')
        self.assertEqual(population, 0)
        self.assertEqual(university_list[0].__repr__(), '<University UT>')
        self.assertEqual(major_list[0].__repr__(), '<Major Business>')
        self.assertEqual(ethnicity_list[0].__repr__(), '<Ethnicity Asian>')
        self.assertEqual(avg_tuition, 0)
        self.assertEqual(urban_or_rural, 'urban')
        add_unique(university)
        add_unique(city)
        entries = City.query.filter_by(name='Austin').first()
        self.assertEqual(entries.urban_or_rural, 'urban')

        # # -------------
        # # city __repr__
        # # -------------

    def test_city_repr_1(self):
        '''
        Test City __repr__
        '''
        city = City('Austin', 'urban')
        self.assertEqual(city.__repr__(), '<City Austin>')

    def test_city_repr_2(self):
        '''
        Test City __repr__
        '''
        city = City('Salt Lake City', 'urban')
        self.assertEqual(city.__repr__(), '<City Salt Lake City>')

    def test_city_repr_3(self):
        '''
        Test City __repr__
        '''
        city = City('New York', 'urban')
        self.assertEqual(city.__repr__(), '<City New York>')

        # # ------------------
        # # city addUniversity
        # # ------------------

    def test_city_add_university_1(self):
        '''
        Test City addUniversity
        '''
        city = City('Austin', 'urban')
        university = University('UT', 0, 0, 0, '')
        city.add_university(university)
        self.assertEqual(city.__repr__(), '<City Austin>')

    def test_city_add_university_2(self):
        '''
        Test City addUniversity
        '''
        city = City('Salt Lake City', 'urban')
        university = University('SLC', 0, 0, 0, '')
        city.add_university(university)
        self.assertEqual(city.__repr__(), '<City Salt Lake City>')

    def test_city_add_university_3(self):
        '''
        Test City addUniversity
        '''
        city = City('New York', 'urban')
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
        city = City('Austin', 'urban')
        city.add_major('Physics')
        self.assertEqual(city.major_list[0].__repr__(), '<Major Physics>')

    def test_city_add_major_2(self):
        '''
        Test city addMajor
        '''
        city = City('Salt Lake City', 'urban')
        city.add_major('Chemistry')
        self.assertEqual(city.major_list[0].__repr__(), '<Major Chemistry>')

    def test_city_add_major_3(self):
        '''
        Test city addMajor
        '''
        city = City('New York', 'urban')
        city.add_major('Biology')
        self.assertEqual(city.major_list[0].__repr__(), '<Major Biology>')

        # # -----------------------
        # # city addEthnicity
        # # -----------------------

    def test_city_add_ethnicity_1(self):
        '''
        Test University addEthnicity
        '''
        city = City('Austin', 'urban')
        city.add_ethnicity('Asian')
        self.assertEqual(city.ethnicity_list[0].__repr__(), '<Ethnicity Asian>')

    def test_city_add_ethnicity_2(self):
        '''
        Test University addEthnicity
        '''
        city = City('Salt Lake City', 'urban')
        city.add_ethnicity('White')
        self.assertEqual(city.ethnicity_list[0].__repr__(), '<Ethnicity White>')

    def test_city_add_ethnicity_3(self):
        '''
        Test University addEthnicity
        '''
        city = City('New York', 'urban')
        city.add_ethnicity('African American')
        self.assertEqual(city.ethnicity_list[0].__repr__(), '<Ethnicity African American>')

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
