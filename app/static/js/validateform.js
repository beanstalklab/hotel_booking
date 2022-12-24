function validateForm() {
    var mail = document.getElementById("email").value;
    var uname = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    var repassword = document.getElementById("repassword".value);
    var regexMail = new RegExp('[^@]+@[^@]+\.[^@]+');

    //check empty mail field
    if (mail = "") {
        document.getElementById('msg-email').innerHTML = "*test";
        return false;
    } else {
        if (regexMail.test(mail)) {
            document.getElementById('msg-email').innerHTML = "*test";
            return false;
        }
    }

    //check empty name field
    if (uname == "") {
        document.getElementById("msg-name").innerHTML = "**Fill the first name";
        return false;
    }

    //character data validation
    if (!isNaN(uname)) {
        document.getElementById("msg-uname").innerHTML = "**Only characters are allowed";
        return false;
    }

    //check empty password field
    if (password == "") {
        document.getElementById("msg-pass").innerHTML = "**Fill the password please!";
        return false;
    }

    //check empty confirm password field
    if (repassword == "") {
        document.getElementById("msg-repass").innerHTML = "**Enter the password please!";
        return false;
    }

    if (password != repassword) {
        document.getElementById("msg-repass").innerHTML = "**Passwords are not same";
        return false;
    } else {
        alert("Your password created successfully");
        document.write("JavaScript form has been submitted successfully");
    }
}
