import requests

#URL Anpassen
BASE_URL = "http://casino.itservsec.dev:8080/api/users"

# User per Username abrufen
def get_user_by_username(username):
    params = {"username": username}
    response = requests.get(f"{BASE_URL}/search", params=params)
    if response.status_code == 404:
        print(f"User '{username}' nicht gefunden.")
        return None
    response.raise_for_status()
    return response.json()

# Neuen User mit Username und Passwort anlegen
def create_user(username, password):
    data = {
        "username": username,
        "password": password
    }
    response = requests.post(BASE_URL, json=data)
    response.raise_for_status()
    return response.json()

# Chips und Score per User-ID updaten
def update_user_chips_and_score(user_id, chips_score_updates):
    # chips_score_updates = dict mit beliebigen keys:
    # z.B. {"score": 100, "chip5_chips": 10, "chip50_chips": 2, ...}
    response = requests.put(f"{BASE_URL}/{user_id}/chips-score", json=chips_score_updates)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    # User suchen
    username_to_search = "max"
    user = get_user_by_username(username_to_search)
    if user:
        print("User gefunden:", user)

        user_id = user["idUser"]
        print(f"User-ID: {user_id}")

        # Beispiel: Chips und Score updaten
        updates = {
            "score": 75,
            "chip5_chips": 3,
            "chip50_chips": 1
        }
        updated_user = update_user_chips_and_score(user_id, updates)
        print("User aktualisiert:", updated_user)

    else:
        print(f"User '{username_to_search}' existiert nicht.")

    # Beispiel: Neuen User anlegen
    new_user = create_user("anna", "meinPasswort123")
    print("Neuer User erstellt:", new_user)
