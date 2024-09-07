// PASSWORD TOGGLE
const passwordToggle = document.getElementById('passwordToggle');
const password = document.getElementById("password");

passwordToggle.addEventListener("change", () => {
    if(passwordToggle.checked) {
        password.type = "text";
    }
    else {
        password.type = "password";
    }
})