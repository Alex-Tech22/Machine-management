//========================================FONCTIONS D'AFFICHAGE==========================================//

// Ouvrir/Fermer les machines d'une ligne
function toggleMachines(ligneId) {
    let machinesDiv = document.getElementById("machines-" + ligneId);
    let toggleIcon = document.querySelector(`[onclick="toggleMachines('${ligneId}')"] .toggle-icon`);

    if (!machinesDiv) {
        console.error(`❌ Erreur : L'élément machines-${ligneId} est introuvable.`);
        return;
    }

    document.querySelectorAll('.machines-container').forEach(container => {
        if (container.id !== "machines-" + ligneId) {
            container.style.display = "none";
        }
    });

    let isVisible = machinesDiv.style.display === "block";
    machinesDiv.style.display = isVisible ? "none" : "block";
    toggleIcon.innerHTML = isVisible ? "▼" : "▲";

    if (!isVisible) {
        loadMachines(ligneId);
    }
}

// Afficher/Masquer le formulaire d'ajout de ligne de production
function toggleProductionLigneForm() {
    let formDiv = document.getElementById("production-ligne-form");
    
    if (!formDiv) {
        console.error("❌ Erreur : Impossible de trouver l'élément #production-ligne-form.");
        return;
    }
    
    formDiv.style.display = (formDiv.style.display === "none" || formDiv.style.display === "") ? "block" : "none";
    
    console.log("✅ Formulaire de production ligne visible :", formDiv.style.display);
}


//======================================CHARGEMENT DES DONNÉES======================================//

let selectedClientId = null;
// Charger un client et ses lignes de production
function loadClient(clientId) {
    selectedClientId = clientId;
    if (!clientId) return;

    document.getElementById("client-details").style.display = "none"; // Masquer temporairement

    fetch(`/client/${clientId}`)
    .then(response => response.json())
    .then(data => {
        if (!data.error) {
            document.getElementById("client-name").textContent = data.customers_name;
            document.getElementById("client-address").textContent = "Adresse: " + data.address;
            document.getElementById("client-details").style.display = "block";

            // Charger les lignes de production après récupération du client
            loadProductionLignes(clientId);
        } else {
            console.error("Client non trouvé !");
        }
    })
    .catch(error => console.error("Erreur lors du chargement du client :", error));
}


// Charger les lignes de production du client sélectionné
function loadProductionLignes(clientId) {
    fetch(`/client/${clientId}/production_lignes`)
    .then(response => response.json())
    .then(data => {
        let productionContainer = document.getElementById("production-ligne-container");
        productionContainer.innerHTML = ""; // Nettoyer l'affichage

        if (data.error) {
            alert("Erreur : " + data.error);
            return;
        }

        data.forEach(line => {
            let div = document.createElement("div");
            div.className = "production-ligne-card";
            div.innerHTML = `
                <p onclick="toggleMachines('${line.id}')">${line.name} <span class="toggle-icon">▼</span></p>
                <button class="delete-btn" onclick="deleteProductionLigne('${line.id}')">🗑</button>
                <div id="machines-${line.id}" class="machines-container" style="display: none;"></div>
            `;
            productionContainer.appendChild(div);
        });

        document.getElementById("client-details").style.display = "block";
    })
    .catch(error => console.error("Erreur lors du chargement des lignes de production :", error));
}

// Charger les machines d'une ligne de production
function loadMachines(ligneId) {
    let machineContainer = document.getElementById(`machines-${ligneId}`);
    if (!machineContainer) {
        console.error(`❌ Erreur : Impossible de trouver machines-${ligneId}`);
        return;
    }

    machineContainer.innerHTML = `<div class="skeleton" style="height: 50px; width: 100%"></div>`;

    fetch(`/client/${selectedClientId}/production_ligne/${ligneId}`)
    .then(response => response.json())
    .then(data => {
        machineContainer.innerHTML = "";  // Nettoyer l'affichage

        if (!Array.isArray(data) || data.length === 0) {
            machineContainer.innerHTML = `<p>Aucune machine enregistrée.</p>`;
        } else {
            data.forEach(machine => {
                let machineDiv = document.createElement("div");
                machineDiv.className = "machine-card";
                machineDiv.id = `machine-${machine.id}`;
                machineDiv.innerHTML = `
                    <a href="/machine/${machine.id}" class="machine-link">
                        <img src="/static/images/general/toridas.png" alt="Machine">
                        <p>${machine.name}</p>
                    </a>
                    <button class="delete-btn" onclick="deleteMachine('${machine.id}')">🗑</button>
                `;
                machineContainer.appendChild(machineDiv);
            });
        }
        let addButton = document.createElement("button");
        addButton.className = "add-machine-card";
        addButton.textContent = "+";
        addButton.onclick = () => openMachineModal(ligneId);
        machineContainer.appendChild(addButton);
    })
    .catch(error => console.error("Erreur lors du chargement des machines :", error));
}

//======================================SUPPRESSION DE DONNÉES======================================//

// Supprimer un client
function deleteClient(clientId) {
    fetch(`/client/delete/${clientId}`, { method: "DELETE" })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("✅ Client supprimé avec succès !");
            location.reload();
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
    if (!confirm("⚠ Voulez-vous vraiment supprimer cette machine ? Cette action est irréversible.")) {
        return;
    }

    fetch(`/client/delete_machine/${machineId}`, { method: "POST" })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showToast("✅ Machine supprimée avec succès !");
            
            let machineElement = document.getElementById(`machine-${machineId}`);
            if (machineElement) {
                machineElement.remove();
            } else {
                console.error(`❌ Erreur : L'élément machine-${machineId} est introuvable.`);
            }

            // Rafraîchissement automatique de la liste des machines
            if (data.ligne_id) {
                setTimeout(() => {
                    refreshMachines(data.ligne_id);

                    // Vérifier si la liste des machines est vide après suppression
                    let machineContainer = document.getElementById(`machines-${data.ligne_id}`);
                    if (!machineContainer || machineContainer.children.length === 0) {
                        console.warn("⚠ Aucune machine restante, rechargement de la page...");
                        location.reload();
                    }
                }, 500);
            } else {
                console.error("❌ Erreur : Aucun ID de ligne retourné par l'API.");
                location.reload();
            }
        } else {
            showToast("❌ Erreur : " + data.error, "error");
        }
    })
    .catch(error => {
        console.error("❌ Erreur lors de la suppression :", error);
        location.reload(); // Recharge la page en cas d'erreur critique
    });
}


//========================================GESTION DE MODAL========================================//

// Ouvrir la modale d'ajout de machine
function openMachineModal(ligneId) {
    document.getElementById("machine-ligne-id").value = ligneId;
    document.getElementById("machineModal").style.display = "block";
}

// Fermer la modale
function closeMachineModal() {
    document.getElementById("machineModal").style.display = "none";
}

//========================================GESTION DE MESSAGE========================================//

function showToast(message, type="success") {
    toastr.options = { "positionClass": "toast-bottom-right" };
    toastr[type](message);
}

function refreshMachines(ligneId) {
    let machineContainer = document.getElementById(`machines-${ligneId}`);
    if (machineContainer) {
        machineContainer.innerHTML = "<p>Chargement...</p>"; // Indiquer qu'un chargement est en cours
        loadMachines(ligneId);
    }
}
