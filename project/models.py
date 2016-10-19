from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/swe'

db = SQLAlchemy(app)

tags = db.Table('tags',
    db.Column('city_id', db.Integer, db.ForeignKey('city.id')),
    db.Column('major_id', db.Integer, db.ForeignKey('major.id'))
)

class University(db.Model):
	'''
	TODO: documentation
	'''
	__tablename__ = 'UNIVERSITY'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	numUndergrads = db.Column(db.Integer)
	costToAttend = db.Column(db.Integer)
	gradRate = db.Column(db.Float)
    
	# todo: relationship
    location = db.Column(db.String(80), db.ForeignKey('city.id'))
    
    publicOrPrivate = db.Column(db.String(80))

    # todo: relationship
    ethnicityCount = db.Column(db.Integer)

    def __init__(self, name, numUndergrads, costToAttend, gradRate, location, publicOrPrivate, ethnicityCount):
        self.name = name
        self.numUndergrads = numUndergrads
        self.costToAttend = costToAttend
        self.gradRate = gradRate
        self.location = location
        self.publicOrPrivate = publicOrPrivate
        self.ethnicityCount = ethnicityCount

    def __repr__(self):
        return '<University %r>' % self.name

class City(db.Model):
	'''
	TODO: documentation
	'''
	__tablename__ = 'CITY'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	population = db.Column(db.Integer)
	
	# todo: relationship
	universityList = db.relationship('University', backref='city', lazy='dynamic')
	majorList = db.relationship('Major', backref='major', lazy='dynamic')
	
	avgTuition = db.Column(db.Integer)
    urbanOrRural = db.Column(db.String(80))

    # todo: relationship
    ethnicityCount = db.Column(db.Integer)

    def __init__(self, name, population, universityList, majorList, avgTuition, urbanOrRural, ethnicityCount):
		self.name = name
		self.population = population
		self.universityList = universityList
		self.majorList = majorList
		self.avgTuition = avgTuition
		self.urbanOrRural = urbanOrRural
		self.ethnicityCount	= ethnicityCount        

    def __repr__(self):
        return '<City %r>' % self.name

class Major(db.Model):
	'''
	TODO: documentation
	'''
	__tablename__ = 'MAJOR'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	numUndergrads = db.Column(db.Integer)
	gradRate = db.Column(db.Float)
    
	# todo: relationship
	universityList = db.relationship('University', backref='city', lazy='dynamic')
	cityList = db.relationship('City', backref='city', lazy='dynamic')
	
	avgPercentage = db.Column(db.Float)
	
    def __init__(self, name, numUndergrads, gradRate, universityList, cityList, avgPercentage):
        self.name = name
		self.numUndergrads = numUndergrads
		self.gradRate = gradRate
		self.universityList = universityList
		self.cityList = cityList
		self.avgPercentage = avgPercentage

    def __repr__(self):
        return '<Major %r>' % self.name

class Ethnicity(db.Model):
	'''
	TODO: documentation
	'''
	__tablename__ = 'ETHNICITY'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	totalCount = db.Column(db.Integer)
	
	# todo:	relationship
	topByCity = db.relationship('City', backref='city', lazy='dynamic')
	topByUniversity = db.relationship('University', backref='university', lazy='dynamic')
    
    # todo:	relationship
	populationTrend = db.relationship('Ethnicity', backref='ethnicity', lazy='dynamic')

    def __init__(self, name, totalCount, topByCity, topByUniversity, populationTrend):
        self.name = name
		self.totalCount = totalCount
		self.topByCity = topByCity
		self.topByUniversity = topByUniversity
		self.populationTrend = populationTrend

    def __repr__(self):
        return '<Ethnicity %r>' % self.name