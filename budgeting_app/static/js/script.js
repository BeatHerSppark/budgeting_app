const burgerMenu = document.getElementById("toggle-btn");
const sidebarLogo = document.querySelector(".sidebar-logo")

window.onload = () => {
    document.getElementById("sidebar").classList.toggle("expand");
}

burgerMenu.addEventListener("click", () => {
    document.getElementById("sidebar").classList.toggle("expand");
})
sidebarLogo.addEventListener("click", () => {
    document.getElementById("sidebar").classList.toggle("expand");
})
