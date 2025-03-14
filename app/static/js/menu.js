function toggleMenu() {
    let menu = document.getElementById("dropdown-menu");
    menu.style.display = (menu.style.display === "block") ? "none" : "block";
}

// Fermer le menu si on clique ailleurs
document.addEventListener("click", function(event) {
    let userMenu = document.querySelector(".user-menu"); // ✅ Correction ici

    if (userMenu && !userMenu.contains(event.target)) {
        let menu = document.getElementById("dropdown-menu");
        if (menu) {
            menu.style.display = "none";
        }
    }
});