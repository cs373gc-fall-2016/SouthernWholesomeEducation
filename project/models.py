# pylint: disable=E1101, R0913, C0103, R0201, R0903
"""Implements the models that will be used in database"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/swe'

DB = SQLAlchemy(APP)

MAJORTOCITY = DB.Table('majorsToCity',
                       DB.Column('city_id', DB.Integer,
                                 DB.ForeignKey('CITY.idNum')),
                       DB.Column('major_id', DB.Integer,
                                 DB.ForeignKey('MAJOR.idNum')))

ETHNICITYTOCITY = DB.Table('ETHNICITYTOCITY',
                           DB.Column('city_id', DB.Integer,
                                     DB.ForeignKey('CITY.idNum')),
                           DB.Column('ethnicity_id', DB.Integer,
                                     DB.ForeignKey('ETHNICITY.idNum')))

ETHNICITYTOUNIVERSITY = DB.Table('ETHNICITYTOUNIVERSITY',
                                 DB.Column('university_id', DB.Integer,
                                           DB.ForeignKey('UNIVERSITY.idNum')),
                                 DB.Column('ethnicity_id', DB.Integer,
                                           DB.ForeignKey('ETHNICITY.idNum')))

MAJORTOUNIVERSITY = DB.Table('MAJORTOUNIVERSITY',
                             DB.Column('university_id', DB.Integer,
                                       DB.ForeignKey('UNIVERSITY.idNum')),
                             DB.Column('major_id', DB.Integer,
                                       DB.ForeignKey('MAJOR.idNum')))


class University(DB.Model):
    '''
    Class for University pillar. The name, numUndergrads, costToAttend, gradRate
    , and publicOrPrivate variables will be set from API data and the
    ethnicityList and majorList will be created from relationships. A city
    variable will also be included from a backref with the City class.
    '''
    __tablename__ = 'UNIVERSITY'
    idNum = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(80))
    numUndergrads = DB.Column(DB.Integer)
    costToAttend = DB.Column(DB.Integer)
    gradRate = DB.Column(DB.Float)
    publicOrPrivate = DB.Column(DB.String(80))
    # ethnicityList = DB.relationship('Ethnicity', secondary=ETHNICITYTOUNIVERSITY,
    #                                 backref=DB.backref('university', lazy='dynamic'))
    majorList = DB.relationship('Major', secondary=MAJORTOUNIVERSITY,
                                backref=DB.backref('university', lazy='dynamic'))

    def __init__(self, name, numundergrads, costtoattend, gradrate, publicorprivate):
        self.name = name
        self.numundergrads = numundergrads
        self.costtoattend = costtoattend
        self.gradrate = gradrate
        self.publicorprivate = publicorprivate

    def __repr__(self):
        return '<University ' + self.name + '>'

    # These functions create relationships between Universities and Majors and
    # Ethnicities.
    def addMajor(self, maj):
        """Appends new major to majorList"""
        maj = Major(maj)
        self.majorList.append(maj)

    def addEthnicity(self, eth):
        """Appends new ethnicity to ethnicityList"""
        University.ethnicityList.insert(eth)


class City(DB.Model):
    '''
    Class for City pillar. The name and urbanOrRural variables will be set from API data and the
    universityList, majorList, and ethnicityList will be created from relationships. The population
    and avgTuition variables will be aggregated from university data in universityList.
    '''
    __tablename__ = 'CITY'
    idNum = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(80))
    population = DB.Column(DB.Integer)

    # universityList = DB.relationship(
    #     'University', backref='city', lazy='dynamic')
    # majorList = DB.relationship('Major', secondary=MAJORTOCITY,
    #                             backref=DB.backref('city', lazy='dynamic'))
    # ethnicityList = DB.relationship('Ethnicity', secondary=ETHNICITYTOCITY,
    #                                 backref=DB.backref('city', lazy='dynamic'))

    avgTuition = DB.Column(DB.Integer)
    urbanOrRural = DB.Column(DB.String(80))

    def __init__(self, name, urbanorrural):
        self.name = name
        self.population = 0
        self.avgtuition = 0
        self.urbanorrural = urbanorrural

    def __repr__(self):
        return '<City %r>' % self.name

    # These functions create relationships between Cities and Majors,
    # Ethnicities, and Universities.
    def addUniversity(self, uni):
        """Appends university to universityList"""
        City.universityList.APPend(uni)

    def addMajor(self, maj):
        """Appends major to majorList"""
        City.majorList.APPend(maj)

    def addEthnicity(self, eth):
        """Adds new ethnicity to ethnicityList"""
        City.ethnicityList.APPend(eth)


class Major(DB.Model):
    '''
    Class for Major pillar. The name variable is passed in initially and
    the numUndergrads, gradRate, and avgPercentage are calculated based
    on relationships. This class will include a backref table
    from University (university) and City (city).
    '''
    __tablename__ = 'MAJOR'
    idNum = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(80))
    numUndergrads = DB.Column(DB.Integer)
    gradRate = DB.Column(DB.Float)
    avgPercentage = DB.Column(DB.Float)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Major ' + self.name + '>'


class Ethnicity(DB.Model):
    '''
    Class for Ethnicity pillar. The name variable is passed in initially and the totalCount variable
    is calculated based on the University relationship. This class will include a backref table
    from University (university) and City (city).
    '''
    __tablename__ = 'ETHNICITY'
    idNum = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(80))
    totalCount = DB.Column(DB.Integer)

    def __init__(self, name):
        self.name = name
        self.totalcount = 0

    def __repr__(self):
        return '<Ethnicity %r>' % self.name
