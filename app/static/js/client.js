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
