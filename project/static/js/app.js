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
             templateUrl : '../static/partials/table.html',
             controller : 'TableCtrl',
             resolve: {
        		test: function ($route) { $route.current.params.test = "city"; }
    		}
        }).
        when('/universities', {
             templateUrl : '../static/partials/table.html',
             controller : 'TableCtrl',
             resolve: {
        		test: function ($route) { $route.current.params.test = "university"; }
    		}
        }).
        when('/majors', {
             templateUrl : '../static/partials/table.html',
             controller : 'TableCtrl',
             resolve: {
        		test: function ($route) { $route.current.params.test = "major"; }
    		}
        }).
        when('/ethnicities', {
             templateUrl : '../static/partials/table.html',
             controller : 'TableCtrl',
             resolve: {
        		test: function ($route) { $route.current.params.test = "ethnicity"; }
    		}
        }).
        otherwise({
            redirectTo: '/'
        });

});

myApp.controller('TableCtrl',function($scope, $routeParams, $http, $location) {
  $scope.path = '/api/'
  // $scope.urlPath = window.location.pathname;
  $scope.urlPath = $routeParams.test;
  $scope.path = $scope.path + $scope.urlPath;
  $http.get($scope.path).success(function (data, status, headers, config) {
        $scope.myData = data.results;
  });
});
