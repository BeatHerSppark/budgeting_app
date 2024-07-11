const burgerMenu = document.getElementById("toggle-btn");
const sidebarLogo = document.querySelector(".sidebar-logo")

// SIDEBAR LOGIC
window.onload = () => {
    document.getElementById("sidebar").classList.toggle("expand");
}

burgerMenu.addEventListener("click", () => {
    document.getElementById("sidebar").classList.toggle("collapse");
})

sidebarLogo.addEventListener("click", () => {
    document.getElementById("sidebar").classList.toggle("collapse");
})

// DATE PICKER LOGIC
const btnsDateMode = document.querySelectorAll(".btnDateMode");

// Adding/remove style for selected date mode and calling handle function
btnsDateMode.forEach(btn => {
    btn.addEventListener("click", (e) => {
        btnsDateMode.forEach(button => {
            if(button.classList.contains("btn-secondary")) {
                button.classList.remove("btn-secondary");
                button.classList.add("btn-outline-secondary");
            }
        })
        btn.classList.add("btn-secondary");
        btn.classList.remove("btn-outline-secondary");
    })
})

// QUICK ADD
