from argon2 import PasswordHasher
def hash_password():
    #Création du mot de passe hashé
    password = input("Entrez le mot de passe: ")
    ph = PasswordHasher()
    hashed_password = ph.hash(password)
    print(f"✅ Mot de passe haché : {hashed_password}")

    #Vérification du mot de passe1234
    test_password = input("Entrez le mot de passe à tester: ")
    try:
        if ph.verify(hashed_password, test_password):
            print("✅ Mot de passe correct !")
    except:
        print("❌ Mot de passe incorrect !")

if __name__ == "__main__":
    hash_password()
