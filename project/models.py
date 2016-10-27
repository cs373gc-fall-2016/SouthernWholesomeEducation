# pylint: disable=E1101, R0913, R0201, R0903
"""Implements the models that will be used in database"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/swe'

DB = SQLAlchemy(APP)

MAJORTOCITY = DB.Table('MAJORTOCITY',
                       DB.Column('city_id', DB.Integer,
                                 DB.ForeignKey('CITY.id_num')),
                       DB.Column('major_id', DB.Integer,
                                 DB.ForeignKey('MAJOR.id_num')))

ETHNICITYTOCITY = DB.Table('ETHNICITYTOCITY',
                           DB.Column('city_id', DB.Integer,
                                     DB.ForeignKey('CITY.id_num')),
                           DB.Column('ethnicity_id', DB.Integer,
                                     DB.ForeignKey('ETHNICITY.id_num')))

ETHNICITYTOUNIVERSITY = DB.Table('ETHNICITYTOUNIVERSITY',
                                 DB.Column('university_id', DB.Integer,
                                           DB.ForeignKey('UNIVERSITY.id_num')),
                                 DB.Column('ethnicity_id', DB.Integer,
                                           DB.ForeignKey('ETHNICITY.id_num')))

MAJORTOUNIVERSITY = DB.Table('MAJORTOUNIVERSITY',
                             DB.Column('university_id', DB.Integer,
                                       DB.ForeignKey('UNIVERSITY.id_num')),
                             DB.Column('major_id', DB.Integer,
                                       DB.ForeignKey('MAJOR.id_num')))


class University(DB.Model):
    '''
    Class for University pillar. The name, numUndergrads, costToAttend, gradRate
    , and publicOrPrivate variables will be set from API data and the
    ethnicityList and major_list will be created from relationships. A city
    variable will also be included from a backref with the City class.
    '''
    __tablename__ = 'UNIVERSITY'
    id_num = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(80))
    num_undergrads = DB.Column(DB.Integer)
    cost_to_attend = DB.Column(DB.Integer)
    grad_rate = DB.Column(DB.Float)
    public_or_private = DB.Column(DB.String(80))
    ethnicity_list = DB.relationship('Ethnicity', secondary=ETHNICITYTOUNIVERSITY, \
                                    backref=DB.backref('university', lazy='dynamic'))
    major_list = DB.relationship('Major', secondary=MAJORTOUNIVERSITY, \
                                backref=DB.backref('university', lazy='dynamic'))
    city_id = DB.Column(DB.Integer, DB.ForeignKey('CITY.id_num'))

    def __init__(self, name, numundergrads, costtoattend, gradrate, publicorprivate):
        self.name = name
        self.num_undergrads = numundergrads
        self.cost_to_attend = costtoattend
        self.grad_rate = gradrate
        self.public_or_private = publicorprivate

    def __repr__(self):
        return '<University ' + self.name + '>'

    # These functions create relationships between Universities and Majors and
    # Ethnicities.
    def add_major(self, maj):
        """Appends new major to major_list"""
        maj = Major(maj)
        self.major_list.append(maj)

    def add_ethnicity(self, eth):
        """Appends new ethnicity to ethnicityList"""
        self.ethnicity_list.append(Ethnicity(eth))


class City(DB.Model):
    '''
    Class for City pillar. The name and urbanOrRural variables will be set from API data and the
    universityList, major_list, and ethnicityList will be created from relationships. The population
    and avgTuition variables will be aggregated from university data in universityList.
    '''
    __tablename__ = 'CITY'
    id_num = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(80))
    population = DB.Column(DB.Integer)
    major_list = DB.relationship('Major', secondary=MAJORTOCITY, \
                                backref=DB.backref('city', lazy='dynamic'))
    ethnicity_list = DB.relationship('Ethnicity', secondary=ETHNICITYTOCITY, \
                                    backref=DB.backref('city', lazy='dynamic'))
    university_list = DB.relationship('University', backref='city', lazy='dynamic')
    avg_tuition = DB.Column(DB.Integer)
    urban_or_rural = DB.Column(DB.String(80))

    def __init__(self, name, urbanorrural):
        self.name = name
        self.population = 0
        self.avg_tuition = 0
        self.urban_or_rural = urbanorrural

    def __repr__(self):
        return '<City ' + self.name + '>'

    # These functions create relationships between Cities and Majors,
    # Ethnicities, and Universities.
    def add_university(self, uni):
        """Appends university to universityList"""
        self.university_list.append(uni)

    def add_major(self, maj):
        """Appends major to major_list"""
        self.major_list.append(Major(maj))

    def add_ethnicity(self, eth):
        """Adds new ethnicity to ethnicity_list"""
        self.ethnicity_list.append(Ethnicity(eth))


class Major(DB.Model):
    '''
    Class for Major pillar. The name variable is passed in initially and
    the numUndergrads, gradRate, and avgPercentage are calculated based
    on relationships. This class will include a backref table
    from University (university) and City (city).
    '''
    __tablename__ = 'MAJOR'
    id_num = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(80))
    num_undergrads = DB.Column(DB.Integer)
    grad_rate = DB.Column(DB.Float)
    avg_percentage = DB.Column(DB.Float)

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
    id_num = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(80))
    total_count = DB.Column(DB.Integer)


    def __init__(self, name):
        self.name = name
        self.total_count = 0

    def __repr__(self):
        return '<Ethnicity ' + self.name + '>'
