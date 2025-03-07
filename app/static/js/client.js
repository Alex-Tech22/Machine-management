//========================================FONCTION DIVERS==========================================//

// Ouvrir/Fermer les machines d'une ligne
function toggleMachines(ligneId) {
    let machinesDiv = document.getElementById("machines-" + ligneId);
    let toggleIcon = document.querySelector(`[onclick="toggleMachines('${ligneId}')"] .toggle-icon`);

    machinesDiv.style.display = (machinesDiv.style.display === "none") ? "block" : "none";
    toggleIcon.innerHTML = (machinesDiv.style.display === "block") ? "▲" : "▼";
}

// Afficher le formulaire d'ajout de ligne de production
function toggleProductionLigneForm() {
    let formDiv = document.getElementById("production-ligne-form");
    formDiv.style.display = (formDiv.style.display === "none") ? "block" : "none";
}

//======================================CHARGEMENT DES DONNEE======================================//

// Charger un client et ses machines
function loadClient(clientId) {
    fetch(`/client/${clientId}`)
        .then(response => response.json())
        .then(data => {
            if (!data.error) {
                let clientDetails = document.getElementById("client-details");

                let machinesHtml = data.machines.length > 0 ? data.machines.map(machine => `
                    <div class="machine-card">
                        <img src="/static/images/machine_placeholder.png" alt="Machine">
                        <p>${machine.machine_name}</p>
                    </div>
                `).join("") : `<p>Aucune machine enregistrée pour ce client.</p>`;

                clientDetails.innerHTML = `
                    <h2>${data.customers_name}</h2>
                    <p>${data.address}</p>
                    <img src="/static/${data.logo}" alt="Logo Client" style="width: 150px;">
                    <div class="machine-container">
                        ${machinesHtml}
                        <button onclick="openMachineModal('${data.ID_customer}')">+</button>
                    </div>
                `;
            } else {
                document.getElementById("client-details").innerHTML = `<h2>Client non trouvé</h2>`;
            }
        })
        .catch(error => console.error("Erreur lors du chargement du client :", error));
}

// Charger les lignes de production d'un client
function loadProductionLignes(clientId) {
    console.log("Chargement des lignes de production pour le client ID:", clientId);

    fetch(`/client/${clientId}/production_lignes`)
        .then(response => {
            console.log("Réponse brute :", response);
            return response.text();  // Récupère le texte brut pour voir s'il y a une erreur
        })
        .then(text => {
            console.log("Texte brut de la réponse :", text);
            return JSON.parse(text);  // Convertit en JSON (si c'est bien du JSON)
        })
        .then(data => {
            console.log("Données JSON reçues :", data);
        })
        .catch(error => console.error("Erreur lors du chargement des lignes :", error));
}


// Charger les machines d'une ligne de production
function loadMachines(clientId, ligneId) {
    fetch(`/client/${clientId}/production_ligne/${ligneId}`)
        .then(response => response.json())
        .then(data => {
            let machineContainer = document.getElementById("machines-" + ligneId);
            machineContainer.innerHTML = data.map(machine => `
                <div class="machine-card">
                    <img src="/static/images/machine_placeholder.png" alt="Machine">
                    <p>${machine.name}</p>
                    <button class="delete-btn" onclick="deleteMachine('${machine.id}')">🗑</button>
                </div>
            `).join("");

            machineContainer.innerHTML += `<button class="add-machine-card" onclick="openMachineModal('${ligneId}')">+</button>`;
        })
        .catch(error => console.error("Erreur lors du chargement des machines :", error));
}

//======================================SUPPRESSION DE DONNEE======================================//

// Supprimer un client
function deleteClient(clientId) {
    fetch(`/client/client/delete/${clientId}`, {
        method: "DELETE",
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("✅ Client supprimé avec succès !");
            document.getElementById(`client-${clientId}`).remove();
        } else {
            alert("❌ Erreur : " + data.error);
        }
    })
    .catch(error => console.error("Erreur lors de la suppression du client :", error));
}

// Confirmation avant suppression d'un client
function confirmDelete(clientId) {
    if (confirm("⚠ Voulez-vous vraiment supprimer ce client et toutes ses données ?")) {
        deleteClient(clientId);
    }
}

// Supprimer une ligne de production
function deleteProductionLigne(ligneId) {
    if (confirm("Voulez-vous vraiment supprimer cette ligne de production et toutes ses machines ?")) {
        fetch(`/client/delete_production_ligne/${ligneId}`, { method: "POST" })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                } else {
                    alert("Erreur lors de la suppression !");
                }
            })
            .catch(error => console.error("Erreur lors de la suppression de la ligne :", error));
    }
}

// Supprimer une machine
function deleteMachine(machineId) {
    if (confirm("Voulez-vous vraiment supprimer cette machine ?")) {
        fetch(`/delete_machine/${machineId}`, { method: "POST" })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                } else {
                    alert("Erreur lors de la suppression !");
                }
            })
            .catch(error => console.error("Erreur lors de la suppression de la machine :", error));
    }
}

//========================================GESTION DE MODAL========================================//

// Ouvrir la modale
function openMachineModal(ligneId) {
    document.getElementById("machine-ligne-id").value = ligneId;
    document.getElementById("machineModal").style.display = "block";
}

// Fermer la modale
function closeMachineModal() {
    document.getElementById("machineModal").style.display = "none";
}