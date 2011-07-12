var Auth = {};

$(function() {
    var OAUTH_TOKEN = "oauth_token";
    var USER_NAME = "username";

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

    function clearUserInfo() {
        localStorage.removeItem(OAUTH_TOKEN);
        localStorage.removeItem(USER_NAME);
    };

    function showLoginDialog(event) {
        if (event) {
            event.preventDefault();
        }
        clearUserInfo();
        showLoginLink();
        $("#loginDialog").dialog({title: 'Log in', closeOnEscape: false, width: 260, height:200, resizable: false});
    }

    $("#loginInfo").find("#login").click(showLoginDialog);

    $("#loginInfo").find("#logout").click(function(event) {
        event.preventDefault();
        clearUserInfo();
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

    //Install global error handler so we can show a login box if required but only if we got it from the rest api
    //from the applicationserver
    $(document).ajaxError(function(event, xhr, options) {
        if (xhr.status === 403 && options.url.indexOf(LFW_CONFIG.appname + "/appserver/rest/") !== -1) {
            showLoginDialog();
        }
    });
    //Intercept all Ajax requests to add the OAuth header parameters if any
    $(document).ajaxSend(
        function(event, xhr, settings)
        {
            addAuthenticationHeader(xhr, settings.url);
        }
    );

    //Add the authentication info to the header of all Ajax request
    function addAuthenticationHeader(xhr, url) {
        if (Auth.getFromLocalStorage(OAUTH_TOKEN) !== null) {
            var completeUrl = "http://alkira";
            if(url.charAt(0) == '/')
            {
                completeUrl += url;
            }
            else
            {
                completeUrl += "/" + url;
            }
            
            var accessor = {
                    consumerSecret: "",
                    tokenSecret: "",
                    token:"",
                    consumerKey:""
                },
                message = {
                    action: completeUrl,
                    method: "GET",
                    parameters: {}
                };
            var token = Auth.getFromLocalStorage(OAUTH_TOKEN);
            if (token !== null) {
                var parts = token.split("&");
                if (parts.length === 2) {
                    var firstPart   = parts[0];
                    var secondPart  = parts[1];
                    if (firstPart.split("=")[0] === "oauth_token") {
                        message.parameters.oauth_token = "token_$(" + firstPart.split("=")[1] + ")";
                        accessor.token = message.parameters.oauth_token;
                        accessor.tokenSecret = secondPart.split("=")[1];
                    } else {
                        message.parameters.oauth_token = "token_$(" + secondPart.split("=")[1] + ")";
                        accessor.token = message.parameters.oauth_token;
                        accessor.tokenSecret = firstPart.split("=")[1];
                    }
                }
            }

            message.parameters.oauth_verifier = "";
            message.parameters.oauth_consumer_key = Auth.getFromLocalStorage(USER_NAME);
            accessor.consumerKey = message.parameters.oauth_consumer_key;
            message.parameters.oauth_consumer_secret = "";
            OAuth.setTimestampAndNonce(message);
            OAuth.SignatureMethod.sign(message, accessor);

            //form the OAuth header
            var oauthParams = {
                oauth_consumer_key: message.parameters.oauth_consumer_key,
                oauth_token: message.parameters.oauth_token,
                oauth_verifier: message.parameters.oauth_verifier,
                oauth_nonce: message.parameters.oauth_nonce,
                oauth_timestamp: message.parameters.oauth_timestamp,
                oauth_signature: message.parameters.oauth_signature,
                oauth_signature_method: message.parameters.oauth_signature_method
            };

            xhr.setRequestHeader("authorization", OAuth.getAuthorizationHeader("alkira", oauthParams));
        }
        else {
            showLoginLink();
        }
    }

    function displayUser() {
        var username = Auth.getFromLocalStorage(USER_NAME);
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
            success: function(data) {
                Auth.parseOAuthToken(data, username);
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

    Auth.getFromLocalStorage = function(key) {
        var itemJson = localStorage.getItem(key);
        if (!itemJson) {
            return null;
        }
        var item = $.parseJSON(itemJson);
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
    };

    Auth.parseOAuthToken = function(token, username, noreload) {
        addToLocalStorage(OAUTH_TOKEN, token);
        showLogoutLink();
        $("#loginInfo #loggeduser").html(username);
        addToLocalStorage(USER_NAME, username);
        if (!noreload) {
            location.reload();
        }
    };

    displayUser();
});
