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

        console.log(iconTag);
    })
})