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

// EDIT BUDGET
const editBudgetBtn = document.getElementById("editBudgetBtn");
const budgetInput = document.getElementById("budget");

editBudgetBtn.addEventListener("click", ()=> {
    if(budgetInput.value) {
        fetch("/app/edit-budget", {
            body: JSON.stringify({
                budget: budgetInput.value,
            }),
            method: "POST",
        })
        .then(res => res.json())
        .then(data => location.reload())
    }
})