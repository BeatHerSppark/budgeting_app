// PASSWORD TOGGLE
const passwordToggle = document.getElementById('passwordToggle');
const password1 = document.getElementById("password1");
const password2 = document.getElementById("password2");

passwordToggle.addEventListener("change", () => {
    if(passwordToggle.checked) {
        password1.type = "text";
        password2.type = "text";
    }
    else {
        password1.type = "password";
        password2.type = "password";
    }
})