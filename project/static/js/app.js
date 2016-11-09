'use strict';
var myApp = angular.module('myApp', ['ngRoute', 'smart-table', 'angular-advanced-searchbox','angularUtils.directives.dirPagination']);

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
             controller : 'pipeCtrl as mc',
        //      resolve: {
        //         model: function ($route) { $route.current.params.model = "city"; }
    		// }
        })
        .when('/universities', {
             templateUrl : '../static/partials/universities.html',
             controller : 'pipeCtrl as mc',
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
             controller : 'pipeCtrl as mc',
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
             controller : 'pipeCtrl as mc',
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
        .when('/search', {
                templateUrl : '../static/partials/search.html',
                controller : 'SearchCtrl',
                // resolve: {
                //     model: function ($route) { $route.current.params.model = "ethnicity"; }
                // }
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

myApp.controller('pipeCtrl', ['Resource', '$location', '$http', function (service, $location, $http) {
  // $route.reload();
  // console.log(tableName);
  var ctrl = this;

  ctrl.rowCollection = [];
  ctrl.displayed = [];
  this.callServer = function callServer(tableState) {
    ctrl.isLoading = true;

    var pagination = tableState.pagination;

    var start = pagination.start || 0;     // This is NOT the page number, but the index of item in the list that you want to use to display the table.
    var number = pagination.number || 10;  // Number of entries showed per page.
    var map = {"/universities":"University", "/cities":"City", "/majors":"Major", "/ethnicities":"Ethnicity"};
    var tableName = map[$location.path()];
    // console.log(tableName);
    var callPath = '/model/' + tableName + '/start/' + start + '/number/' + number + '/attr/' + tableState.sort.predicate + '/reverse/' + tableState.sort.reverse;
    $http.get(callPath).success(function(data) {
      ctrl.displayed = data.results,
      tableState.pagination.numberOfPages = data.numpages
    });
    ctrl.isLoading = false;
    // service.getPage(start, number, tableState).then(function (result) {
    //   // console.log($window.path());
    //   ctrl.rowCollection = result.data;
    //   // ctrl.rowCollection = result.data;
    //   // console.log(result.data);
    //   tableState.pagination.numberOfPages = result.numberOfPages;//set the number of pages so the pagination can update
    //   ctrl.displayed = angular.copy(ctrl.rowCollection);
    //   ctrl.isLoading = false;
    //
    // });

  };

}]);

myApp.factory('Resource', ['$q', '$filter', '$timeout', '$http', '$location', function ($q, $filter, $timeout, $http, $location) {
  var map = {"/universities":"University", "/cities":"City", "/majors":"Major", "/ethnicities":"Ethnicity"};
  var tableName = map[$location.path()];
  // console.log($location.path());
  // console.log(tableName);

	function getPage(start, number, params) {
    // console.log(params);
    var callPath = '/model/' + tableName + '/start/' + start + '/number/' + number + '/attr/' + params.sort.predicate + '/reverse/' + params.sort.reverse;
    // console.log(callPath);
		var deferred = $q.defer();
    // $timeout(function(){
    $http.get(callPath).success(function(data) {
      deferred.resolve({
        data: data.results,
        numberOfPages: data.numpages
      });
    });
    // }, 1500);


		return deferred.promise;
	}

	return {
		getPage: getPage
	};

}]);


myApp.controller('DetailCtrl', function($scope, $routeParams, $http, $location) {
  $scope.path = '/api/';
  $scope.urlPath = $routeParams.model;
  $scope.path = $scope.path + $scope.urlPath +'/id/' + $routeParams.ID;

  $http.get($scope.path).success(function (data, status, headers, config) {
    $scope.myData = data.results;
  });
  $scope.image = function(name) {
    $http.get('/image/'+name).success(function (data, status, headers, config) {
      $scope.imageUrl = data.Image;
    });
  }
});

myApp.controller('AboutCtrl', function($scope, $routeParams, $http, $location) {
  $scope.path = '/api/runUnitTests';
  $scope.runUnitTests = function() {
  	$scope.unitTestData = "Running.............................";
	  $http.get($scope.path).success(function (result) {
      $scope.unitTestData = result.split("\n");
	  });
  }
  $scope.getGithubStats = function() {
	$http.get('/githubstats').success(function (data, status, headers, config) {
		$scope.user_stats = data.user_stats;
    $scope.total_stats = data.total_stats;
	});
  }
});

myApp.controller('SearchCtrl', ['$scope','$http','$sce', function(scope, http, sce) {
  scope.rowCollection = [];
 scope.availableSearchParams = [
];
scope.itemsByPage = 10;
scope.renderHtml = function(html_code) {
  return sce.trustAsHtml(html_code);
};
scope.andResults = [];
scope.orResults = [];
 scope.$on('advanced-searchbox:modelUpdated', function (event, model) {
  // console.log(model.query);
  http.get('/search/' + model.query).success(function (data, status, headers, config) {
		scope.andResults = data.andResults;
    scope.orResults = data.orResults;
	});
});

}]);
