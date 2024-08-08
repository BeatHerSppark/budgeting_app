// DATE LOGIC
const todayBtn = document.getElementById("todayBtn");
const weekBtn = document.getElementById("weekBtn");
const monthBtn = document.getElementById("monthBtn");
const yearBtn = document.getElementById("yearBtn");

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
    todayBtn.href = `?start=${encodeURIComponent(today)}&end=${encodeURIComponent(today)}&date=${encodeURIComponent("today")}`;
})

weekBtn.addEventListener("click", () => {
    let today = formatDate(new Date());
    let monday = formatDate( getMonday(new Date()) );
    weekBtn.href = `?start=${encodeURIComponent(monday)}&end=${encodeURIComponent(today)}&date=${encodeURIComponent("week")}`;
})

monthBtn.addEventListener("click", () => {
    let today = formatDate(new Date());
    let firstOfMonth = formatDate( getFirstOfMonth(new Date()) );
    monthBtn.href = `?start=${encodeURIComponent(firstOfMonth)}&end=${encodeURIComponent(today)}&date=${encodeURIComponent("month")}`;
})

yearBtn.addEventListener("click", () => {
    let today = formatDate(new Date());
    let firstOfYear = formatDate( getFirstOfYear(new Date()) );
    yearBtn.href = `?start=${encodeURIComponent(firstOfYear)}&end=${encodeURIComponent(today)}&date=${encodeURIComponent("year")}`;
})
