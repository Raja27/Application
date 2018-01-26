
app.controller('loginController', function ($scope, $http, $location, $window) {
    $scope.email = null;
    $scope.password = null;
    
    $scope.login_view = function(){
        $window.location.href = '/login/';
    };
    
    $scope.login = function(){
        console.log($scope.data);
        $http({
             method: "POST",
             url: '/api/login/',
             async: true,
             crossDomain: true,
             headers: {
                         'Content-Type': 'application/json',
                       },
             data: {email: $scope.email, password: $scope.password}
           }).then(function mySuccess(response) {
             console.log(response.data);
             sessionStorage.setItem('auth_token', response.data.auth_token);
             $window.location.href = '/applications';
           }, function myError(response) {
               console.log(response)
               swal("Login Error")

        });
    };

    $scope.logout = function(){
        console.log($scope.data);
        $http({
             method: "POST",
             url: '/api/logout/',
             async: true,
             crossDomain: true,
             headers: {
                         'Content-Type': 'application/json',
                         'Authorization' : sessionStorage.getItem('auth_token')
                       },
             data: {email: $scope.email, password: $scope.password}
           }).then(function mySuccess(response) {
             console.log(response.data);
             sessionStorage.removeItem('auth_token');
             $window.location.href = '/';

           });
    };
});


app.controller('appController', function ($scope, $http, $location, $window) {

    $scope.getList = function (next_url) {

        if (next_url){
            var url = next_url
        } else {
            var url = '/api/application/list/';
        }

        $http({
             method: 'GET',
             url: url,
             async: true,
             crossDomain: true,
             headers: {
                         'Content-Type': 'application/json',
                         'Authorization' : sessionStorage.getItem('auth_token')
                       },
             data: {'token' : $scope.auth_token}
           }).then(function mySuccess(response) {
             console.log(response.data);
            $scope.data = response.data;
           }, function error(response) {
               console.log(response.status);
               if (response.status == 401){
                   $window.location.href = '/login/';
                   console.log(response.status);
               }
        });
    };

    $scope.detailView = function (detail_id) {
        $window.location.href = '/applications/detail/#' + detail_id ;
    };

    $scope.getAppNo = function () {
        $scope.app_no = window.location.hash.substr(1) ;
    };

    $scope.goHome = function () {
        console.log('1234');
        $scope.app_no = null ;
        $window.location.href = '/';
    };

    $scope.detail = function () {

        $http({
             method: 'GET',
             url: '/api/application/detail/' + window.location.hash.substr(1) + '/',
             async: true,
             crossDomain: true,
             headers: {
                         'Content-Type': 'application/json',
                         'Authorization' : sessionStorage.getItem('auth_token')
                       },
             data: {'token' : $scope.auth_token}
           }).then(function mySuccess(response) {
             console.log(response.data);
            $scope.data = response.data;
           }, function error(response) {
               console.log(response.status);
               if (response.status == 401){
                   $window.location.href = '/login/';
                   console.log(response.status);
               }
        });
    };

    $scope.createApplication = function(data){
        console.log(data);

        var form = new FormData();
        form.append("name", data.name);
        form.append("dob", data.dob);
        form.append("email", data.email);
        form.append("phone_no", data.phone_no);
        form.append("phone_code", data.phone_code);
        form.append("skills", data.skills);
        form.append("resume", data.resume_file);

        var settings = {
          "async": true,
          "crossDomain": true,
          "url": "/api/application/create",
          "method": "POST",
          "headers": {
            "Content-Type": "multipart/form-data",
          },
          "processData": false,
          "contentType": false,
          "mimeType": "multipart/form-data",
          "data": form
        }

        $http(settings).then(function mySuccess(response) {
             console.log(response.data);
                swal("Accepted", response.data.status_message)
                    .then(
                      $window.location.href = '/applications'
                );
           });
    };

    $scope.accepted = function(app_id){
        $http({
             method: 'PUT',
             url: '/api/application/edit/' + app_id + '/',
             async: true,
             crossDomain: true,
             headers: {
                         'Content-Type': 'application/json',
                         'Authorization' : sessionStorage.getItem('auth_token')
                       },
             data: {'status' : 'Accepted'}
           }).then(function mySuccess(response) {
             console.log(response.data);
                swal("Accepted", response.data.status_message)
                    .then(
                      $window.location.href = '/applications'
                );
           }, function error(response) {
               console.log(response.status);
               if (response.status == 401){
                   $window.location.href = '/login/';
                   console.log(response.status);
               }
        });
    };

    $scope.rejected = function(app_id){
        $http({
             method: 'PUT',
             url: '/api/application/edit/' + app_id + '/',
             async: true,
             crossDomain: true,
             headers: {
                         'Content-Type': 'application/json',
                         'Authorization' : sessionStorage.getItem('auth_token')
                       },
             data: {'status' : 'Rejected'}
           }).then(function mySuccess(response) {
             console.log(response.data);

                swal("Rejected", response.data.status_message)
                    .then(
                          $window.location.href = '/applications'
                    );
           }, function error(response) {
               console.log(response.status);
               if (response.status == 401){
                   $window.location.href = '/login/';
                   console.log(response.status);
               }
        });
    };

});

