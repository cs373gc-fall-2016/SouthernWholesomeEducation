'use strict';
var myApp = angular.module('myApp', ['ngRoute']);

myApp.config(function($routeProvider) {

	$routeProvider.
        when('/', {
            templateUrl : '../partials/splash.html',
        }).
            // when('/university', {
            //     templateUrl : '/static/partials/table.html',
            // }).
            // when('/major', {
            //     templateUrl : '/static/partials/table.html',
            // }).
            // when('/city', {
            //     templateUrl : '/static/partials/table.html',
            // }).
            // when('/ethnicity', {
            //     templateUrl : '/static/partials/table.html',
            // }).
        when('/about', {
             templateUrl : '../partials/about.html',
        }).
        otherwise({
            redirectTo: '/'
        });

});
