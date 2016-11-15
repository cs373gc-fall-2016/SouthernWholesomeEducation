'use strict';
var myApp = angular.module('myApp', ['ngRoute', 'smart-table', 'angular-advanced-searchbox','angularUtils.directives.dirPagination','ngAnimate','vTabs','ui.bootstrap']);

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
        })
    	.otherwise({
            redirectTo: '/'
        });

});

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
    $scope.currentPage = 0;
    $http.get($scope.path+query).success(function (data, status, headers, config) {
      $scope.myData = data.results;
    });
  }


  $scope.page = function(page) {
    $http.get($scope.path+'/'+page).success(function (data, status, headers, config) {
      $scope.myData = data.results;
    });
  }

  $http.get($scope.path).success(function (data, status, headers, config) {
    $scope.myData = data.results;
  });
});

myApp.controller('pipeCtrl', ['Resource', '$location', '$http', function (service, $location, $http) {
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
    var callPath = '/model/' + tableName + '/start/' + start + '/number/' + number + '/attr/' + tableState.sort.predicate + '/reverse/' + tableState.sort.reverse;
    $http.get(callPath).success(function(data) {
      ctrl.displayed = data.results,
      tableState.pagination.numberOfPages = data.numpages
    });
    ctrl.isLoading = false;
  };

}]);

myApp.factory('Resource', ['$q', '$filter', '$timeout', '$http', '$location', function ($q, $filter, $timeout, $http, $location) {
  var map = {"/universities":"University", "/cities":"City", "/majors":"Major", "/ethnicities":"Ethnicity"};
  var tableName = map[$location.path()];
	function getPage(start, number, params) {
    var callPath = '/model/' + tableName + '/start/' + start + '/number/' + number + '/attr/' + params.sort.predicate + '/reverse/' + params.sort.reverse;
		var deferred = $q.defer();
    $http.get(callPath).success(function(data) {
      deferred.resolve({
        data: data.results,
        numberOfPages: data.numpages
      });
    });

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
      $scope.unitTestData = result;
	  });
  }
  $scope.getGithubStats = function() {
	$http.get('/githubstats').success(function (data, status, headers, config) {
		$scope.user_stats = data.user_stats;
    $scope.total_stats = data.total_stats;
	});
  }
});

myApp.controller('SearchCtrl', ['$scope','$http','$sce','$q', function(scope, http, sce,q) {
  scope.rowCollection = [];
  scope.query = "";
  scope.availableSearchParams = [];
  scope.itemsByPage = 10;
  scope.searchType = 'and';
  scope.setSearchType = function(searchType) {
	  scope.searchType = searchType;
  }
  scope.getOR = function(){
	console.log("searching OR");
	if(scope.query.length != 0){
	  scope.getPage(1,2,1);
	  scope.getPage(3,2,1);
	  scope.getPage(4,2,1);
	  scope.getPage(2,2,1);
	}
  };
  scope.getAND = function(){
	console.log("searching AND");
	if(scope.query.length != 0){
	  scope.getPage(1,1,1);
	  scope.getPage(3,1,1);
	  scope.getPage(4,1,1);
	  scope.getPage(2,1,1);
	}
  };

  scope.search = function() {
	if (scope.searchType == 'and') {
	  scope.getAND();
	}
	else if (scope.searchType == 'or') {
	  scope.getOR();
	}
	else {
	  console.log("ERROR: search type should only be 'and' or 'or', not " + scope.searchType);	
	}

  };
  scope.renderHtml = function(html_code) {
	return sce.trustAsHtml(html_code);
  };
  scope.getPage = function(model,op,pagenum) {
	if (model == 1 && op == 1){
	  http.get('/search/University/' + scope.query + '/AND/' + pagenum).success(function (data, status, headers, config) {
		  scope.universityAnd = data.results;
		scope.universityAndPages = data.numpages * 10;
	  });
	} else if (model == 1 && op == 2){
	  http.get('/search/University/' + scope.query + '/OR/' + pagenum).success(function (data, status, headers, config) {
		  scope.universityOr = data.results;
		scope.universityOrPages = data.numpages * 10;
	  });
	} else if (model == 2 && op == 1){
	  http.get('/search/City/' + scope.query + '/AND/' + pagenum).success(function (data, status, headers, config) {
		  scope.cityAnd = data.results;
		scope.cityAndPages = data.numpages * 10;
	  });
	} else if (model == 2 && op == 2){
	  http.get('/search/City/' + scope.query + '/OR/' + pagenum).success(function (data, status, headers, config) {
		  scope.cityOr = data.results;
		scope.cityOrPages = data.numpages * 10;
	  });
	} else if (model == 3 && op == 1){
	  http.get('/search/Major/' + scope.query + '/AND/' + pagenum).success(function (data, status, headers, config) {
		  scope.majorAnd = data.results;
		scope.majorAndPages = data.numpages * 10;
	  });
	} else if (model == 3 && op == 2){
	  http.get('/search/Major/' + scope.query + '/OR/' + pagenum).success(function (data, status, headers, config) {
		  scope.majorOr = data.results;
		scope.majorOrPages = data.numpages * 10;
	  });
	} else if (model == 4 && op == 1){
	  http.get('/search/Ethnicity/' + scope.query + '/AND/' + pagenum).success(function (data, status, headers, config) {
		  scope.ethnicityAnd = data.results;
		scope.ethnicityAndPages = data.numpages * 10;
	  });
	} else if (model == 4 && op == 2){
	  http.get('/search/Ethnicity/' + scope.query + '/OR/' + pagenum).success(function (data, status, headers, config) {
		  scope.ethnicityOr = data.results;
		scope.ethnicityOrPages = data.numpages * 10;
	  });
	}
  };
  scope.$on('advanced-searchbox:modelUpdated', function (event, model) {
	scope.query = model.query;
  });

}]);
