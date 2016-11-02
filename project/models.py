# pylint: disable=E1101, R0913, R0903
"""Implements the models that will be used in database"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

APP = Flask(__name__)

APP.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgresql://ec2-user:ec2-user@localhost/swe'
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
DB = SQLAlchemy(APP)


def create_unique(model, **args):
    is_exist = model.query.filter_by(**args).first()
    if not is_exist:
        is_exist = model(**args)
        DB.session.add(is_exist)
    return is_exist


def add_unique(obj):
    is_exist = obj.__class__.query.filter_by(
        **obj.primary_attributes()).first()
    if not is_exist:
        DB.session.add(obj)
    else:
        is_exist.update(obj)


def get_association(model, **args):
    return model.query.filter_by(**args).first()

def get_models(model_name):
    if model_name == 'University':
        return University.query.all()
    elif model_name == 'City':
        return City.query.all()
    elif model_name == 'Major':
        temp_list = []
        for t in Major.query.distinct(Major.name):
            temp_list.append(t)
        return temp_list
    elif model_name == 'Ethnicity':
        temp_list = []
        for t in Ethnicity.query.distinct(Ethnicity.name):
            temp_list.append(t)
        return temp_list


class MAJORTOCITY(DB.Model):
    __tablename__ = 'MAJORTOCITY'
    city_id = DB.Column(DB.Integer, DB.ForeignKey(
        'CITY.id_num'), primary_key=True)
    major_id = DB.Column(DB.Integer, DB.ForeignKey(
        'MAJOR.id_num'), primary_key=True)
    num_students = DB.Column(DB.Integer)
    city_name = DB.Column(DB.String(80))
    major_name = DB.Column(DB.String(80))
    major = DB.relationship('Major', backref='cities')
    city = DB.relationship('City', backref='majors')

    def __init__(self, city, major, num_students):
        self.city = city
        self.major = major
        self.num_students = num_students
        self.city_name = self.city.name
        self.major_name = self.major.name

    def attributes(self):
        return {'city': self.city, 'major': self.major, 'num_students': self.num_students}

    def primary_attributes(self):
        return {'city': self.city, 'major': self.major}

    def update(self, rhs):
        self.num_students = rhs.num_students

    def __repr__(self):
        return '<City ' + self.city.name + ', Major ' + self.major.name + '>'


class ETHNICITYTOCITY(DB.Model):
    __tablename__ = 'ETHNICITYTOCITY'
    city_id = DB.Column(DB.Integer, DB.ForeignKey(
        'CITY.id_num'), primary_key=True)
    ethnicity_id = DB.Column(DB.Integer, DB.ForeignKey(
        'ETHNICITY.id_num'), primary_key=True)
    num_students = DB.Column(DB.Integer)
    city_name = DB.Column(DB.String(80))
    ethnicity_name = DB.Column(DB.String(80))
    ethnicity = DB.relationship('Ethnicity', backref='cities')
    city = DB.relationship('City', backref='ethnicities')

    def __init__(self, city, ethnicity, num_students):
        self.city = city
        self.ethnicity = ethnicity
        self.num_students = num_students
        self.city_name = self.city.name
        self.ethnicity_name = self.ethnicity.name

    def __repr__(self):
        return '<City ' + self.city.name + ', Ethnicity ' + self.ethnicity.name + '>'

    def primary_attributes(self):
        return {'city': self.city, 'ethnicity': self.ethnicity}

    def attributes(self):
        return {'city': self.city, 'ethnicity': self.ethnicity, 'num_students': self.num_students}

    def update(self, rhs):
        self.num_students = rhs.num_students


class MAJORTOUNIVERSITY(DB.Model):
    __tablename__ = 'MAJORTOUNIVERSITY'
    university_id = DB.Column(DB.Integer, DB.ForeignKey(
        'UNIVERSITY.id_num'), primary_key=True)
    major_id = DB.Column(DB.Integer, DB.ForeignKey(
        'MAJOR.id_num'), primary_key=True)
    num_students = DB.Column(DB.Integer)
    university_name = DB.Column(DB.String(80))
    major_name = DB.Column(DB.String(80))
    major = DB.relationship('Major', backref='universities')
    university = DB.relationship('University', backref='majors')

    def __init__(self, university, major, num_students):
        self.university = university
        self.major = major
        self.num_students = num_students
        self.university_name = self.university.name
        self.major_name = self.major.name

    def __repr__(self):
        return '<University ' + self.university.name + ', Major ' + self.major.name + '>'

    def primary_attributes(self):
        return {'university': self.university, 'major': self.major}

    def attributes(self):
        return {'university': self.university, 'major': self.major, \
            'num_students': self.num_students}

    def update(self, rhs):
        self.num_students = rhs.num_students


class ETHNICITYTOUNIVERSITY(DB.Model):
    __tablename__ = 'ETHNICITYTOUNIVERSITY'
    university_id = DB.Column(DB.Integer, DB.ForeignKey(
        'UNIVERSITY.id_num'), primary_key=True)
    ethnicity_id = DB.Column(DB.Integer, DB.ForeignKey(
        'ETHNICITY.id_num'), primary_key=True)
    num_students = DB.Column(DB.Integer)
    university_name = DB.Column(DB.String(80))
    ethnicity_name = DB.Column(DB.String(80))
    ethnicity = DB.relationship('Ethnicity', backref='universities')
    university = DB.relationship('University', backref='ethnicities')

    def __init__(self, university, ethnicity, num_students):
        self.university = university
        self.ethnicity = ethnicity
        self.num_students = num_students
        self.university_name = self.university.name
        self.ethnicity_name = self.ethnicity.name

    def __repr__(self):
        return '<University ' + self.university.name + ', Ethnicity ' + self.ethnicity.name + '>'

    def primary_attributes(self):
        return {'university': self.university, 'ethnicity': self.ethnicity}

    def attributes(self):
        return {'university': self.university, 'ethnicity': self.ethnicity, \
            'num_students': self.num_students}

    def update(self, rhs):
        self.num_students = rhs.num_students


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
    ethnicity_list = DB.relationship('ETHNICITYTOUNIVERSITY')
    major_list = DB.relationship('MAJORTOUNIVERSITY')

    city_id = DB.Column(DB.Integer, DB.ForeignKey('CITY.id_num'))

    def __init__(self, name, num_undergrads, cost_to_attend, grad_rate, public_or_private):
        self.name = name
        self.num_undergrads = num_undergrads
        self.cost_to_attend = cost_to_attend
        self.grad_rate = grad_rate
        self.public_or_private = public_or_private

    def __repr__(self):
        return '<University ' + self.name + '>'

    def attributes(self):
        return {'name': self.name, 'num_undergrads': self.num_undergrads, 'cost_to_attend': self.cost_to_attend,
                'grad_rate': self.grad_rate, 'public_or_private': self.public_or_private}

    def primary_attributes(self):
        return {'name': self.name, 'city_id': self.city_id}

    def update(self, rhs):
        self.num_undergrads = rhs.num_undergrads
        self.cost_to_attend = rhs.cost_to_attend
        self.grad_rate = rhs.grad_rate
        self.public_or_private = rhs.public_or_private

    # These functions create relationships between Universities and Majors and
    # Ethnicities.
    def add_major(self, num, **args):
        """Appends new major to major_list"""
        # major_id = Major.query.filter_by(name=maj).first().id_num
        assoc = next((a for a in self.major_list if a.major.name == args['name']), None)
        if not assoc:
            maj = Major(**args)
            maj.assoc_university = 1
            assoc_maj = MAJORTOUNIVERSITY(self, maj, num)
            self.major_list.append(assoc_maj)

    def add_ethnicity(self, num, **args):
        """Appends new ethnicity to ethnicityList"""
        assoc = next(
            (a for a in self.ethnicity_list if a.ethnicity.name == args['name']), None)
        if not assoc:
            eth = Ethnicity(**args)
            eth.assoc_university = 1
            assoc_eth = ETHNICITYTOUNIVERSITY(self, eth, num)
            self.ethnicity_list.append(assoc_eth)


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
    university_list = DB.relationship(
        'University', backref='city', lazy='dynamic')
    ethnicity_list = DB.relationship('ETHNICITYTOCITY')
    major_list = DB.relationship('MAJORTOCITY')
    avg_tuition = DB.Column(DB.Integer)

    def __init__(self, name, population=0, avg_tuition=0):
        self.name = name
        self.population = population
        self.avg_tuition = avg_tuition

    def __repr__(self):
        return '<City ' + self.name + '>'

    def attributes(self):
        return {'name': self.name}

    def primary_attributes(self):
        return {'name': self.name}

    def update(self, rhs):
        self.population = rhs.population
        self.avg_tuition = rhs.avg_tuition

    # These functions create relationships between Cities and Majors,
    # Ethnicities, and Universities.
    def add_university(self, uni):
        """Appends university to universityList"""
        assoc = next((a for a in self.university_list if a.name == uni.name), None)
        if not assoc:
            self.university_list.append(uni)

    def add_major(self, num, **args):
        """Appends major to major_list"""
        # print(args)
        assoc = next((a for a in self.major_list if a.major.name == args['name']), None)
        if not assoc:
            maj = Major(**args)
            maj.assoc_university = 0
            assoc_maj = MAJORTOCITY(self, maj, num)
            self.major_list.append(assoc_maj)

    def add_ethnicity(self, num, **args):
        """Adds new ethnicity to ethnicity_list"""
        assoc = next(
            (a for a in self.ethnicity_list if a.ethnicity.name == args['name']), None)
        if not assoc:
            eth = Ethnicity(**args)
            eth.assoc_university = 0
            assoc_eth = ETHNICITYTOCITY(self, eth, num)
            self.ethnicity_list.append(assoc_eth)


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
    top_city = DB.Column(DB.String(80))
    avg_percentage = DB.Column(DB.Float)
    assoc_university = DB.Column(DB.Integer)

    def __init__(self, name, num_undergrads=0, top_city='Default', avg_percentage=0):
        self.name = name
        self.num_undergrads = num_undergrads
        self.top_city = top_city
        self.avg_percentage = avg_percentage

    def __repr__(self):
        return '<Major ' + self.name + '>'

    def attributes(self):
        return {'name': self.name}

    def primary_attributes(self):
        return {'name': self.name}

    def update(self, rhs):
        self.num_undergrads = rhs.num_undergrads
        self.top_city = rhs.top_city
        self.avg_percentage = rhs.avg_percentage


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
    top_city = DB.Column(DB.String(80))
    top_city_amt = DB.Column(DB.Integer)
    top_university = DB.Column(DB.String(80))
    top_university_amt = DB.Column(DB.Integer)
    assoc_university = DB.Column(DB.Integer)

    def __init__(self, name, total_count=0, top_city='Default', top_city_amt=0, top_university='Default', top_university_amt=0):
        self.name = name
        self.total_count = 0
        self.top_city = top_city
        self.top_city_amt = top_city_amt
        self.top_university = top_university
        self.top_university_amt = top_university_amt

    def __repr__(self):
        return '<Ethnicity ' + self.name + '>'

    def attributes(self):
        return {'name': self.name}

    def primary_attributes(self):
        return {'name': self.name}

    def update(self, rhs):
        self.total_count = rhs.total_count
