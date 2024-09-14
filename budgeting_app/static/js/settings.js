let pfps = document.querySelectorAll("#pfpChoices .rounded-circle");
const savePfp = document.getElementById("savePfp");

let pfpUrl = null;

pfps.forEach(pfp => {
    if(pfp.getAttribute("data-bs-url") == userPfp) {
        pfpUrl = userPfp;
        pfp.classList.add("border-primary", "border", "border-3");
    }
    pfp.addEventListener('click', () => {
        if(!pfp.classList.contains("border-primary")) {
            pfps.forEach(pfp2 => {
                if(pfp2.classList.contains("border-primary")){
                    pfp2.classList.remove("border-primary", "border", "border-3");
                }
            })
            pfp.classList.add("border-primary", "border", "border-3");
            pfpUrl = pfp.getAttribute("data-bs-url");
            if(savePfp.disabled) savePfp.disabled = false;
        }
    })
})

savePfp.addEventListener("click", () => {
    fetch("/app/change-pfp", {
        body: JSON.stringify({
            pfpUrl: pfpUrl,
        }),
        method: "POST",
    })
    .then(res => res.json())
    .then(data => location.reload())
})