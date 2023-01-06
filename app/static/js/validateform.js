// let link = "fa-solid fa-circle-exclamation"; 
var temp = "<i class='fa-solid fa-circle-exclamation'></i>";

var checked = "<i class='fa-solid fa-circle-check' style='color:green;'></i> <span style='color:green;'> Hợp lệ</span>"

function validateLogin() {
    let mail = document.getElementById("email").value;
    let password = document.getElementById("password").value;
    let regexMail = /[^@]+@[^@]+\.[^@]+/;
    let regexPass = /^(?=\S{8,18}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])/

    let check = true

    //check empty mail field
    if (mail.length === 0) {
        document.getElementById('msg-email').innerHTML = temp + "Email không được để trống <br>";
        check = false
    } else {
        if (!regexMail.test(mail)) {
            document.getElementById('msg-email').innerHTML = temp + "Email sai định dạng <br>";
            check = false
        } else {
            document.getElementById('msg-email').innerHTML = "";
        }
    }

    //check empty password field
    if (password.length === 0) {
        document.getElementById("msg-pass").innerHTML = temp + "Mật khẩu không được để trống <br>";
        check = false;
    } else {
        if (!regexPass.test(password)) {
            document.getElementById('msg-pass').innerHTML = temp + "Mật khẩu gồm 8-18 kí tự bao gồm viết thường(a-z), viết hoa(A-Z), số(0-9) <br>";
            check = false
        } else {
            document.getElementById('msg-pass').innerHTML = "";
        }
    }

    return check;
}

function validateRegister() {
    let mail = document.getElementById("email").value;
    let uname = document.getElementById("username").value;
    let password = document.getElementById("password").value;
    let repassword = document.getElementById("repassword").value;
    let regexMail = /[^@]+@[^@]+\.[^@]+/;
    let regexPass = /^(?=\S{8,18}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])/

    console.log(password)

    let check = true

    //check empty mail field
    if (mail.length === 0) {
        document.getElementById('msg-email').innerHTML = temp + "Email không được để trống <br>";
        check = false
    } else {
        if (!regexMail.test(mail)) {
            document.getElementById('msg-email').innerHTML = temp + "Email sai định dạng <br>";
            check = false
        } else {
            document.getElementById('msg-email').innerHTML = checked;
        }
    }

    //check empty name field
    if (uname.length === 0) {
        document.getElementById("msg-name").innerHTML = temp + "Tên không được để trống <br>";
        check = false;
    } else {
        //character data validation
        if (!isNaN(uname)) {
            document.getElementById("msg-name").innerHTML = temp + "Tên chỉ được chứa các kí tự <br>";
            check = false;
        } else {
            document.getElementById("msg-name").innerHTML = checked;
        }
    }

    //check empty password field
    if (password.length === 0) {
        document.getElementById("msg-pass").innerHTML = temp + "Mật khẩu không được để trống <br>";
        check = false;
    } else {
        if (!regexPass.test(password)) {
            document.getElementById('msg-pass').innerHTML = temp + "Mật khẩu gồm 8-18 kí tự bao gồm viết thường(a-z), viết hoa(A-Z), số(0-9) <br>";
            check = false
        } else {
            document.getElementById('msg-pass').innerHTML = checked;

            //check empty confirm password field
            if (password !== repassword) {
                document.getElementById("msg-repass").innerHTML = temp + "Mật khẩu không trùng khớp <br>";
                check = false;
            } else {
                document.getElementById("msg-repass").innerHTML = checked;
            }
        }
    }

    return check;

    // if (!check) {
    //     return false;
    // }
    // alert("Your password created successfully");
    // document.write("JavaScript form has been submitted successfully");
    // return true;
}

function validateReset() {
    let mail = document.getElementById("email").value;
    let password = document.getElementById("password").value;
    let repassword = document.getElementById("repassword").value;
    let regexMail = /[^@]+@[^@]+\.[^@]+/;
    let regexPass = /^(?=\S{8,18}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])/

    let check = true

    //check empty mail field
    if (mail.length === 0) {
        document.getElementById('msg-email').innerHTML = temp + "Email không được để trống <br>";
        check = false
    } else {
        if (!regexMail.test(mail)) {
            document.getElementById('msg-email').innerHTML = temp + "Email sai định dạng <br>";
            check = false
        } else {
            document.getElementById('msg-email').innerHTML = checked;
        }
    }

    //check empty password field
    if (password.length === 0) {
        document.getElementById("msg-pass").innerHTML = temp + "Mật khẩu không được để trống <br>";
        check = false;
    } else {
        if (!regexPass.test(password)) {
            document.getElementById('msg-pass').innerHTML = temp + "Mật khẩu gồm 8-18 kí tự bao gồm viết thường(a-z), viết hoa(A-Z), số(0-9) <br>";
            check = false
        } else {
            document.getElementById('msg-pass').innerHTML = checked;

            //check empty confirm password field
            if (password !== repassword) {
                document.getElementById("msg-repass").innerHTML = temp + "Mật khẩu không trùng khớp <br>";
                check = false;
            } else {
                document.getElementById("msg-repass").innerHTML = checked;
            }
        }
    }

    return check;
}


function validateEditProfile() {
    let firstname = document.getElementById("firstname").value;
    let lastname = document.getElementById("lastname").value;
    let phonenumber = document.getElementById("phonenumber").value;
    let address = document.getElementById("address").value;
    let identify = document.getElementById("identify").value;

    let regexPhone = /[2-9]{1}\d{2}/;

    let check = true;

    if (firstname.length === 0) {
        document.getElementById("firstname-msg").innerHTML = temp + "Thông tin bắt buộc"
        check = false;
    } else {
        document.getElementById("firstname-msg").innerHTML = checked
    }

    if (lastname.length === 0) {
        document.getElementById("lastname-msg").innerHTML = temp + "Thông tin bắt buộc"
        check = false;
    } else {
        document.getElementById("lastname-msg").innerHTML = checked
    } 

    if (phonenumber.length === 0) {
        document.getElementById("phone-msg").innerHTML = temp + "Thông tin bắt buộc";
        check = false;
    } else {
        if (!regexPhone.test(phonenumber)) {
            document.getElementById('phone-msg').innerHTML = temp + "Số điện thoạt không hợp lệ";
            check = false
        } else {
            document.getElementById('phone-msg').innerHTML = checked;
        }
    }

    if (address.length === 0) {
        document.getElementById("address-msg").innerHTML = temp + "Thông tin bắt buộc"
        check = false;
    } else {
        document.getElementById("address-msg").innerHTML = checked
    } 

    if (identify.length === 0) {
        document.getElementById("identify-msg").innerHTML = temp + "Thông tin bắt buộc"
        check = false;
    } else {
        document.getElementById("identify-msg").innerHTML = checked
    } 

    return check;
}