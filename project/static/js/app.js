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
        .when('/visualization', {
             templateUrl : '../static/partials/visualization.html',
             // controller: 'VisualizationCtrl'
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
  $scope.majors = [];
  $scope.ethnicities = [];
  $scope.universities = [];
  $scope.majsort = function(keyname){
        if (angular.isUndefined($scope.majreverse)) {
          $scope.majreverse = false;
        } else {

          $scope.majreverse = !$scope.majreverse; //if true make it false and vice versa
        }
        if ($scope.majsortKey != keyname) {
          $scope.majreverse = false;
        }
        $scope.majsortKey = keyname;   //set the sortKey to the param passed
  };
  $scope.ethsort = function(keyname){
        if (angular.isUndefined($scope.ethreverse)) {
          $scope.ethreverse = false;
        } else {

          $scope.ethreverse = !$scope.ethreverse; //if true make it false and vice versa
        }
        if ($scope.ethsortKey != keyname) {
          $scope.ethreverse = false;
        }
        $scope.ethsortKey = keyname;   //set the sortKey to the param passed
  };
  $scope.unisort = function(keyname){
        if (angular.isUndefined($scope.unireverse)) {
          $scope.unireverse = false;
        } else {

          $scope.unireverse = !$scope.unireverse; //if true make it false and vice versa
        }
        if ($scope.unisortKey != keyname) {
          $scope.unireverse = false;
        }
        $scope.unisortKey = keyname;   //set the sortKey to the param passed
  };
  $http.get($scope.path).success(function (data, status, headers, config) {
    $scope.myData = data.results;
    if($routeParams.model == "university" || $routeParams.model == "city"){
        $scope.majors = $scope.myData.majors;
        $scope.ethnicities = $scope.myData.ethnicities;
    }
    if($routeParams.model == "city") {
      $scope.universities = $scope.myData.universities;
    }
  }).then(function() {
    $scope.imageUri = null;
    var name = $scope.myData.name.toLowerCase();

    if (name == 'BLACK'.toLowerCase()) {
      $scope.imageUri = 'http://cache2.asset-cache.net/xt/509259793.jpg?v=1&g=fs1|0|FPG|59|793&s=1&b=RjI4';
    } else if (name == 'WHITE'.toLowerCase()) {
      $scope.imageUri = 'http://cache3.asset-cache.net/xt/555799109.jpg?v=1&g=fs1|0|MIR|99|109&s=1&b=RjI4';
    } else if (name == 'HISPANIC'.toLowerCase()) {
      $scope.imageUri = 'http://cache2.asset-cache.net/xt/508455394.jpg?v=1&g=fs1|0|EPL|55|394&s=1&b=RjI4';
    } else if (name == 'ASIAN'.toLowerCase()) {
      $scope.imageUri = 'http://cache2.asset-cache.net/xt/575098377.jpg?v=1&g=fs1|0|FKF|98|377&s=1&b=RjI4';
    } else if (name == 'American Indian Alaska Native'.toLowerCase()) {
      $scope.imageUri = 'http://cache1.asset-cache.net/xt/115122824.jpg?v=1&g=fs1|0|SKP57|22|824&s=1&b=OEYz';
    } else if (name == 'Native Hawaiian Pacific Islander'.toLowerCase()) {
      $scope.imageUri = 'http://cache2.asset-cache.net/xt/602287064.jpg?v=1&g=fs1|0|EPL|87|064&s=1&b=RjI4';
    } else if(name == 'TWO OR MORE'.toLowerCase() || name == 'UNKNOWN'.toLowerCase()) {
      $scope.imageUri = 'http://cache2.asset-cache.net/xt/532969250.jpg?v=1&g=fs1|0|EPL|69|250&s=1&b=RjI4';
    } else if (name != 'NON RESIDENT ALIEN'.toLowerCase()) {
      $http({
        method: 'GET',
        url: 'https://api.gettyimages.com/v3/search/images/creative?phrase=' + name,
        headers: {'Api-Key': 'jcav9s3kv2emua4rvn2d8kkc'}
      })
      .success(function(data) {
        if (data.images.length) {
          var rand = Math.floor(Math.random() * data.images.length);
          $scope.imageUri = data.images[rand].display_sizes[0].uri;
        } else {
          $scope.imageUri = 'http://cache2.asset-cache.net/xt/452716295.jpg?v=1&g=fs1|0|DV|16|295&s=1&b=RTRE';
        }
      })
    }
  });
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


// myApp.controller('VisualizationCtrl', function($scope, $routeParams, $http, $location) {
//   $scope.path = 'blablabla';
//   $scope.getVisualization = function() {
//     $http.get('http://opensourcery.me/api/projects/1').success(function (data, status, headers, config) {
//       $scope.rec_data = data;
//     });
//   }
// });

myApp.controller('SearchCtrl', ['$scope','$http','$sce','$q', '$timeout', function($scope, http, sce,q, $timeout) {
  $scope.rowCollection = [];
  $scope.query = "";
  $scope.availableSearchParams = [];
  $scope.itemsByPage = 10;
  $scope.searchType = 'and';
  $scope.setSearchType = function(searchType) {
	  $scope.searchType = searchType;
  }
  $scope.getOR = function(){
	if($scope.query.length != 0){
	  $scope.getPage(1,2,1);
	  $scope.getPage(3,2,1);
	  $scope.getPage(4,2,1);
	  $scope.getPage(2,2,1);
	}
  };
  $scope.getAND = function(){
	if($scope.query.length != 0){
	  $scope.getPage(1,1,1);
	  $scope.getPage(3,1,1);
	  $scope.getPage(4,1,1);
	  $scope.getPage(2,1,1);
	}
  };

  $scope.search = function() {
	$timeout(function() {
		if ($scope.searchType == 'and') {
		  $scope.getAND();
		}
		else if ($scope.searchType == 'or') {
		  $scope.getOR();
		}
		else {
		  console.log("ERROR: search type should only be 'and' or 'or', not " + $scope.searchType);
		}
	  }, 1000);
  };

  $scope.renderHtml = function(html_code) {
	return sce.trustAsHtml(html_code);
  };
  $scope.getPage = function(model,op,pagenum) {
	if (model == 1 && op == 1){
	  http.get('/search/University/' + $scope.query + '/AND/' + pagenum).success(function (data, status, headers, config) {
		  $scope.universityAnd = data.results;
		$scope.universityAndPages = data.numpages * 10;
	  });
	} else if (model == 1 && op == 2){
	  http.get('/search/University/' + $scope.query + '/OR/' + pagenum).success(function (data, status, headers, config) {
		  $scope.universityOr = data.results;
		$scope.universityOrPages = data.numpages * 10;
	  });
	} else if (model == 2 && op == 1){
	  http.get('/search/City/' + $scope.query + '/AND/' + pagenum).success(function (data, status, headers, config) {
		  $scope.cityAnd = data.results;
		$scope.cityAndPages = data.numpages * 10;
	  });
	} else if (model == 2 && op == 2){
	  http.get('/search/City/' + $scope.query + '/OR/' + pagenum).success(function (data, status, headers, config) {
		  $scope.cityOr = data.results;
		$scope.cityOrPages = data.numpages * 10;
	  });
	} else if (model == 3 && op == 1){
	  http.get('/search/Major/' + $scope.query + '/AND/' + pagenum).success(function (data, status, headers, config) {
		  $scope.majorAnd = data.results;
		$scope.majorAndPages = data.numpages * 10;
	  });
	} else if (model == 3 && op == 2){
	  http.get('/search/Major/' + $scope.query + '/OR/' + pagenum).success(function (data, status, headers, config) {
		  $scope.majorOr = data.results;
		$scope.majorOrPages = data.numpages * 10;
	  });
	} else if (model == 4 && op == 1){
	  http.get('/search/Ethnicity/' + $scope.query + '/AND/' + pagenum).success(function (data, status, headers, config) {
		  $scope.ethnicityAnd = data.results;
		$scope.ethnicityAndPages = data.numpages * 10;
	  });
	} else if (model == 4 && op == 2){
	  http.get('/search/Ethnicity/' + $scope.query + '/OR/' + pagenum).success(function (data, status, headers, config) {
		  $scope.ethnicityOr = data.results;
		$scope.ethnicityOrPages = data.numpages * 10;
	  });
	}
  };
  $scope.$on('advanced-searchbox:modelUpdated', function (event, model) {
	$scope.query = model.query;
  });

}]);
