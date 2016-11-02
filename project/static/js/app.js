var app = angular.module('Myapp', ['ngRoute']);

app.config(function($routeProvider) {

	$routeProvider.
            when('/', {
                templateUrl : '/static/partials/splash.html',
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
                templateUrl : '/static/partials/about.html',
            }).
            otherwise({
                 redirectTo: '/'
             });

});
