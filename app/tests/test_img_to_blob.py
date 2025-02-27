def image_to_blob(image_path):
    """Convertit une image en BLOB."""
    with open(image_path, "rb") as file:
        return file.read()

def save_blob(blob_data, output_path):
    """Enregistre un BLOB dans un fichier binaire."""
    with open(output_path, "wb") as file:
        file.write(blob_data)

# Exemple d'utilisation
image_path = "app/static/images/Logo-Boscher.jpg"  # Chemin de l'image d'entrée
output_blob_path = "app/static/images_blob/blob_data.bin"      # Fichier où stocker le BLOB

# Convertir l'image en BLOB
blob_result = image_to_blob(image_path)

# Stocker le BLOB dans un fichier binaire
save_blob(blob_result, output_blob_path)

# Vérification
print(f"✅ Image convertie et stockée en BLOB ({len(blob_result)} octets)")
print(f"🔹 Fichier BLOB enregistré sous : {output_blob_path}")
