let selectedItem = null;

function selectItem(element) {
    document.querySelectorAll(".selectable").forEach(el => el.classList.remove("selected"));
    element.classList.add("selected");
    selectedItem = {
        type: element.dataset.type,
        id: element.dataset.id,
        dom: element
    };
    console.log("✅ Sélection :", selectedItem);
}

function deleteSelected(e) {
    e.preventDefault();
    if (!selectedItem) {
        toastr.warning("Aucun élément sélectionné");
        return;
    }

    fetch(`/admin/delete/${selectedItem.type}/${selectedItem.id}`, {
        method: "POST"
    })
    .then(res => {
        if (res.ok) {
            toastr.success("Élément supprimé !");
            selectedItem.dom.remove();
            selectedItem = null;
        } else {
            toastr.error("Erreur lors de la suppression");
        }
    })
    .catch(err => {
        console.error("❌", err);
        toastr.error("Erreur serveur");
    });
}

function openValueModal(settingId, settingType) {
    const modal = document.getElementById("valueModal");
    const modalSettingId = document.getElementById("modalSettingId");
    const modalSettingType = document.getElementById("modalSettingType");

    const numericInput = document.getElementById("numericInput");
    const tableInput = document.getElementById("tableInput");

    modalSettingId.value = settingId;
    modalSettingType.value = settingType;

    // Affiche ou cache les champs selon le type
    if (settingType === "Num") {
        numericInput.style.display = "block";
        tableInput.style.display = "none";
    } else if (settingType === "Tab") {
        numericInput.style.display = "none";
        tableInput.style.display = "block";
    }

    modal.style.display = "block";
}

function closeModal() {
    const modal = document.getElementById("valueModal");
    modal.style.display = "none";
}

window.onclick = function(event) {
    const modal = document.getElementById("valueModal");
    if (event.target == modal) {
        modal.style.display = "none";
    }
}
