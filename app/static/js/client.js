function loadClient(clientId) {
    fetch(`/client/${clientId}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById("client-details").innerHTML = `<h2>Client non trouvé</h2>`;
            } else {
                document.getElementById("client-details").innerHTML = `
                    <h2>${data.customers_name}</h2>
                    <p>${data.address}</p>
                    <img src="/static/images/${data.logo}" alt="Logo Client" style="width: 150px;">
                `;
            }
        })
        .catch(error => console.error("Erreur:", error));

    // Vérifier si le client existe
    if (clientsData[clientName]) {
        const client = clientsData[clientName];

        // Construire l'affichage des machines
        let machinesHtml = '';
        client.machines.forEach(machine => {
            machinesHtml += `
                <div class="machine-card">
                    <img src="/static/images/${machine.image}" alt="${machine.name}">
                    <p>${machine.name}</p>
                </div>
            `;
        });

        // Ajouter une carte pour ajouter une machine
        machinesHtml += `
            <div class="add-machine-card" onclick="addMachine('${clientName}')">
                +
            </div>
        `;

        // Mettre à jour la section client
        clientDetails.innerHTML = `
            <h2>${clientName}</h2>
            <p>${client.address}</p>
            <div class="machine-list">${machinesHtml}</div>
        `;
    } else {
        clientDetails.innerHTML = `<h2>Aucun client trouvé</h2>`;
    }
}

function addMachine(clientName) {
    alert(`Ajout d'une nouvelle machine pour ${clientName}`);
}

function confirmDelete(clientId) {
    if (confirm("⚠ Voulez-vous vraiment supprimer ce client et toutes ses données ?")) {
        deleteClient(clientId);
    }
}

function deleteClient(clientId) {
    fetch(`/client/client/delete/${clientId}`, {
        method: "DELETE",
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("✅ Client supprimé avec succès !");
            document.getElementById(`client-${clientId}`).remove(); // Supprime l'élément de la liste
        } else {
            alert("❌ Erreur : " + data.error);
        }
    })
    .catch(error => console.error("Erreur lors de la suppression :", error));
}

