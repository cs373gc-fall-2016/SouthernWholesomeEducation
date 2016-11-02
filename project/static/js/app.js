'use strict';
var myApp = angular.module('myApp', ['ngRoute']);

myApp.config(function($routeProvider) {
	$routeProvider.
        when('/', {
            templateUrl : '../static/partials/splash.html',
        }).
        when('/about', {
             templateUrl : '../static/partials/about.html',
        }).
        otherwise({
            redirectTo: '/'
        });

});
