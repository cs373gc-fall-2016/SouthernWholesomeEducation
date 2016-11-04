'use strict';
var myApp = angular.module('myApp', ['ngRoute']);

myApp.config(function($routeProvider) {
	$routeProvider.
        when('/', {
            templateUrl : '../static/partials/splash.html'
        })
        .when('/about', {
             templateUrl : '../static/partials/about.html',
             controller: 'AboutCtrl'
        })
        .when('/cities', {
             templateUrl : '../static/partials/cities.html',
             controller : 'TableCtrl',
             resolve: {
                model: function ($route) { $route.current.params.model = "city"; }
    		}
        })
        .when('/universities', {
             templateUrl : '../static/partials/universities.html',
             controller : 'TableCtrl',
             resolve: {
                model: function ($route) { $route.current.params.model = "university"; }
    		}
        })
        .when('/universities/:ID', {
                templateUrl : '../static/partials/university-detail.html',
                controller : 'DetailCtrl',
                resolve: {
                    model: function ($route) { $route.current.params.model = "university"; }
                }
        })
        .when('/cities/:ID', {
                templateUrl : '../static/partials/city-detail.html',
                controller : 'DetailCtrl',
                resolve: {
                    model: function ($route) { $route.current.params.model = "city"; }
                }
        })
        .when('/majors', {
             templateUrl : '../static/partials/majors.html',
             controller : 'TableCtrl',
             resolve: {
                model: function ($route) { $route.current.params.model = "major"; }
    		}
        })
        .when('/majors/:ID', {
                templateUrl : '../static/partials/major-detail.html',
                controller : 'DetailCtrl',
                resolve: {
                    model: function ($route) { $route.current.params.model = "major"; }
                }
        })
        .when('/ethnicities', {
             templateUrl : '../static/partials/ethnicities.html',
             controller : 'TableCtrl',
             resolve: {
                 model: function ($route) { $route.current.params.model = "ethnicity"; }
    		}
        })
        .when('/ethnicities/:ID', {
                templateUrl : '../static/partials/ethnicity-detail.html',
                controller : 'DetailCtrl',
                resolve: {
                    model: function ($route) { $route.current.params.model = "ethnicity"; }
                }
        })
    	.otherwise({
            redirectTo: '/'
        });

});

// myApp.controller('TableCtrl',function($scope, $routeParams, $http, $location) {
//   $scope.path = '/api/'
//   $scope.urlPath = $routeParams.model;
//   $scope.path = $scope.path + $scope.urlPath;
//   $http.get($scope.path).success(function (data, status, headers, config) {
//         $scope.myData = data.results;
//   });
// });

myApp.controller('TableCtrl', function($scope, $routeParams, $http, $location) {
  $scope.path = '/api/'
  $scope.urlPath = $routeParams.model;
  $scope.path = $scope.path + $scope.urlPath;

	$http.get($scope.path+'/num_pages').success(function (data, status, headers, config) {
		$scope.numPages = data.result;
	});

  $scope.currentPage = 0;
  $scope.prevPage = function() {
    if ($scope.currentPage > 0) {
		  $scope.currentPage--;
      $scope.page($scope.currentPage);
		}
  }

  $scope.nextPage = function() {
    if ($scope.currentPage < $scope.numPages - 1) {
			$scope.currentPage++;
    	$scope.page($scope.currentPage);
		}
  }

  $scope.setPage = function() {
		$scope.currentPage = this.n;
	}

  $scope.order = 'asc';
  $scope.query = function(query) {
    // $scope.path += '?sort=' + $scope.urlPath + '&order=' + $scope.order;
    $scope.currentPage = 0;
    $http.get($scope.path+query).success(function (data, status, headers, config) {
      $scope.myData = data.results;
    });
  }

  $scope.page = function(page) {
    // $scope.path += '?sort=' + $scope.urlPath + '&order=' + $scope.order;

    $http.get($scope.path+'/'+page).success(function (data, status, headers, config) {
      $scope.myData = data.results;
    });
  }

  $http.get($scope.path).success(function (data, status, headers, config) {
    $scope.myData = data.results;
  });
});

myApp.controller('DetailCtrl', function($scope, $routeParams, $http, $location) {
  $scope.path = '/api/';
  $scope.urlPath = $routeParams.model;
  $scope.path = $scope.path + $scope.urlPath +'/id/' + $routeParams.ID;

  $http.get($scope.path).success(function (data, status, headers, config) {
    $scope.myData = data.results;
  });
});

app.controller('AboutCtrl', function($scope, $http, $location) {
  $scope.path = '/api/runUnitTests';
  $scope.runUnitTests = function() {
  	$scope.unitTestData = "Running...";
	  $http.get($scope.path).success(function (result) {
      $scope.unitTestData = result.data;
	  });
  }
});)
