'use strict';
var myApp = angular.module('myApp', ['ngRoute']);

myApp.config(function($routeProvider) {
	$routeProvider.
        when('/', {
            templateUrl : '../static/partials/splash.html'
        }).
        when('/about', {
             templateUrl : '../static/partials/about.html'
        }).
        when('/cities', {
             templateUrl : '../static/partials/cities.html',
             controller : 'TableCtrl',
             resolve: {
                model: function ($route) { $route.current.params.model = "city"; }
    		}
        }).
        when('/universities', {
             templateUrl : '../static/partials/universities.html',
             controller : 'TableCtrl',
             resolve: {
                model: function ($route) { $route.current.params.model = "university"; }
    		}
        }).
        when('/majors', {
             templateUrl : '../static/partials/majors.html',
             controller : 'TableCtrl',
             resolve: {
                model: function ($route) { $route.current.params.model = "major"; }
    		}
        }).
        when('/ethnicities', {
             templateUrl : '../static/partials/ethnicities.html',
             controller : 'TableCtrl',
             resolve: {
                 model: function ($route) { $route.current.params.model = "ethnicity"; }
    		}
        }).
        otherwise({
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

myApp.controller('TableCtrl',function($scope, $routeParams, $http, $location) {
  $scope.path = '/api/'
  $scope.urlPath = $routeParams.model;
  $scope.path = $scope.path + $scope.urlPath;

  $scope.order = 'asc';
  $scope.query = function(query) {
    // $scope.path += '?sort=' + $scope.urlPath + '&order=' + $scope.order;
    
    $http.get($scope.path+query).success(function (data, status, headers, config) {
      $scope.myData = data.results;
    });
  }

  $http.get($scope.path).success(function (data, status, headers, config) {
        $scope.myData = data.results;
  });
});
