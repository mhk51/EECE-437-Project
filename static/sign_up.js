var token = "";
var username_field = document.getElementById("username");
var pwd_field = document.getElementById("password");
var repwd_field = document.getElementById("re_password");
var email_field = document.getElementById("mail");
var dob_field = document.getElementById("dob");


var sign_up_btn = document.getElementById("signup_btn");
sign_up_btn.addEventListener("click", create_user());

var SERVER_URL = "http://127.0.0.1:5000"

async function create_user() {

    var usn = username_field.value
    var pwd = pwd_field.value
    var repwd = repwd_field.value
    var email = email_field.value
    var dob = dob_field.value
    if (!usn || !pwd || !repwd || !email || !dob) {
        alert(`Please fill all the field ${usn}`)
    }

    else if (pwd != repwd) {
        alert("Please make sure your paswword and confirmed password match")
    } else {
        var data = { "username": usn, "password": pwd, "mail": email, "dob": dob}
        await fetch(`${SERVER_URL}/add_user`, {
            credentials: 'same-origin',
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
            .then(response => {
                if (!response.ok) { alert("Username already in use!") }
                else { alert("Sign up Successful!"); window.location.replace("Sign_in.html"); }
            })
    }

}