OAUTH_TOKEN = "oauth_token";
USER_NAME = "username";
$("#logout").click(function(event) {
    event.preventDefault();
    localStorage.removeItem(OAUTH_TOKEN);
    localStorage.removeItem(USER_NAME);
    location.reload();
});
function doLogin()
{
    if(jQuery.trim( $('#username').val() ) == "" || jQuery.trim( $('#password').val() ) == "")
    {
        alert("Invalid username/password combination!");
        return;
    }
    makeOAuthRequest($('#username').val(), $('#password').val());
    $(loginDialog).dialog('close');
}
addAuthenticationHeader();
displayUser();
//GUID generator
function guidGenerator() {
    var S4 = function() {
    return (((1+Math.random())*0x10000)|0).toString(16).substring(1);
    };
    return (S4()+S4()+"-"+S4()+"-"+S4()+"-"+S4()+"-"+S4()+S4()+S4());
}

//Token generation function
function makeOAuthRequest(username, password)
{
    var url = LFW_CONFIG['oauthservice'];

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
                                   $("#loginInfo").attr("style", ""); 
                                   $("#loggeduser").attr("value",username);
                                   addToLocalStorage(USER_NAME, username);
                               },
    });

}
//Add the authentication info to the header of all Ajax request
function addAuthenticationHeader()
{
    if(getFromLocalStorage(OAUTH_TOKEN) != null)
    {
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
    else
    {
        $(loginDialog).dialog({title: 'Login required', closeOnEscape: false, width: 260, height:200, resizable: false});
    }
}
function displayUser()
{
    var username = getFromLocalStorage('username');
    if(username != null)
    {
        $("#loginInfo").attr("style", "");
        $("#loggeduser").attr("value",username);
    }
}
function addToLocalStorage(key, value)
{
    //The local storage entry is valid for 1 hour
    var data = {timestamp: new Date().getTime() + (60*60*1000), value: value};
    localStorage.setItem(key,  JSON.stringify(data));
}
function getFromLocalStorage(key)
{
    
    var item = JSON.parse(localStorage.getItem(key));
    var now = new Date().getTime().toString();
    if(item == null)
        return null;
    if(now - item.timestamp > 0)
    {
        localStorage.removeItem(key);
        alert("The Authentication token has expired!");
        return null;
    }
    return item.value;
}

