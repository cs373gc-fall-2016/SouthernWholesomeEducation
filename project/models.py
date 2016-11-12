# pylint: disable=E1101, R0913, R0903, R0902, W0611
"""Implements the models that will be used in database"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

APP = Flask(__name__)

APP.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgresql://ec2-user:ec2-user@54.187.105.249/swe'
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
DB = SQLAlchemy(APP)


def create_unique(model, **args):
    """Creates unique model object"""
    is_exist = model.query.filter_by(**args).first()
    if not is_exist:
        is_exist = model(**args)
        DB.session.add(is_exist)
    return is_exist


def get_association(model, **args):
    """Gets model object given arguments"""
    return model.query.filter_by(**args).first()

def get_model(model_name):
    """Gets the model class given model name"""
    model_name = model_name.lower()
    if model_name == 'university':
        return University
    elif model_name == 'city':
        return City
    elif model_name == 'major':
        return Major
    elif model_name == 'ethnicity':
        return Ethnicity

def get_models(model_name):
    """Gets all model objects given model name"""
    if model_name == 'University':
        return University.query.all()
    elif model_name == 'City':
        return City.query.all()
    elif model_name == 'Major':
        temp_list = []
        for t_model in Major.query.distinct(Major.name):
            temp_list.append(t_model)
        return temp_list
    elif model_name == 'Ethnicity':
        temp_list = []
        for t_model in Ethnicity.query.distinct(Ethnicity.name):
            temp_list.append(t_model)
        return temp_list

def get_count(model_name):
    """Get the number of models given model name"""
    if model_name == 'University':
        return University.query.count()
    elif model_name == 'City':
        return City.query.count()
    elif model_name == 'Major':
        return Major.query.distinct(Major.name).count()
    elif model_name == 'Ethnicity':
        return Ethnicity.query.distinct(Ethnicity.name).count()

class MAJORTOCITY(DB.Model):
    """Major to City Association Table"""
    __tablename__ = 'MAJORTOCITY'
    city_id = DB.Column(DB.Integer, DB.ForeignKey(
        'CITY.id_num'), primary_key=True)
    major_id = DB.Column(DB.Integer, DB.ForeignKey(
        'MAJOR.id_num'), primary_key=True)
    num_students = DB.Column(DB.Integer)
    city_name = DB.Column(DB.String(225))
    major_name = DB.Column(DB.String(225))
    major = DB.relationship('Major', backref='cities')
    city = DB.relationship('City', backref='majors')

    def __init__(self, city, major, num_students):
        self.city = city
        self.major = major
        self.num_students = num_students
        self.city_name = self.city.name
        self.major_name = self.major.name

    def attributes(self):
        """Attributes of MAJORTOCITY"""
        return {'city': self.city, 'major': self.major, 'num_students': self.num_students}

    def __repr__(self):
        return '<City ' + self.city.name + ', Major ' + self.major.name + '>'


class ETHNICITYTOCITY(DB.Model):
    """Ethnicity to city association table"""
    __tablename__ = 'ETHNICITYTOCITY'
    city_id = DB.Column(DB.Integer, DB.ForeignKey(
        'CITY.id_num'), primary_key=True)
    ethnicity_id = DB.Column(DB.Integer, DB.ForeignKey(
        'ETHNICITY.id_num'), primary_key=True)
    num_students = DB.Column(DB.Integer)
    city_name = DB.Column(DB.String(225))
    ethnicity_name = DB.Column(DB.String(225))
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

    def attributes(self):
        """Get attributes from ETHNICITYTOCITY"""
        return {'city': self.city, 'ethnicity': self.ethnicity, 'num_students': self.num_students}


class MAJORTOUNIVERSITY(DB.Model):
    """Major to university association table"""
    __tablename__ = 'MAJORTOUNIVERSITY'
    university_id = DB.Column(DB.Integer, DB.ForeignKey(
        'UNIVERSITY.id_num'), primary_key=True)
    major_id = DB.Column(DB.Integer, DB.ForeignKey(
        'MAJOR.id_num'), primary_key=True)
    num_students = DB.Column(DB.Integer)
    university_name = DB.Column(DB.String(225))
    major_name = DB.Column(DB.String(225))
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

    def attributes(self):
        """Get attributes for MAJORTOUNIVERSITY"""
        return {'university': self.university, 'major': self.major, \
            'num_students': self.num_students}


class ETHNICITYTOUNIVERSITY(DB.Model):
    """Ethnicity to university association table"""
    __tablename__ = 'ETHNICITYTOUNIVERSITY'
    university_id = DB.Column(DB.Integer, DB.ForeignKey(
        'UNIVERSITY.id_num'), primary_key=True)
    ethnicity_id = DB.Column(DB.Integer, DB.ForeignKey(
        'ETHNICITY.id_num'), primary_key=True)
    num_students = DB.Column(DB.Integer)
    university_name = DB.Column(DB.String(225))
    ethnicity_name = DB.Column(DB.String(225))
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

    def attributes(self):
        """Attributes for ETHNICITYTOUNIVERSITY"""
        return {'university': self.university, 'ethnicity': self.ethnicity, \
            'num_students': self.num_students}


class University(DB.Model):
    '''
    Class for University pillar. The name, numUndergrads, costToAttend, gradRate
    , and publicOrPrivate variables will be set from API data and the
    ethnicityList and major_list will be created from relationships. A city
    variable will also be included from a backref with the City class.
    '''
    __tablename__ = 'UNIVERSITY'
    id_num = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(225))
    num_undergrads = DB.Column(DB.Integer)
    cost_to_attend = DB.Column(DB.Integer)
    grad_rate = DB.Column(DB.Float)
    public_or_private = DB.Column(DB.String(225))
    city_name = DB.Column(DB.String(225))
    ethnicity_list = DB.relationship('ETHNICITYTOUNIVERSITY')
    major_list = DB.relationship('MAJORTOUNIVERSITY')
    city_name = DB.Column(DB.String(225))

    city_id = DB.Column(DB.Integer, DB.ForeignKey('CITY.id_num'))

    def __init__(self, name, num_undergrads, cost_to_attend, grad_rate, public_or_private, city_name):
        self.name = name
        self.num_undergrads = num_undergrads
        self.cost_to_attend = cost_to_attend
        self.grad_rate = grad_rate
        self.public_or_private = public_or_private
        self.city_name = city_name


    def __repr__(self):
        return '<University ' + self.name + '>'

    def get_ethnicities(self):
        """Get all ethnicities for university"""
        ethnic_list = ETHNICITYTOUNIVERSITY.query.filter_by(university_name=self.name).all()
        ethnic_list_json = []
        for i in ethnic_list:
            ethnic_list_json.append({'name': i.ethnicity_name, \
                'id': i.ethnicity_id, 'num_students': i.num_students})
        return ethnic_list_json

    def get_majors(self):
        """Get all majors for university"""
        maj_list = MAJORTOUNIVERSITY.query.filter_by(university_name=self.name).all()
        major_list_json = []
        for i in maj_list:
            major_list_json.append({'name': i.major_name, \
                'id': i.major_id, 'num_students': i.num_students})
        return major_list_json

    def attributes(self):
        """Get attributes for university"""
        return {
            'id_num': self.id_num,
            'name': self.name,
            'num_undergrads': self.num_undergrads,
            'cost_to_attend': self.cost_to_attend,
            'grad_rate': round(self.grad_rate*100),
            'public_or_private': self.public_or_private,
            'city_id': self.city_id,
            'city_name': self.city_name,
            'majors': self.get_majors(),
            'ethnicities': self.get_ethnicities()
        }

    # These functions create relationships between Universities and Majors and
    # Ethnicities.
    def add_major(self, num, maj):
        """Appends new major to major_list"""
        # major_id = Major.query.filter_by(name=maj).first().id_num
        # assoc = next((a for a in self.major_list if a.major.name == maj.name), None)
        # if not assoc:
        maj.assoc_university = 1
        assoc_maj = MAJORTOUNIVERSITY(self, maj, num)
        self.major_list.append(assoc_maj)

    def add_ethnicity(self, num, eth):
        """Appends new ethnicity to ethnicityList"""
        # assoc = next(
        #     (a for a in self.ethnicity_list if a.ethnicity.name == eth.name), None)
        # if not assoc:
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
    name = DB.Column(DB.String(225))
    population = DB.Column(DB.Integer)
    university_list = DB.relationship(
        'University', backref='city')
    ethnicity_list = DB.relationship('ETHNICITYTOCITY')
    major_list = DB.relationship('MAJORTOCITY')
    avg_tuition = DB.Column(DB.Integer)
    top_university = DB.Column(DB.String(225))
    top_major = DB.Column(DB.String(225))
    top_ethnicity = DB.Column(DB.String(225))
    uni_count = DB.Column(DB.Integer)
    maj_count = DB.Column(DB.Integer)
    eth_count = DB.Column(DB.Integer)

    def __init__(self, name, population=0, avg_tuition=0, top_university='none', \
        top_major='none', top_ethnicity='none', uni_count=0, maj_count=0, eth_count=0):
        self.name = name
        self.population = population
        self.avg_tuition = avg_tuition
        self.top_university = top_university
        self.top_major = top_major.replace( \
            "2014.academics.program_percentage.", "").replace("_", " ").title()
        self.top_ethnicity = top_ethnicity.replace("2014.student.demographics.race_ethnicity.", "")
        self.top_ethnicity = self.top_ethnicity.replace( \
            "2014.student.demographics.race_ethnicity.", "")
        self.top_ethnicity = self.top_ethnicity.replace('nhpi', 'native_hawaiian_pacific_islander')
        self.top_ethnicity = self.top_ethnicity.replace('aian', 'american_indian_alaska_native')
        self.top_ethnicity = self.top_ethnicity.replace("_", " ").title()
        self.uni_count = uni_count
        self.maj_count = maj_count
        self.eth_count = eth_count

    def __repr__(self):
        return '<City ' + self.name + '>'

    def attributes(self):
        """Get attributes for city"""
        return {
            'id_num': self.id_num,
            'name': self.name,
            'population': self.population,
            'uni_count': self.uni_count,
            'eth_count': self.eth_count,
            'maj_count': self.maj_count,
            'avg_tuition': self.avg_tuition,
            'universities': self.get_universities(),
            'majors': self.get_majors(),
            'ethnicities': self.get_ethnicities()
        }

    def get_ethnicities(self):
        """Get ethnicities for city"""
        ethnic_list = ETHNICITYTOCITY.query.filter_by(city_name=self.name).all()
        ethnic_list_json = []
        for i in ethnic_list:
            ethnic_list_json.append({'name': i.ethnicity_name, \
                'id': i.ethnicity_id, 'num_students': i.num_students})
        return ethnic_list_json

    def get_majors(self):
        """Get majors for city"""
        maj_list = MAJORTOCITY.query.filter_by(city_name=self.name).all()
        major_list_json = []
        for i in maj_list:
            major_list_json.append({'name': i.major_name, \
                'id': i.major_id, 'num_students': i.num_students})
        return major_list_json

    def get_universities(self):
        """Get universities for city"""
        uni_list = University.query.filter_by(city_id=self.id_num).all()
        uni_list_json = []
        for i in uni_list:
            uni_list_json.append({'name': i.name, 'id': i.id_num})
        return uni_list_json

    # These functions create relationships between Cities and Majors,
    # Ethnicities, and Universities.
    def add_university(self, uni):
        """Appends university to universityList"""
        # assoc = next((a for a in self.university_list if a.name == uni.name), None)
        # if not assoc:
        self.university_list.append(uni)

    def add_major(self, num, maj):
        """Appends major to major_list"""
        # print(args)
        # assoc = next((a for a in self.major_list if a.major.name == maj.name), None)
        # if not assoc:
        maj.assoc_university = 0
        assoc_maj = MAJORTOCITY(self, maj, num)
        self.major_list.append(assoc_maj)

    def add_ethnicity(self, num, eth):
        """Adds new ethnicity to ethnicity_list"""
        # assoc = next(
        #     (a for a in self.ethnicity_list if a.ethnicity.name == eth.name), None)
        # if not assoc:
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
    name = DB.Column(DB.String(225))
    num_undergrads = DB.Column(DB.Integer)
    top_city = DB.Column(DB.String(225))
    top_city_amt = DB.Column(DB.Integer)
    top_university = DB.Column(DB.String(225))
    top_university_amt = DB.Column(DB.Integer)
    avg_percentage = DB.Column(DB.Float) # to delete?
    assoc_university = DB.Column(DB.Integer)

    def __init__(self, name, num_undergrads=0, top_city='Default', top_city_amt=0, top_university='Default', top_university_amt=0 ,avg_percentage=0):
        name = name.replace("2014.academics.program_percentage.", "")
        name = name.replace("_", " ").title()
        self.name = name
        self.num_undergrads = num_undergrads
        self.top_city = top_city
        self.top_city_amt = top_city_amt
        self.top_university = top_university
        self.top_university_amt = top_university_amt
        self.avg_percentage = avg_percentage # to delte?

    def __repr__(self):
        return '<Major ' + self.name + '>'

    def attributes(self):
        """Get attributes for major"""
        top_city_id = MAJORTOCITY.query.filter_by(major_name=self.name, \
            city_name=self.top_city).first().city_id
        num_cities = len(MAJORTOCITY.query.filter_by(major_name=self.name).all())
        # top_university_id = MAJORTOUNIVERSITY.query.filter_by(major_name=self.name, \
        #     university_name=self.top_university).first().university_id
        return {
            'id_num': self.id_num,
            'name': self.name,
            'num_undergrads': self.num_undergrads,
            'top_city': self.top_city,
            'top_city_amt': self.top_city_amt,
            'top_university': self.top_university,
            'top_university_amt': self.top_university_amt,
            'avg_percentage': self.avg_percentage, # to delete

            'top_city_id': top_city_id, # what is this?
            'num_cities': num_cities  # what is this?
        }


class Ethnicity(DB.Model):
    '''
    Class for Ethnicity pillar. The name variable is passed in initially and the totalCount variable
    is calculated based on the University relationship. This class will include a backref table
    from University (university) and City (city).
    '''
    __tablename__ = 'ETHNICITY'
    id_num = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(225))
    total_count = DB.Column(DB.Integer)
    top_city = DB.Column(DB.String(225))
    top_city_amt = DB.Column(DB.Integer)
    top_university = DB.Column(DB.String(225))
    top_university_amt = DB.Column(DB.Integer)
    assoc_university = DB.Column(DB.Integer)

    def __init__(self, name, total_count=0, top_city='Default', \
        top_city_amt=0, top_university='Default', top_university_amt=0):
        name = name.replace("2014.student.demographics.race_ethnicity.", "")
        name = name.replace('nhpi', 'native_hawaiian_pacific_islander')
        name = name.replace('aian', 'american_indian_alaska_native')
        self.name = name.replace("_", " ").title()
        self.total_count = total_count
        self.top_city = top_city
        self.top_city_amt = top_city_amt
        self.top_university = top_university
        self.top_university_amt = top_university_amt

    def __repr__(self):
        return '<Ethnicity ' + self.name + '>'

    def attributes(self):
        """Get attributes for ethnicity"""
        top_city_id = ETHNICITYTOCITY.query.filter_by(ethnicity_name=self.name, \
            city_name=self.top_city).first().city_id
        top_university_id = ETHNICITYTOUNIVERSITY.query.filter_by(ethnicity_name=self.name, \
            university_name=self.top_university).first().university_id
        num_universities = len(ETHNICITYTOUNIVERSITY.query.filter_by( \
            ethnicity_name=self.name).all())
        num_cities = len(ETHNICITYTOCITY.query.filter_by(ethnicity_name=self.name).all())
        return {
            'id_num': self.id_num,
            'name': self.name,
            'total_count': self.total_count,
            'top_city': self.top_city,
            'top_city_id': top_city_id,
            'top_city_amt': self.top_city_amt,
            'top_university': self.top_university,
            'top_university_id': top_university_id,
            'top_university_amt': self.top_university_amt,
            'num_universities': num_universities,
            'num_cities': num_cities
        }
