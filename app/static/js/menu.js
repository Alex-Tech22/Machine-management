function toggleMenu() {
    let menu = document.getElementById("dropdown-menu");
    menu.style.display = (menu.style.display === "block") ? "none" : "block";
}

// Fermer le menu si on clique ailleurs
document.addEventListener("click", function(event) {
    let userMenu = document.querySelector(".user-menu");
    if (!userMenu.contains(event.target)) {
        document.getElementById("dropdown-menu").style.display = "none";
    }
});