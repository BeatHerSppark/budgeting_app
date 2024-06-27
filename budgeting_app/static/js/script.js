const burgerMenu = document.getElementById("toggle-btn");

burgerMenu.addEventListener("click", () => {
    document.getElementById("sidebar").classList.toggle("expand");
})