angular.module('HookViewer.controllers', []).
	controller('hooksController', function($scope, DataService) {
		$scope.hooks = [];

		DataService.getHooks().success(function (response) {
			$scope.hooks = response.hooks;
		});
	}
);
