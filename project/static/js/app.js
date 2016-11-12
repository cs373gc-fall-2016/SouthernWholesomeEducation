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
  }).then(function() {
    $scope.imageUri = null;

    if ($scope.myData.name == 'BLACK') {
      $scope.imageUri = 'http://cache2.asset-cache.net/xt/509259793.jpg?v=1&g=fs1|0|FPG|59|793&s=1&b=RjI4';
    } else if ($scope.myData.name == 'WHITE') {
      $scope.imageUri = 'http://cache3.asset-cache.net/xt/555799109.jpg?v=1&g=fs1|0|MIR|99|109&s=1&b=RjI4';
    } else if ($scope.myData.name == 'HISPANIC') {
      $scope.imageUri = 'http://cache2.asset-cache.net/xt/508455394.jpg?v=1&g=fs1|0|EPL|55|394&s=1&b=RjI4';
    } else if ($scope.myData.name == 'ASIAN') {
      $scope.imageUri = 'http://cache2.asset-cache.net/xt/575098377.jpg?v=1&g=fs1|0|FKF|98|377&s=1&b=RjI4';
    } else if ($scope.myData.name == 'American Indian Alaska Native') {
      $scope.imageUri = 'http://cache1.asset-cache.net/xt/115122824.jpg?v=1&g=fs1|0|SKP57|22|824&s=1&b=OEYz';
    } else if ($scope.myData.name == 'Native Hawaiian Pacific Islander') {
      $scope.imageUri = 'http://cache2.asset-cache.net/xt/602287064.jpg?v=1&g=fs1|0|EPL|87|064&s=1&b=RjI4';
    } else if ($scope.myData.name != 'UNKOWN')
      $http({
        method: 'GET',
        url: 'https://api.gettyimages.com/v3/search/images/creative?phrase=' + $scope.myData.name,
        headers: {'Api-Key': 'jcav9s3kv2emua4rvn2d8kkc'}
      })
      .success(function(data) {
        if (data.images.length) {
          var rand = Math.floor(Math.random() * data.images.length);
          $scope.imageUri = data.images[rand].display_sizes[0].uri;
        }
      })
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

myApp.controller('SearchCtrl', ['$scope','$http','$sce','$q', function(scope, http, sce,q) {
  scope.rowCollection = [];
  scope.query = "";
  scope.availableSearchParams = [];
  scope.itemsByPage = 10;
  scope.getOR = function(){
    if(scope.query.length != 0){
    scope.getPage(1,2,1);
    scope.getPage(3,2,1);
    scope.getPage(4,2,1);
    scope.getPage(2,2,1);
  }
  };
  scope.getAND = function(){
    if(scope.query.length != 0){
      scope.getPage(1,1,1);
      scope.getPage(3,1,1);
      scope.getPage(4,1,1);
      scope.getPage(2,1,1);
  }
  };
  scope.renderHtml = function(html_code) {
    return sce.trustAsHtml(html_code);
  };
  scope.getPage = function(model,op,pagenum) {
    // model 1 -> university
    // model 2 -> city
    // model 3 -> major
    // model 4 -> ethnicity
    // op 1 -> and
    // op 2 -> or
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
    // console.log(model.query);
    scope.query = model.query;
    // console.log(scope.query);
    // q.all([http.get('/search/University/'+model.query+'/AND/1'),
    //        http.get('/search/University/'+model.query+'/OR/1'),
    //        http.get('/search/City/'+model.query+'/AND/1'),
    //        http.get('/search/City/'+model.query+'/OR/1'),
    //        http.get('/search/Major/'+model.query+'/AND/1'),
    //        http.get('/search/Major/'+model.query+'/OR/1'),
    //        http.get('/search/Ethnicity/'+model.query+'/AND/1'),
    //        http.get('/search/Ethnicity/'+model.query+'/OR/1')])
    // .then(function(responses) {
    //   scope.universityAnd = responses[0].results;
    //   scope.universityAndPages = responses[0].numpages*10;
    //   scope.universityOr = responses[1].results;
    //   scope.universityOrPages = responses[1].numpages*10;
    //   scope.cityAnd = responses[2].results;
    //   scope.cityAndPages = responses[2].numpages*10;
    //   scope.cityOr = responses[3].results;
    //   scope.cityOrPages = responses[3].numpages*10;
    //   scope.majorAnd = responses[4].results;
    //   scope.majorAndPages = responses[4].numpages*10;
    //   scope.majorOr = responses[5].results;
    //   scope.majorOrPages = responses[5].numpages*10;
    //   scope.ethnicityAnd = responses[6].results;
    //   scope.ethnicityAndPages = responses[6].numpages*10;
    //   scope.ethnicityOr = responses[7].results;
    //   scope.ethnicityOrPages = responses[7].numpages*10;
    // });
    // console.log(scope.universityAndPages);
    // http.get('/search/' + model.query).success(function (data, status, headers, config) {
  	// 	scope.andResults = data.andResults;
    //       scope.orResults = data.orResults;
  	// });
  });

}]);
