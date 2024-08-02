let icons = document.querySelectorAll("#iconsContainer .icon");

let iconTag = null;

icons.forEach(icon => {
    icon.addEventListener('click', () => {
        if(icon.classList.contains("bg-secondary")) {
            icons.forEach(icon2 => {
                if(icon2.classList.contains("bg-primary")){
                    icon2.classList.remove("bg-primary");
                    icon2.classList.add("bg-secondary");
                }
            })
            icon.classList.remove("bg-secondary");
            icon.classList.add("bg-primary");

            iconTag = icon.getAttribute("data-bs-icon");
        }
        else {
            icon.classList.remove("bg-primary");
            icon.classList.add("bg-secondary");

            iconTag = null;
        }
    })
})

const expenseBtn = document.getElementById("createExpenseCategory");
const incomeBtn = document.getElementById("createIncomeCategory");
const titleInput1 = document.getElementById("title1");
const titleInput2 = document.getElementById("title2");
const category_type1 = document.getElementById("category_type1");
const category_type2 = document.getElementById("category_type2");

expenseBtn.addEventListener('click', () => {
    if(titleInput1.value) {
        fetch("/app/create-category", {
            body: JSON.stringify({
                icon_tag: iconTag,
                title: titleInput1.value,
                category_type: category_type1.value,
            }),
            method: "POST",
        })
        .then(res => res.json())
        .then(data => location.reload())
    }
})

incomeBtn.addEventListener('click', () => {
    if(titleInput2.value) {
        fetch("/app/create-category", {
            body: JSON.stringify({
                icon_tag: iconTag,
                title: titleInput2.value,
                category_type: category_type2.value,
            }),
            method: "POST",
        })
        .then(res => res.json())
        .then(data => location.reload())
    }
})