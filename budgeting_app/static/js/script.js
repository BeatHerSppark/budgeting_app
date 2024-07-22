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

// DELETING TRANSACTIONS
const transaction_checkboxes = document.querySelectorAll("td input");

transaction_checkboxes.forEach(checkbox => {
    checkbox.addEventListener("change", () => {
        if(checkbox.checked) {
            document.getElementById("dashboard_delete_transactions").classList.remove("d-none");
            document.getElementById("dashboard_delete_transactions").classList.add("d-block");
        }
        let noneSelected=true;
        transaction_checkboxes.forEach(checkbox2 => {
            if(checkbox2.checked) {
                noneSelected=false;
            }
        })
        if(noneSelected) {
            document.getElementById("dashboard_delete_transactions").classList.remove("d-block");
            document.getElementById("dashboard_delete_transactions").classList.add("d-none");
        }
    })
})

const dashboard_delete_transactions = document.getElementById("dashboard_delete_transactions");

dashboard_delete_transactions.addEventListener("click", () => {
    let idArray = [];
    transaction_checkboxes.forEach(checkbox => {
        if(checkbox.checked) idArray.push(checkbox.id);
    })

    fetch("/app/dashboard-delete-transactions", {
        body: JSON.stringify({ checkedIDs: idArray }),
        method: "POST",
    })
    .then(res => res.json())
    .then(data => {
        location.reload();
    })
})