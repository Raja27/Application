
var app = angular.module('recApp', ['ngRoute']);


app.config(['$routeProvider', '$locationProvider', '$interpolateProvider', '$sceDelegateProvider', '$httpProvider',

    function($routeProvider, $locationProvider, $interpolateProvider, $sceDelegateProvider, $httpProvider) {
        $interpolateProvider.startSymbol('{[{');
        $interpolateProvider.endSymbol('}]}');

        $locationProvider.html5Mode({
            enabled: true,
            requireBase: false
        });
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
        $sceDelegateProvider.resourceUrlWhitelist([
            // Allow same origin resource loads.
            'self',
            // Allow loading from our assets domain.  Notice the difference between * and **.
        ]);
    }
]);