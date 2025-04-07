function openTab(evt, tabName) {
    var i, tabcontent, tabbuttons;
    tabcontent = document.getElementsByClassName("tab-content");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tabbuttons = document.getElementsByClassName("tab-button");
    for (i = 0; i < tabbuttons.length; i++) {
        tabbuttons[i].className = tabbuttons[i].className.replace(" active", "");
    }
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

function openImageModal(src) {
    const modal = document.getElementById("imageModal");
    const modalImg = document.getElementById("modal-img");
    modal.style.display = "block";
    modalImg.src = src;
}

function closeImageModal() {
    document.getElementById("imageModal").style.display = "none";
}

function openRevisionModal() {
    document.getElementById("revisionModal").style.display = "flex";
}

function closeRevisionModal() {
    document.getElementById("revisionModal").style.display = "none";
}

function deleteSelectedHistory() {
    const form = document.getElementById('historyForm');
    const selected = form.querySelectorAll('input[name="selected"]:checked');

    if (selected.length === 0) {
        alert("Veuillez sélectionner au moins une révision à supprimer.");
        return;
    }

    if (!confirm("Voulez-vous vraiment supprimer les révisions sélectionnées ?")) {
        return;
    }

    const data = new FormData();
    selected.forEach(input => {
        data.append('selected_ids', input.value);
    });

    fetch(window.location.pathname + "/delete_history", {
        method: "POST",
        body: data
    }).then(res => {
        if (res.ok) {
            location.reload();
        } else {
            alert("Erreur serveur pendant la suppression.");
        }
    });
}