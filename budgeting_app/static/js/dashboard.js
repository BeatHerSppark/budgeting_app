// DATE FETCHING
const todayBtn = document.getElementById("todayBtn");
const weekBtn = document.getElementById("weekBtn");
const monthBtn = document.getElementById("monthBtn");
const yearBtn = document.getElementById("yearBtn");

const formatDate_date = (date) => {
    let year = date.getFullYear();
    let month = (date.getMonth() + 1).toString();
    let day = date.getDate().toString();
    if (month.length < 2) {
        month = '0' + month;
    }
    if (day.length < 2) {
        day = '0' + day;
    }

    return `${year}-${month}-${day}`;
}

const getMonday = (d) => {
    d = new Date(d);
    let day = d.getDay(),
        diff = d.getDate() - day + (day === 0 ? -6 : 1);
    return new Date(d.setDate(diff));
}

const getFirstOfMonth = (d) => {
    d = new Date(d);
    return new Date(d.getFullYear(), d.getMonth(), 1);
}

const getFirstOfYear = (d) => {
    d = new Date(d);
    return new Date(d.getFullYear(), 0, 1);
}

todayBtn.addEventListener("click", () => {
    let today = formatDate_date(new Date());
    fetch("/app/set-date-range", {
        body: JSON.stringify({
            start: today,
            end: today,
            selected_date: "today",
        }),
        method: "POST",
    })
    .then(res => res.json())
    .then(data => location.reload())
    //todayBtn.href = `?start=${encodeURIComponent(today)}&end=${encodeURIComponent(today)}&selected_date=${encodeURIComponent("today")}`;
})

weekBtn.addEventListener("click", () => {
    let today = formatDate_date(new Date());
    let monday = formatDate_date( getMonday(new Date()) );
    fetch("/app/set-date-range", {
        body: JSON.stringify({
            start: monday,
            end: today,
            selected_date: "week",
        }),
        method: "POST",
    })
    .then(res => res.json())
    .then(data => location.reload())
    //weekBtn.href = `?start=${encodeURIComponent(monday)}&end=${encodeURIComponent(today)}&selected_date=${encodeURIComponent("week")}`;
})

monthBtn.addEventListener("click", () => {
    let today = formatDate_date(new Date());
    let firstOfMonth = formatDate_date( getFirstOfMonth(new Date()) );
    fetch("/app/set-date-range", {
        body: JSON.stringify({
            start: firstOfMonth,
            end: today,
            selected_date: "month",
        }),
        method: "POST",
    })
    .then(res => res.json())
    .then(data => location.reload())
    //monthBtn.href = `?start=${encodeURIComponent(firstOfMonth)}&end=${encodeURIComponent(today)}&selected_date=${encodeURIComponent("month")}`;
})

yearBtn.addEventListener("click", () => {
    let today = formatDate_date(new Date());
    let firstOfYear = formatDate_date( getFirstOfYear(new Date()) );
    fetch("/app/set-date-range", {
        body: JSON.stringify({
            start: firstOfYear,
            end: today,
            selected_date: "year",
        }),
        method: "POST",
    })
    .then(res => res.json())
    .then(data => location.reload())
    //yearBtn.href = `?start=${encodeURIComponent(firstOfYear)}&end=${encodeURIComponent(today)}&selected_date=${encodeURIComponent("year")}`;
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

// EDITING TRANSACTIONS
const editModal = document.getElementById("editModalToggle");
let openedOnce = false;
if(editModal) {
    editModal.addEventListener("show.bs.modal", e => {
        if(!openedOnce) document.getElementById("modal-body").innerHTML += `<input type="hidden" name="path" id="path" value="dashboard">`;

        const button = e.relatedTarget;
        const id = button.getAttribute("data-bs-id");
        const type = button.getAttribute("data-bs-type");
        const amount = button.getAttribute("data-bs-amount");
        const category = button.getAttribute("data-bs-category");
        const date = button.getAttribute("data-bs-date");
        const comment = button.getAttribute("data-bs-comment");

        const idInput = editModal.querySelector("#id");
        const typeInput = editModal.querySelector("#transaction_type");
        const amountInput = editModal.querySelector("#amount");
        const categoryInput = editModal.querySelector("#category");
        const dateInput = editModal.querySelector("#date");
        const commentInput = editModal.querySelector("#comment");

        fetch("/app/dashboard-get-categories", {
            body: JSON.stringify({ category_type: type }),
            method: "POST",
        })
        .then(res => res.json())
        .then(data => {
            data.categories.forEach(category => {
                categoryInput.innerHTML += `<option value="${category.title}">${category.title}</option>`
            })
            if(category=="Uncategorized") {
                categoryInput.value = "Choose a category";
            }
            else {
                categoryInput.value = category;
            }
        })

        idInput.value = id;
        typeInput.value = type;
        amountInput.value = amount;
        dateInput.value = date;
        commentInput.value = comment;
        openedOnce = true;
    })

    editModal.addEventListener("hide.bs.modal", e => {
        const categoryInput = editModal.querySelector("#category");
        categoryInput.innerHTML = `<option selected>Choose a category</option>`
    })
}

// EXPENSE VS INCOME CHART
async function fetchChartData() {
    const response = await fetch("/app/dashboard-get-chart", {
                    method: "POST",
                });

    const data = await response.json();

    let incomeData = data.income;
    let expensesData = data.expenses;
    let categories = data.categories;

    updateChart(incomeData, expensesData, categories);
}

const updateChart = (income, expenses, categories) => {
    var options = {
        chart: {
            type: 'area',
            height: '100%',
        },
        stroke: {
            curve: 'smooth'
        },
        series: [
            {
                name: 'Income',
                data: income
            },
            {
                name: 'Expenses',
                data: expenses
            }
        ],
        xaxis: {
            categories: categories
        },
        fill: {
            type: 'gradient',
            gradient: {
                shadeIntensity: 1,
                opacityFrom: 0.7,
                opacityTo: 0.9,
                stops: [0, 90, 100]
            }
        },
        dataLabels: {
            enabled: false
        },
        tooltip: {
            shared: true,
            intersect: false
        },
        colors: ['#00E396', '#E91E63']
    };

    var chart = new ApexCharts(document.querySelector("#expenseIncomeChart"), options);

    chart.render();
}

fetchChartData();
