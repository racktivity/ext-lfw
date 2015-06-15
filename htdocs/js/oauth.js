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
        "<div><label for='username'>User name:</label><input type='text' name='username' id='username' placeholder='username' " +
        "class='input.text' /></div><div><label for='password'>Password:</label><input type='password' " +
        "name='password' id='password' placeholder='password' class='input.text' /></div><div><input type='submit' " +
        "name='login' id='login' value='Login' /></div></form> or <a class='oauth' data-provider='github'>Github</a></div>");

    function clearUserInfo() {
        localStorage.removeItem(OAUTH_TOKEN);
        localStorage.removeItem(USER_NAME);
    }

    function showLoginDialog(event) {
        if (event) {
            event.preventDefault();
        }
        clearUserInfo();
        showLoginLink();
        $("#loginDialog").dialog({title: 'Log in',
                                  closeOnEscape: false,
                                  width: 260,
                                  height:200,
                                  resizable: false});
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
        if ((xhr.status === 403 || xhr.status === 401) &&
            options.url.indexOf(LFW_CONFIG.appname + "/appserver/rest/") !== -1) {

            event.preventDefault();
            showLoginDialog();
        } else if (xhr.status === 405) {
            event.preventDefault();
            $.alerterror(xhr);
        }
    });

    //Intercept all Ajax requests to add the OAuth header parameters if any
    $(document).ajaxSend(function(event, xhr, settings) {
        addAuthenticationHeader(xhr, settings);
    });

    //Add the authentication info to the header of all Ajax request
    function addAuthenticationHeader(xhr, settings) {
        if (Auth.getFromLocalStorage(OAUTH_TOKEN) !== null) {
            var completeUrl;
            if (settings.url.charAt(0) === '/') {
                completeUrl = settings.url;
            } else {
                completeUrl = "/" + settings.url;
            }
            //remove the appname from the url
            if (completeUrl.indexOf("/" + LFW_CONFIG.appname) === 0) {
                completeUrl = completeUrl.substr(("/" + LFW_CONFIG.appname).length);
            }
            completeUrl = "http://alkira" + completeUrl;

            var params = OAuth.getParameterMap(settings.data || ""); //convert to object
            //make sure our params are not in the url already
            var q = completeUrl.indexOf('?');
            if (q > 0) {
                var urlParams = OAuth.getParameterMap(completeUrl.substring(q + 1));
                var urlParam;
                for (urlParam in urlParams) {
                    if (urlParams.hasOwnProperty(urlParam) && params.hasOwnProperty(urlParam)) {
                        delete params[urlParam];
                    }
                }
            }

            var accessor = {
                    consumerSecret: "",
                    tokenSecret: ""
                },
                message = {
                    action: completeUrl,
                    method: settings.type,
                    parameters: params
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
    function makeOAuthRequest(username, password, provider) {
        var url = LFW_CONFIG.uris.oauthservice;

        var message = {
            action: url,
            method: "GET",
            parameters: {'user': username,
                         'password': password,
                         'provider': provider
            }
        };

        url = url + '?' + OAuth.formEncode(message.parameters);

        jQuery.ajax({
            type: "GET",
            url: url,
            error: function(xhr, text, exc, options) {
                $("#loginDialog").find("input").attr("disabled", false);
                $.alerterror(xhr, text, exc, options);
            },
            success: function(data) {
                Auth.parseOAuthToken(data);
            }
        });
    }

    $("#loginDialog").find("#login").click(function(event) {
        event.preventDefault();
        if (jQuery.trim( $('#username').val() ) === "" || jQuery.trim( $('#password').val() ) === "") {
            $.alert("Invalid username/password combination!", {title: "Invalid Login"});
            return;
        }
        $("#loginDialog").find("input").attr("disabled", true);
        makeOAuthRequest($('#username').val(), $('#password').val());

    });

    $('#loginDialog').find('.oauth').click(function(e){
        var provider = $(this).data('provider');
        makeOAuthRequest(null, null, provider);
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

        return item.value;
    };

    function getParams() {
        var params = {};
        var search = location.search.substr(1)
        $.each(search.split('&'), function(i, pair) {
            var parts = pair.split('=', 2);
            params[decodeURIComponent(parts[0])] = decodeURIComponent(parts[1]);
        });

        return params;
    }

    Auth.parseOAuthToken = function(token, noreload) {
        if (token.error) {
            $.alert(token.message, {title: 'Invalid login'});
            $("#loginDialog").find("input").attr("disabled", false);
            return;
        }

        if (token.action === 'redirect') {
            //TODO: redirect to provider.
            window.location = token.url;
        } else if (token.action === 'login') {
            var username = token.user;
            addToLocalStorage(OAUTH_TOKEN, token.token);
            showLogoutLink();
            $("#loginInfo #loggeduser").html(username);
            addToLocalStorage(USER_NAME, username);
            $("#loginDialog").dialog("close")
                             .find("input").attr("disabled", false);
            if (!noreload) {
                location = location.origin + location.pathname;
            }
        }
    };

    var urlParams = getParams();
    if ('l' in urlParams) {
        var data = JSON.parse(atob(urlParams.l));
        Auth.parseOAuthToken(data);
    }

    displayUser();
});
