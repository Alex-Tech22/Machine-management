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


