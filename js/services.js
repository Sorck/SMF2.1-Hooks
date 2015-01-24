angular.module('HookViewer.services', []).
	factory('DataService', function($http) {
		var DataService = {};
		DataService.getHooks = function() {
			return $http.get('hooks.json');
		}
		return DataService;
	}
);
