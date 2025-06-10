import json
import os
import requests
import urllib3
from tkinter import messagebox
import sys

# Füge den Projektroot-Pfad hinzu
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
sys.path.append(project_root)

# Pfad zur JSON-Datei
JSON_FILE_PATH = os.path.join(project_root, "Casino", "Bank", "Data", "coin.json")

# Unterdrückt SSL-Warnungen (nur für lokale Tests, nicht für Produktion!)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# API-Endpunkt und Header
BASE_URL = "http://backend.casino.itservsec.dev/api/users"
HEADERS = {"X-API-KEY": "Key"}  # Ersetze mit deinem API-Schlüssel

def print_response(response):
    """Gibt den Status und die Antwort der API aus."""
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {response.json()}")
    except ValueError:
        print(f"Response: {response.text}")

def update_users_in_db():
    """Liest Benutzerdaten aus Coin.json und aktualisiert sie in der Datenbank."""
    try:
        # Lese die JSON-Datei
        if not os.path.exists(JSON_FILE_PATH):
            messagebox.showerror("Fehler", f"JSON-Datei nicht gefunden: {JSON_FILE_PATH}")
            return

        with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
            users = json.load(f)

        # Falls nur ein einzelner Benutzer in der Datei ist, in eine Liste umwandeln
        if isinstance(users, dict):
            users = [users]

        # Iteriere über alle Benutzer
        for user in users:
            user_id = user.get("ID_USER")
            if not user_id:
                print(f"Fehler: ID_USER fehlt für Benutzer {user.get('USERNAME', 'unbekannt')}")
                messagebox.showerror("Fehler", f"ID_USER fehlt für Benutzer {user.get('USERNAME', 'unbekannt')}")
                continue

            # Erstelle das Update-Payload und mappe Coins zu SCORE
            update_data = {
                "score": user.get("coin", 50),  # Coins aus JSON wird zu SCORE
                "chip5_chips": user.get("chip5_chips", 0),
                "chip10_chips": user.get("chip10_chips", 0),
                "chip50_chips": user.get("chip50_chips", 0),
                "chip100_chips": user.get("chip100_chips", 0),
                "chip500_chips": user.get("chip500_chips", 0),
                "chip1000_chips": user.get("chip1000_chips", 0),
                "chip5000_chips": user.get("chip5000_chips", 0)  # API erwartet chip5000
            }

            # Sende PUT-Anfrage an die API
            try:
                response = requests.put(
                    f"{BASE_URL}/{user_id}/chips-score",
                    json=update_data,
                    headers=HEADERS,
                    verify=False
                )
                if response.status_code == 200:
                    print(f"Benutzer {user.get('USERNAME', 'unbekannt')} (ID: {user_id}) erfolgreich aktualisiert.")
                else:
                    try:
                        error_msg = response.json().get("message", "Fe-metal beim Aktualisieren des Benutzers.")
                    except ValueError:
                        error_msg = response.text or "Unbekannter Fehler."
                    print(f"Fehler beim Aktualisieren von Benutzer {user.get('USERNAME', 'unbekannt')} (ID: {user_id}): {error_msg}")
                    messagebox.showerror(
                        "Fehler",
                        f"Fehler beim Aktualisieren von Benutzer {user.get('USERNAME', 'unbekannt')} (ID: {user_id}): {error_msg}"
                    )
            except requests.RequestException as e:
                print(f"Netzwerkfehler beim Aktualisieren von Benutzer {user.get('USERNAME', 'unbekannt')} (ID: {user_id}): {str(e)}")
                messagebox.showerror(
                    "Netzwerkfehler",
                    f"Verbindungsfehler für Benutzer {user.get('USERNAME', 'unbekannt')} (ID: {user_id}): {str(e)}"
                )

        messagebox.showinfo("Erfolg", "Alle Benutzer wurden verarbeitet.")
    except json.JSONDecodeError:
        print(f"Fehler: Ungültiges JSON-Format in {JSON_FILE_PATH}")
        messagebox.showerror("Fehler", f"Ungültiges JSON-Format in {JSON_FILE_PATH}")
    except Exception as e:
        print(f"Fehler beim Lesen der JSON-Datei oder Verarbeitung: {str(e)}")
        messagebox.showerror("Fehler", f"Fehler beim Verarbeiten der Benutzerdaten: {str(e)}")

def main():
    """Hauptfunktion zum Ausführen des Skripts."""
    update_users_in_db()

if __name__ == "__main__":
    main()