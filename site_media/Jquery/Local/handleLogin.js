var path_to_redirect = "/all_story/"; //path for redirection if login successful or user already logged in
var token = localStorage.getItem('token');
$(document).ready(function() {
    if (typeof token != 'undefined' && token != ''){ //if user is already logged in redirect to all story page
        if(token != '') window.location.href = path_to_redirect;
    }

    window.history.pushState(null, "", window.location.href);
        window.onpopstate = function() {
            window.history.pushState(null, "", window.location.href);
    };

    //if login button is clicked
    $("#loginbtn").click(function(e) {
        e.preventDefault();
        login_func();
    });

    //if ender is pressed during login
    $('#username, #password').live('keydown', function(e) {
        if (e.keyCode == 13) {
            e.preventDefault();
            login_func();
        }
    });

    //if sign up button is clicked
    $("#sign_up").click(function(e) {
        sign_up();
    });
});

//handles user login
function login_func() {
    var username = $("#username").val().trim();
    var password = $("#password").val();
    if (!username || !password) {
        alertify.set({
            delay: 300000
        });
        alertify.error("Username or password cannot be emtpy");
        return;
    }
    $("#loginbtn").html("Logging in...");
    $("#loginbtn").prop("disabled", true);

    //calls login api
    $.ajax({
        url: "login/",
        data: {
            "username": username,
            "password": password
        },
        type: "POST",
        dataType: "json",
        success: function(data) {
            if (data['code'] === '0') { //login unsuccessful
                $("#loginbtn").html("Try again");
                $("#loginbtn").removeClass("blue");
                $("#loginbtn").addClass("red");
                setTimeout(() => {
                    $("#loginbtn").html("Login");
                    $("#loginbtn").removeClass("red");
                    $("#loginbtn").addClass("blue");
                    $("#loginbtn").prop("disabled", false);
                }, 2000);
                alertify.set({
                    delay: 300000
                });
                alertify.error(data['message']);
                $("#password").val("");
            } else if (data['code'] === "1") { //login successful, saves username and token and redirects to all story page
                $("#loginbtn").html("Success");
                $("#loginbtn").removeClass("blue");
                $("#loginbtn").addClass("dark");

                $.session.set('user', username);
                $.session.set('token', data['token']);
                $.session.set('logged_in', "yes");
                localStorage.setItem("user", username);
                localStorage.setItem('token', data['token']);
                localStorage.setItem('logged_in', "yes");

                window.location.href = path_to_redirect;
            } else { // something is wrong with the server, it shouldn't have come here
                alertify.set({
                    delay: 300000
                });
                alertify.error("Something went wrong! Please check server settings.");
                $("#loginbtn").html("Error");
                $("#loginbtn").removeClass("blue");
                $("#loginbtn").addClass("red");
                setTimeout(() => {
                    $("#loginbtn").html("Login");
                    $("#loginbtn").removeClass("red");
                    $("#loginbtn").addClass("blue");
                    $("#loginbtn").prop("disabled", false);
                }, 2000);
            }
        }
    });
}


//handles new user sign up
function sign_up() {
    var user_name = $('#signup_username').val().trim();
    var password1 = $('#signup_password1').val().trim();
    var password2 = $('#signup_password2').val().trim();

    if (!user_name || !password1 || !password2) {
        alertify.error('Required fields are empty!');
    }

    if (password1!=password2) {
        alertify.error('Passwords must match!!!');
    }

    //calls signup api
    $.ajax({
        url: "signup/",
        data: {
            'username': user_name,
            'password1': password1,
            'password2': password2
        },
        type: "POST",
        dataType: "json",
        success: function(data) {
            if (data['code'] === '0') { //if signup is unsuccessful
                alertify.error(data['message']);
                reset_fields();
                return;
            }  else if (data['code'] === '1') { //if signup is successful,save user and token and redirect
                alertify.success("Sign up successful!");
                $.session.set('user', username);
                $.session.set('token', data['token']);
                $.session.set('logged_in', "yes");
                localStorage.setItem("user", username);
                localStorage.setItem('token', data['token']);
                localStorage.setItem('logged_in', "yes");

                window.location.href = path_to_redirect;
            } else {
                alertify.error("Sorry! Sign up failed. Please try again.");
                reset_fields();
            }
        }
    });
}

//resets signup fields
function reset_fields() {
    $('#signup_username').val('');
    $('#signup_password1').val('');
    $('#signup_password2').val('');
}
