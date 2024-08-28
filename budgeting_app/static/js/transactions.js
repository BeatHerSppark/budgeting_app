// DATE LOGIC
const todayBtn = document.getElementById("todayBtn");
const weekBtn = document.getElementById("weekBtn");
const monthBtn = document.getElementById("monthBtn");
const yearBtn = document.getElementById("yearBtn");
const allTimeBtn = document.getElementById("allTimeBtn");

const formatDate = (date) => {
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
    let today = formatDate(new Date());
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
    //todayBtn.href = `?start=${encodeURIComponent(today)}&end=${encodeURIComponent(today)}&date=${encodeURIComponent("today")}`;
})

weekBtn.addEventListener("click", () => {
    let today = formatDate(new Date());
    let monday = formatDate( getMonday(new Date()) );
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
    //weekBtn.href = `?start=${encodeURIComponent(monday)}&end=${encodeURIComponent(today)}&date=${encodeURIComponent("week")}`;
})

monthBtn.addEventListener("click", () => {
    let today = formatDate(new Date());
    let firstOfMonth = formatDate( getFirstOfMonth(new Date()) );
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
    //monthBtn.href = `?start=${encodeURIComponent(firstOfMonth)}&end=${encodeURIComponent(today)}&date=${encodeURIComponent("month")}`;
})

yearBtn.addEventListener("click", () => {
    let today = formatDate(new Date());
    let firstOfYear = formatDate( getFirstOfYear(new Date()) );
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
    //yearBtn.href = `?start=${encodeURIComponent(firstOfYear)}&end=${encodeURIComponent(today)}&date=${encodeURIComponent("year")}`;
})

allTimeBtn.addEventListener("click", () => {
    let earliestDate = formatDate(new Date(0));
    let today = formatDate(new Date());
    fetch("/app/set-date-range", {
        body: JSON.stringify({
            start: earliestDate,
            end: today,
            selected_date: "allTime",
        }),
        method: "POST",
    })
    .then(res => res.json())
    .then(data => location.reload())
    //allTimeBtn.href = `?start=${encodeURIComponent(earliestDate)}&end=${encodeURIComponent(today)}&date=${encodeURIComponent("allTime")}`;
})

// DELETE TRANSACTIONS
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

// CHART
var options = {
    chart: {
        height: 'auto',
        type: 'pie',
    },
    series: [44, 33, 23], // Three values
    labels: ['Apples', 'Oranges', 'Bananas'], // Labels for the values
    legend: {
        position: 'bottom'
    }
};

var chart = new ApexCharts(document.querySelector("#pieChart"), options);
chart.render();
