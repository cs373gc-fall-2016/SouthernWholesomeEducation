app.controller("cityCtrl", function($scope) {
	var dummy = {
		"name": "Austin",
		"student_population": "38,914",
		"university_count": "1",
		"major_list": "3",
		"average_tuition": "$17,152",
		"urban_or_rural": "Urban",
		"ethnicity_count": "3"
	}

    $scope.cities = [dummy];
});

app.controller("ethnicityCtrl", function($scope) {
	var dummy = {
		"name": "Asian",
		"total_undergraduate_population": "12,553",
		"top_city": "Austin, TX",
		"top_university": "University of Texas at Austin",
		"peak_enrollment_year": "2012"
	}

    $scope.ethnicities = [dummy];
});

app.controller("majorCtrl", function($scope) {
	var dummy = {
		"name": "Engineering",
		"undergraduate_population": "8,136",
		"graduation_rate": "53.6%",
		"university_count": "3",
		"city_count": "3",
		"average_percentage": "11.1%"
	}

    $scope.majors = [dummy];
});

app.controller("universityCtrl", function($scope) {
	var dummy = {
		"name": "University of Texas at Austin",
		"undergraduate_population": "38,914",
		"cost_to_attend": "$17,152",
		"graduation_rate": "80%",
		"location": "Austin, TX",
		"public_or_private": "Public",
		"ethnicity_count": "3"
	}

    $scope.universities = [dummy];
});