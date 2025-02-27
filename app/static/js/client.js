<<<<<<< HEAD
function loadClient(clientName) {
    const clientDetails = document.getElementById('client-details');

    // Simuler les données des clients
    const clientsData = {
        "Client 1": {
            address: "Adresse du client 1",
            machines: [
                { name: "Machine 1", image: "machine1.png" },
                { name: "Machine 2", image: "machine1.png" }
            ]
        },
        "Client 2": {
            address: "Adresse du client 2",
            machines: [
                { name: "Machine A", image: "machine1.png" }
            ]
        },
        "Client 3": {
            address: "Adresse du client 3",
            machines: []
        }
    };
=======
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
>>>>>>> 15d197504dd6b7197bf27b1106aaaea7339df254

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
<<<<<<< HEAD
=======

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

>>>>>>> 15d197504dd6b7197bf27b1106aaaea7339df254
