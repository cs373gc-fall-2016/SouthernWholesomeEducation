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
        self.assertEqual(uni.num_undergrads, 1066)

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


    # ---------------------
    # university attributes
    # ---------------------

    def test_university_attr_1(self):
        '''
        Test University attributes
        '''
        uni = University.query.filter_by(name='Star Career Academy-Audubon').first()
        self.assertEqual(uni.attributes()['name'], 'Star Career Academy-Audubon')


    def test_university_attr_2(self):
        '''
        Test University attributes
        '''
        uni = University.query.filter_by(name='CUNY LaGuardia Community College').first()
        self.assertEqual(uni.attributes()['num_undergrads'], 17069)



    def test_university_attr_3(self):
        '''
        Test University attributes
        '''
        uni = University.query.filter_by(name='Pepperdine University').first()
        self.assertEqual(uni.attributes()['cost_to_attend'], 26876)



    def test_university_attr_4(self):
        '''
        Test University attributes
        '''
        uni = University.query.filter_by(name='South Texas Training Center').first()
        self.assertEqual(uni.attributes()['public_or_private'], 'Private')



    def test_university_attr_5(self):
        '''
        Test University attributes
        '''
        uni = University.query.filter_by(name='Young Harris College').first()
        self.assertEqual(uni.attributes()['grad_rate'], 0.38154256198347)


    def test_university_attr_6(self):
        '''
        Test University attributes
        '''
        uni = University.query.filter_by(name='Everest Institute-Bensalem').first()
        self.assertEqual(uni.attributes()['name'], 'Everest Institute-Bensalem')


    def test_university_attr_7(self):
        '''
        Test University attributes
        '''
        uni = University.query.filter_by(name='University of Hartford').first()
        self.assertEqual(uni.attributes()['num_undergrads'], 4956)



    def test_university_attr_8(self):
        '''
        Test University attributes
        '''
        uni = University.query.filter_by(name='Grayson College').first()
        self.assertEqual(uni.attributes()['cost_to_attend'], 6941)



    def test_university_attr_9(self):
        '''
        Test University attributes
        '''
        uni = University.query.filter_by(name='Point University').first()
        self.assertEqual(uni.attributes()['public_or_private'], 'Private')



    def test_university_attr_10(self):
        '''
        Test University attributes
        '''
        uni = University.query.filter_by(name='College of the Marshall Islands').first()
        self.assertEqual(uni.attributes()['grad_rate'], 0.04389054054054)

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


    # -----------------------
    # MAJORTOUNIVERSITY class
    # -----------------------

    def test_majortouniversity_1(self):
        '''
        Test MAJORTOUNIVERSITY class
        '''
        majoruni = MAJORTOUNIVERSITY.query.filter_by(university_name='Delaware College of Art and Design', \
            major_name='Computer').first()
        self.assertEqual(majoruni.num_students, 2)


    def test_majortouniversity_2(self):
        '''
        Test MAJORTOUNIVERSITY class
        '''
        majoruni = MAJORTOUNIVERSITY.query.filter_by(university_name='Erskine College', \
            major_name='Mathematics').first()
        self.assertEqual(majoruni.num_students, 16)


    def test_majortouniversity_3(self):
        '''
        Test MAJORTOUNIVERSITY class
        '''
        majoruni = MAJORTOUNIVERSITY.query.filter_by(university_name='Ohio Business College-Sheffield', \
            major_name='Legal').first()
        self.assertEqual(majoruni.num_students, 24)


    def test_majortouniversity_4(self):
        '''
        Test MAJORTOUNIVERSITY class
        '''
        majoruni = MAJORTOUNIVERSITY.query.filter_by(university_name='East Central College', \
            major_name='Engineering').first()
        self.assertEqual(majoruni.num_students, 70)


    def test_majortouniversity_5(self):
        '''
        Test MAJORTOUNIVERSITY class
        '''
        majoruni = MAJORTOUNIVERSITY.query.filter_by(university_name='Baker College of Port Huron', \
            major_name='Health').first()
        self.assertEqual(majoruni.num_students, 391)


    def test_majortouniversity_6(self):
        '''
        Test MAJORTOUNIVERSITY class
        '''
        majoruni = MAJORTOUNIVERSITY.query.filter_by(university_name='William Penn University', \
            major_name='Education').first()
        self.assertEqual(majoruni.num_students, 243)


    def test_majortouniversity_7(self):
        '''
        Test MAJORTOUNIVERSITY class
        '''
        majoruni = MAJORTOUNIVERSITY.query.filter_by(university_name='Midland University', \
            major_name='English').first()
        self.assertEqual(majoruni.num_students, 6)


    def test_majortouniversity_8(self):
        '''
        Test MAJORTOUNIVERSITY class
        '''
        majoruni = MAJORTOUNIVERSITY.query.filter_by(university_name='Advance Tech College', \
            major_name='Health').first()
        self.assertEqual(majoruni.num_students, 1)


    def test_majortouniversity_9(self):
        '''
        Test MAJORTOUNIVERSITY class
        '''
        majoruni = MAJORTOUNIVERSITY.query.filter_by(university_name='Herzing University-Kenner', \
            major_name='Transportation').first()
        self.assertEqual(majoruni.num_students, 7)


    def test_majortouniversity_10(self):
        '''
        Test MAJORTOUNIVERSITY class
        '''
        majoruni = MAJORTOUNIVERSITY.query.filter_by(university_name='Antonelli College-Jackson', \
            major_name='Visual Performing').first()
        self.assertEqual(majoruni.num_students, 16)


    # --------------------------
    # MAJORTOUNIVERSITY __repr__
    # --------------------------



    # ----------
    # city class
    # ----------

    def test_city_1(self):
        '''
        Test City class
        '''
        city = City.query.filter_by(name='Richfield').first()
        self.assertEqual(city.population, 673)
        self.assertEqual(city.top_major, 'Business Marketing')

    def test_city_2(self):
        '''
        Test City class
        '''
        city = City.query.filter_by(name='Lakeland').first()
        self.assertEqual(city.population, 6988)
        self.assertEqual(city.top_major, 'Health')

    def test_city_3(self):
        '''
        Test City class
        '''
        city = City.query.filter_by(name='Sunnyvale').first()
        self.assertEqual(city.population, 40685)
        self.assertEqual(city.top_major, 'Visual Performing')

    def test_city_4(self):
        '''
        Test City class
        '''
        city = City.query.filter_by(name='Pittsburgh').first()
        self.assertEqual(city.population, 67755)
        self.assertEqual(city.top_major, 'Health')

    def test_city_5(self):
        '''
        Test City class
        '''
        city = City.query.filter_by(name='Santa Barbara').first()
        self.assertEqual(city.population, 37657)
        self.assertEqual(city.top_major, 'Humanities')

    def test_city_6(self):
        '''
        Test City class
        '''
        city = City.query.filter_by(name='Villanova').first()
        self.assertEqual(city.population, 15471)
        self.assertEqual(city.top_major, 'Business Marketing')

    def test_city_7(self):
        '''
        Test City class
        '''
        city = City.query.filter_by(name='Miami').first()
        self.assertEqual(city.population, 127001)
        self.assertEqual(city.top_major, 'Humanities')

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


    # ---------------
    # City attributes
    # ---------------

    def test_city_attr_1(self):
        '''
        Test City attributes
        '''
        city = City('Seattle')
        self.assertEqual(city.attributes()['name'], 'Seattle')


    def test_city_attr_2(self):
        '''
        Test City attributes
        '''
        city = City('Miami')
        self.assertEqual(city.attributes()['name'], 'Miami')


    def test_city_attr_3(self):
        '''
        Test City attributes
        '''
        city = City('Newberg')
        self.assertEqual(city.attributes()['name'], 'Newberg')


    def test_city_attr_4(self):
        '''
        Test City attributes
        '''
        city = City('Findlay')
        self.assertEqual(city.attributes()['name'], 'Findlay')


    def test_city_attr_5(self):
        '''
        Test City attributes
        '''
        city = City('Keshena')
        self.assertEqual(city.attributes()['name'], 'Keshena')


    def test_city_attr_5(self):
        '''
        Test City attributes
        '''
        city = City('Las Vegas')
        self.assertEqual(city.attributes()['name'], 'Las Vegas')


    def test_city_attr_6(self):
        '''
        Test City attributes
        '''
        city = City('Ontario')
        self.assertEqual(city.attributes()['name'], 'Ontario')


    def test_city_attr_7(self):
        '''
        Test City attributes
        '''
        city = City('Lawrenceburg')
        self.assertEqual(city.attributes()['name'], 'Lawrenceburg')


    def test_city_attr_9(self):
        '''
        Test City attributes
        '''
        city = City('Dobson')
        self.assertEqual(city.attributes()['name'], 'Dobson')


    def test_city_attr_10(self):
        '''
        Test City attributes
        '''
        city = City('Bessemer')
        self.assertEqual(city.attributes()['name'], 'Bessemer')


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

    # ---------------
    # ethnicity class
    # ---------------


    def test_ethnicity_1(self):
        '''
        Test Ethnicity class
        '''
        eth = Ethnicity.query.filter_by(name='White').first()
        self.assertEqual(eth.total_count, 8356122)
        self.assertEqual(eth.top_city, "Indianapolis")

    def test_ethnicity_2(self):
        '''
        Test Ethnicity class
        '''
        eth = Ethnicity.query.filter_by(name='Hispanic').first()
        self.assertEqual(eth.total_count, 2893839)
        self.assertEqual(eth.top_city, "Miami")

    def test_ethnicity_3(self):
        '''
        Test Ethnicity class
        '''
        eth = Ethnicity.query.filter_by(name='Asian').first()
        self.assertEqual(eth.total_count, 914889)
        self.assertEqual(eth.top_city, "New York")

    def test_ethnicity_4(self):
        '''
        Test Ethnicity class
        '''
        eth = Ethnicity.query.filter_by(name='Black').first()
        self.assertEqual(eth.total_count, 2261288)
        self.assertEqual(eth.top_city, "Houston")

    def test_ethnicity_5(self):
        '''
        Test Ethnicity class
        '''
        eth = Ethnicity.query.filter_by(name='Native Hawaiian Pacific Islander').first()
        self.assertEqual(eth.total_count, 53897)
        self.assertEqual(eth.top_city, "Mangilao")


# ----
# main
# ----

if __name__ == "__main__":
    main()

