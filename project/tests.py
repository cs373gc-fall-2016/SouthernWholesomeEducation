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

class test(TestCase):
	'''
	Unit tests for models.py
	'''

	# ----------------
	# university class
	# ----------------

	# def test_university_1(self):
	# 	'''
	# 	Test University class
	# 	'''
	# 	university = University('UT', 10, 100, .80 , 'public')
	# 	major = Major('Engineering', 0, 0, 0)
	# 	ethnicity = Ethnicity('White')
	# 	university.addMajor(major)
	# 	university.addEthnicity(ethnicity)
		
	# 	name = university.name
	# 	numUndergrads = university.numUndergrads
	# 	costToAttend = university.costToAttend
	# 	gradRate = university.gradRate
	# 	publicOrPrivate = university.publicOrPrivate
	# 	majorList = university.majorList
	# 	ethnicityList = university.ethnicityList
	# 	city = university.city

	# 	self.assertEqual(name, "UT")
	# 	self.assertEqual(numUndergrads, 10)
	# 	self.assertEqual(costToAttend, 100)
	# 	self.assertEqual(gradRate, .80)
	# 	self.assertEqual(publicOrPrivate, "public")
	# 	self.assertEqual(majorList[0].__repr__(), '<Major Engineering>')
	# 	self.assertEqual(ethnicityList[0].__repr__(), '<Ethnicity White>')
	# 	self.assertEqual(city, "Austin")

	# -------------------
	# university __repr__
	# -------------------

	def test_university_repr_1(self):
		'''
		Test University __repr__
		'''
		university = University('UT', 0, 0, 0 , '')
		self.assertEqual(university.__repr__(), '<University UT>');

	def test_university_repr_2(self):
		'''
		Test University __repr__
		'''
		university = University('A&M', 0, 0, 0 , '')
		self.assertEqual(university.__repr__(), '<University A&M>');

	def test_university_repr_3(self):
		'''
		Test University __repr__
		'''
		university = University('Rice', 0, 0, 0 , '')
		self.assertEqual(university.__repr__(), '<University Rice>');

	# -------------------
	# university addMajor
	# -------------------

	def test_university_addMajor_1(self):
		'''
		Test University addMajor
		'''
		university = University('UT', 0, 0, 0 , '')
		university.addMajor('Physics')
		self.assertEqual(university.majorList[0].__repr__(), '<Major Physics>');

	# def test_university_addMajor_2(self):
	# 	'''
	# 	Test University addMajor
	# 	'''
	# 	university = University('A&M', 0, 0, 0 , '')
	# 	university.addMajor('Chemistry')
	# 	self.assertEqual(university.majorList[0].__repr__(), '<Major Chemistry>');

	# def test_university_addMajor_3(self):
	# 	'''
	# 	Test University addMajor
	# 	'''
	# 	university = University('Rice', 0, 0, 0 , '')
	# 	university.addMajor('Biology')
	# 	self.assertEqual(university.majorList[0].__repr__(), '<Major Biology>');

	# # -----------------------
	# # university addEthnicity
	# # -----------------------

	# def test_university_addEthnicity_1(self):
	# 	'''
	# 	Test University addEthnicity
	# 	'''
	# 	university = University('UT', 0, 0, 0 , '')
	# 	ethnicity = Ethnicity('Asian')
	# 	university.addEthnicity(ethnicity)
	# 	self.assertEqual(university.ethnicityList[0].__repr__(), '<Ethnicity Asian>');

	# def test_university_addEthnicity_2(self):
	# 	'''
	# 	Test University addEthnicity
	# 	'''
	# 	university = University('A&M', 0, 0, 0 , '')
	# 	ethnicity = Ethnicity('White')
	# 	university.addEthnicity(ethnicity)
	# 	self.assertEqual(university.ethnicityList[0].__repr__(), '<Ethnicity White>');

	# def test_university_addEthnicity_3(self):
	# 	'''
	# 	Test University addEthnicity
	# 	'''
	# 	university = University('Rice', 0, 0, 0 , '')
	# 	ethnicity = Ethnicity('African American')
	# 	university.addEthnicity(ethnicity)
	# 	self.assertEqual(university.ethnicityList[0].__repr__(), '<Ethnicity African American>');

	# # ----------
	# # city class
	# # ----------

	# def test_city_1(self):
	# 	'''
	# 	Test City class
	# 	'''
	# 	city = City('Austin', 'urban')
	# 	university = University('UT', 0, 0, 0 , '')
	# 	major = Major('Business', 0, 0, 0)
	# 	ethnicity = Ethnicity('Asian')
	# 	city.addUniversity(university)
	# 	city.addMajor(major)
	# 	city.addEthnicity(ethnicity)

	# 	name = city.name
	# 	population = city.population
	# 	universityList = city.universityList
	# 	majorList = city.majorList
	# 	ethnicityList = city.ethnicityList
	# 	avgTuition = city.avgTuition
	# 	urbanOrRural = city.urbanOrRural

	# 	self.assertEqual(name, 'Austin')
	# 	self.assertEqual(population, 0)
	# 	self.assertEqual(universityList[0].__repr__(), '<University UT>')
	# 	self.assertEqual(majorList[0].__repr__(), '<Major Business>')
	# 	self.assertEqual(ethnicityList[0].__repr__(), '<Ethnicity Asian>')
	# 	self.assertEqual(avgTuition, 0)
	# 	self.assertEqual(urbanOrRural, 'urban')

	# # -------------
	# # city __repr__
	# # -------------

	# def test_city_repr_1(self):
	# 	'''
	# 	Test City __repr__
	# 	'''
	# 	city = City('Austin', 'urban')
	# 	self.assertEqual(city.__repr__(), '<City Austin>')

	# def test_city_repr_2(self):
	# 	'''
	# 	Test City __repr__
	# 	'''
	# 	city = City('Salt Lake City', 'urban')
	# 	self.assertEqual(city.__repr__(), '<City Salt Lake City>')

	# def test_city_repr_3(self):
	# 	'''
	# 	Test City __repr__
	# 	'''
	# 	city = City('New York', 'urban')
	# 	self.assertEqual(city.__repr__(), '<City New York>')

	# # ------------------
	# # city addUniversity
	# # ------------------

	# def test_city_addUniversity_1(self):
	# 	'''
	# 	Test City addUniversity
	# 	'''
	# 	city = City('Austin', 'urban')
	# 	university = University('UT', 0, 0, 0 , '')
	# 	city.addUniversity(university)
	# 	self.assertEqual(city.__repr__(), '<City Austin>')

	# def test_city_addUniversity_2(self):
	# 	'''
	# 	Test City addUniversity
	# 	'''
	# 	city = City('Salt Lake City', 'urban')
	# 	university = University('SLC', 0, 0, 0 , '')
	# 	city.addUniversity(university)
	# 	self.assertEqual(city.__repr__(), '<City Salt Lake City>')

	# def test_city_addUniversity_3(self):
	# 	'''
	# 	Test City addUniversity
	# 	'''
	# 	city = City('New York', 'urban')
	# 	university = University('NY', 0, 0, 0 , '')
	# 	city.addUniversity(university)
	# 	self.assertEqual(city.__repr__(), '<City New York>')

	# # -------------
	# # city addMajor
	# # -------------

	# def test_university_addMajor_1(self):
	# 	'''
	# 	Test city addMajor
	# 	'''
	# 	city = City('Austin', 'urban')
	# 	cirtt.addMajor('Physics')
	# 	self.assertEqual(city.majorList[0].__repr__(), '<Major Physics>');

	# def test_university_addMajor_2(self):
	# 	'''
	# 	Test city addMajor
	# 	'''
	# 	city = City('Salt Lake City', 'urban')
	# 	cirtt.addMajor('Chemistry')
	# 	self.assertEqual(city.majorList[0].__repr__(), '<Major Chemistry>');

	# def test_university_addMajor_3(self):
	# 	'''
	# 	Test city addMajor
	# 	'''
	# 	city = City('New York', 'urban')
	# 	cirtt.addMajor('Biology')
	# 	self.assertEqual(city.majorList[0].__repr__(), '<Major Biology>');

	# # -----------------------
	# # city addEthnicity
	# # -----------------------

	# def test_university_addEthnicity_1(self):
	# 	'''
	# 	Test University addEthnicity
	# 	'''
	# 	city = City('Austin', 'urban')
	# 	ethnicity = Ethnicity('Asian')
	# 	city.addEthnicity(ethnicity)
	# 	self.assertEqual(city.ethnicityList[0].__repr__(), '<Ethnicity Asian>');

	# def test_university_addEthnicity_2(self):
	# 	'''
	# 	Test University addEthnicity
	# 	'''
	# 	city = City('Salt Lake City', 'urban')
	# 	ethnicity = Ethnicity('White')
	# 	city.addEthnicity(ethnicity)
	# 	self.assertEqual(city.ethnicityList[0].__repr__(), '<Ethnicity White>');

	# def test_university_addEthnicity_3(self):
	# 	'''
	# 	Test University addEthnicity
	# 	'''
	# 	city = City('New York', 'urban')
	# 	ethnicity = Ethnicity('African American')
	# 	city.addEthnicity(ethnicity)
	# 	self.assertEqual(city.ethnicityList[0].__repr__(), '<Ethnicity African American>');

	# # -----------
	# # major class
	# # -----------

	# def test_major_1(self):
	# 	'''
	# 	Test Major class
	# 	'''
	# 	major = Major('Economics', 22, .55, .14)
		
	# 	name = major.name
	# 	numUndergrads = major.numUndergrads
	# 	gradRate = major.gradRate
	# 	avgPercentage = major.avgPercentage

	# 	self.assertEqual(name, 'Economics')
	# 	self.assertEqual(numUndergrads, 22)
	# 	self.assertEqual(gradRate, .55)
	# 	self.assertEqual(avgPercentage, .14)
		
	# # -------------
	# # major __repr__
	# # -------------

	# def test_major_repr_1(self):
	# 	'''
	# 	Test Major __repr__
	# 	'''
	# 	major = Major('Economics', 0, 0, 0)
	# 	self.assertEqual(major.__repr__(), '<Major Economics>')

	# def test_major_repr_2(self):
	# 	'''
	# 	Test Major __repr__
	# 	'''
	# 	major = Major('Engineering', 0, 0, 0)
	# 	self.assertEqual(major.__repr__(), '<Major Engineering>')

	# def test_major_repr_3(self):
	# 	'''
	# 	Test Major __repr__
	# 	'''
	# 	major = Major('Business', 0, 0, 0)
	# 	self.assertEqual(major.__repr__(), '<Major Business>')

	# # ---------------
	# # ethnicity class
	# # ---------------

	# def test_ethnicity_1(self):
	# 	'''
	# 	Test Ethnicity class
	# 	'''
	# 	ethnicity = Ethnicity('Alaskan Indian')

	# 	name = ethnicity.name
	# 	totalCount = ethnicity.totalCount

	# 	self.assertEqual(name, 'Alaskan Indian')
	# 	self.assertEqual(totalCount, 0)

	# # -------------
	# # ethnicity __repr__
	# # -------------

	# def test_major_repr_1(self):
	# 	'''
	# 	Test Ethnicity __repr__
	# 	'''
	# 	ethnicity = Ethnicity('Alaskan Indian')
	# 	self.assertEqual(ethnicity.__repr__(), '<Ethnicity Alaskan Indian>')

	# def test_major_repr_2(self):
	# 	'''
	# 	Test Ethnicity __repr__
	# 	'''
	# 	ethnicity = Ethnicity('Native American')
	# 	self.assertEqual(ethnicity.__repr__(), '<Ethnicity Native American>')

	# def test_major_repr_3(self):
	# 	'''
	# 	Test Ethnicity __repr__
	# 	'''
	# 	ethnicity = Ethnicity('African American')
	# 	self.assertEqual(ethnicity.__repr__(), '<Ethnicity African American>')

# ----
# main
# ----

if __name__ == "__main__":
    main()