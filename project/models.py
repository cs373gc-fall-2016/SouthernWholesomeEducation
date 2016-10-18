class University(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	universityName = db.Column(db.String(80))
	studentCount = db.Column(db.Integer)
	costToAttend = db.Column(db.Integer)
	salaryAfterGrad = db.Column(db.Integer)
	gradRate = db.Column(db.Float)
    location = db.Column(db.String(80), db.ForeignKey('city.id'))
    publicPrivate = db.Column(db.String(80))

    def __init__(self, studentCount, costToAttend, salaryAfterGrad, gradRate, location, publicPrivate):
        self.studentCount = studentCount
        self.costToAttend = costToAttend
        self.salaryAfterGrad = salaryAfterGrad
        self.gradRate = gradRate
        self.location = location
        self.publicPrivate = publicPrivate

    def __repr__(self):
        return '<University %r>' % self.universityName

class City(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	cityName = db.Column(db.String(80))
	Population = db.Column(db.Integer)
	universityCount = db.relationship('University', backref='city', lazy='dynamic')
	majors = db.relationship('Major', backref='city', lazy='dynamic')
	avgTuition = db.Column(db.Integer)
    urbanRural = db.Column(db.String(80))


    def __init__(self, studentCount, costToAttend, salaryAfterGrad, gradRate, location, publicPrivate):
        self.studentCount = studentCount
        self.costToAttend = costToAttend
        self.salaryAfterGrad = salaryAfterGrad
        self.gradRate = gradRate
        self.location = location
        self.publicPrivate = publicPrivate

    def __repr__(self):
        return '<University %r>' % self.universityName


tags = db.Table('tags',
    db.Column('city_id', db.Integer, db.ForeignKey('city.id')),
    db.Column('major_id', db.Integer, db.ForeignKey('major.id'))
)



# City Name 
# 	Population
# 	Universities in the city
# 	Majors in the city or most popular
# 	average tuition in the city
# 	Urban/Rural

# Austin, TX
# 	1,362,416
# 	UT Austin
# 	Journalism, Engineering, Social Sciences
# 	17,152
# 	Urban

# Los Angeles, CA
# 	12,150,996
# 	University of Southern California
# 	Journalism, Engineering, Social Sciences
# 	28,344
# 	Urban


# Charlottesville, VA
# 	92,359
# 	University of Virginia-Main Campus
# 	Engineering, Social Sciences
# 	17,863
# 	Urban