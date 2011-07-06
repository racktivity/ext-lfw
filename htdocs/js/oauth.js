function getFromLocalStorage(key) {
    var item = JSON.parse(localStorage.getItem(key));
    var now = new Date().getTime().toString();
    if (item === null) {
        return null;
    }
    if (now - item.timestamp > 0) {
        localStorage.removeItem(key);
        alert("The Authentication token has expired!");
        return null;
    }
    return item.value;
}

$(function() {
    var OAUTH_TOKEN = "oauth_token";
    var USER_NAME = "username";

    $('body').append("<div id='loginInfo' name='loginInfo' style='position:absolute; top: 0.3em; right:1em;'" +
        " align='right'></div>");
    $("#loginInfo").append("<div id='logoutDiv' style='display:none';><span id='loggeduser'>" +
        " </span>&nbsp;|&nbsp;<a href='#' id='logout' name='logout'>Log out</a>&nbsp;</div>");
    $("#loginInfo").append("<div id='loginDiv' style='display:none';><a href='#' id='login' name='login'>Log in</a>" +
        "</div>");

    $('body').append("<div id='loginDialog' style='display:none;'>" +
        "<form name='login-form' id='login-form' method='get'>" +
        "<div><label for='username'>User name:</label><input name='username' id='username' placeholder='username' " +
        "class='input.text' /></div><div><label for='password'>Password:</label><input type='password' " +
        "name='password' id='password' placeholder='password' class='input.text' /></div><div><input type='submit' " +
        "name='login' id='login' value='Login' /></div></form></div>");

    $("#loginInfo").find("#login").click(function(event) {
        event.preventDefault();
        $("#loginDialog").dialog({title: 'Log in', closeOnEscape: false, width: 260, height:200, resizable: false});
    });

    $("#loginInfo").find("#logout").click(function(event) {
        event.preventDefault();
        localStorage.removeItem(OAUTH_TOKEN);
        localStorage.removeItem(USER_NAME);
        self.location = "http://" + document.domain + "/" + LFW_CONFIG.appname + "/";
    });

    function showLoginLink() {
        $("#logoutDiv").css("display", "none");
        $("#loginDiv").css("display", "inline");
    }

    function showLogoutLink() {
        $("#loginDiv").css("display", "none");
        $("#logoutDiv").css("display", "inline");
    }

    //Add the authentication info to the header of all Ajax request
    function addAuthenticationHeader() {
        if (getFromLocalStorage(OAUTH_TOKEN) !== null) {
            var tokenKey, tokenSecret;
            var accessor = {
                    consumerSecret: "",
                    tokenSecret: "",
                    token:"",
                    consumerKey:""
                },
                message = {
                    action: "http://alkira",
                    method: "GET",
                    parameters: {}
                };

            var token = getFromLocalStorage(OAUTH_TOKEN);
            if (token !== null) {
                var parts = token.split("&");
                if (parts.length === 2) {
                    var firstPart   = parts[0];
                    var secondPart  = parts[1];
                    if (firstPart.split("=")[0] === "oauth_token") {
                        message.parameters.oauth_token = "token_$(" + firstPart.split("=")[1] + ")";
                        accessor.token = message.parameters.oauth_token;
                        tokenKey = "token_$(" + firstPart.split("=")[1] + ")";
                        tokenSecret = secondPart.split("=")[1];
                        accessor.tokenSecret = secondPart.split("=")[1];
                    } else {
                        message.parameters.oauth_token = "token_$(" + secondPart.split("=")[1] + ")";
                        tokenKey = "token_$(" + secondPart.split("=")[1] + ")";
                        accessor.token = message.parameters.oauth_token;
                        accessor.tokenSecret = firstPart.split("=")[1];
                        tokenSecret = firstPart.split("=")[1];
                    }
                }
            }

            message.parameters.oauth_verifier = "";
            message.parameters.oauth_consumer_key = getFromLocalStorage(USER_NAME);
            accessor.consumerKey = message.parameters.oauth_consumer_key;
            message.parameters.oauth_consumer_secret = "";
            OAuth.setTimestampAndNonce(message);
            OAuth.SignatureMethod.sign(message, accessor);

            //form the OAuth header
            var oauthParams = {
                oauth_consumer_key: message.parameters.oauth_consumer_key,
                oauth_token: tokenKey,
                oauth_verifier: message.parameters.oauth_verifier,
                oauth_nonce: message.parameters.oauth_nonce,
                oauth_timestamp: message.parameters.oauth_timestamp,
                oauth_signature: message.parameters.oauth_signature,
                oauth_signature_method: message.parameters.oauth_signature_method
            };
            jQuery.ajaxSetup({
                'beforeSend': function(xhr) {
                    xhr.setRequestHeader("authorization", OAuth.getAuthorizationHeader("alkira", oauthParams));
                }
            });
        }
        else {
            showLoginLink();
        }
    }

    function displayUser() {
        var username = getFromLocalStorage('username');
        if (username !== null) {
            showLogoutLink();
            $("#loginInfo").find("#loggeduser").html(username);
        }
    }

    function addToLocalStorage(key, value) {
        //The local storage entry is valid for 1 hour
        var data = {timestamp: new Date().getTime() + (60*60*1000), value: value};
        localStorage.setItem(key,  JSON.stringify(data));
    }

    //Token generation function
    function makeOAuthRequest(username, password) {
        var url = LFW_CONFIG.oauthservice;
        url = url.replace("[HOST]", window.location.hostname);

        var message = {
            action: url,
            method: "GET",
            parameters: {'user': username, 'password': password}
        };
        url = url + '?' + OAuth.formEncode(message.parameters);
        jQuery.ajax({
            type: "GET",
            dataType: 'jsonp',
            jsonp: '_jsonp',
            url: url,
            success: function(data){
               addToLocalStorage(OAUTH_TOKEN, data);
               showLogoutLink();
               $("#loginInfo").find("#loggeduser").html(username);
               addToLocalStorage(USER_NAME, username);
               addAuthenticationHeader();
               location.reload();
           }
        });
    }

    $("#loginDialog").find("#login").click(function(event) {
        event.preventDefault();
        if (jQuery.trim( $('#username').val() ) === "" || jQuery.trim( $('#password').val() ) === "") {
            alert("Invalid username/password combination!");
            return;
        }
        makeOAuthRequest($('#username').val(), $('#password').val());
        $("#loginDialog").dialog('close');
    });

    addAuthenticationHeader();
    displayUser();
});
