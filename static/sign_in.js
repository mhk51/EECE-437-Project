var token = ""
var sign_in_btn = document.getElementById("sign_in_btn")
if (sign_in_btn) { sign_in_btn.addEventListener("click", sign_in()); }
const SERVER_URL = "http://127.0.0.1:5000"


function sign_in() {
    var usn = document.getElementById("user_signup").value
    var pwd = document.getElementById("user_pwd").value
    if (!usn || !pwd) { alert("Please fill all the fields") }

    else {
        data = { "username": usn, "password": pwd }
        fetch(`${SERVER_URL}/authentication`, {
            
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data),
        }).then(response => {
            if (!response.ok) {
                alert("Wrong username or password!")
            }
            return response.json();
        })
        .then(data => {
            saveUserToken(data.token)
            alert("Sign in Successful!")
            window.location.replace("Home_signed.html")
        })



    }
}
function log_out() {

    fetch(`${SERVER_URL}/logout`, {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ "test": "test" }),
    })
}


function saveUserToken(userToken) {
    localStorage.setItem("TOKEN", userToken);
}
function getUserToken() {
    return localStorage.getItem("TOKEN");
}
function clearUserToken() {
    return localStorage.removeItem("TOKEN");
}
