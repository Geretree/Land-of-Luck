import tkinter as tk
from tkinter import messagebox
import sys
import os
import requests
import urllib3
import re  # Für Regex
import json  # Für JSON-Dateioperationen

# Füge den Projektroot-Pfad hinzu, um Casino.Lobby.Scripts zu importieren
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
sys.path.append(project_root)

# Pfad zur JSON-Datei
JSON_FILE_PATH = os.path.join(project_root, "Casino", "Bank", "Data", "coin.json")

# Unterdrückt SSL-Warnungen (nur für lokale Tests, nicht für Produktion!)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "http://backend.casino.itservsec.dev/api/users"
HEADERS = {"X-API-KEY": "Key"}  # Ersetze mit deinem API-Schlüssel


def print_response(response):
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {response.json()}")
    except ValueError:
        print(f"Response: {response.text}")


def validate_password(password):
    """Prüft, ob das Passwort den Anforderungen entspricht."""
    pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    if re.match(pattern, password):
        return True
    return False


def validate_username(username):
    """Prüft, ob der Benutzername nur Buchstaben und Zahlen enthält."""
    pattern = r"^[a-zA-Z0-9]+$"
    if re.match(pattern, username):
        return True
    return False


def write_user_to_json(user_data):
    """Schreibt die Benutzerdaten in die JSON-Datei im gewünschten Format."""
    try:
        # Erstelle das Verzeichnis, falls es nicht existiert
        os.makedirs(os.path.dirname(JSON_FILE_PATH), exist_ok=True)

        # Transformiere die Benutzerdaten in das gewünschte Format
        transformed_data = {
            "ID_USER": user_data.get("id", 1),  # Falls 'id' nicht existiert, Default 1
            "USERNAME": user_data.get("username", ""),
            "Password": user_data.get("password", ""),
            "Coin": user_data.get("SCORE", 50),  # Umbenannt von SCORE zu Coins, Default 50
            "chip5_chips": user_data.get("chip5_chips", 0),
            "chip10_chips": user_data.get("chip10_chips", 0),
            "chip50_chips": user_data.get("chip50_chips", 0),
            "chip100_chips": user_data.get("chip100_chips", 0),
            "chip500_chips": user_data.get("chip500_chips", 0),
            "chip1000_chips": user_data.get("chip1000_chips", 0),
            "chip5000_chips": user_data.get("chip5000_chips", 0)
        }

        # Schreibe die Benutzerdaten in die JSON-Datei
        with open(JSON_FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(transformed_data, f, indent=4)
        print(f"Benutzerdaten erfolgreich in {JSON_FILE_PATH} geschrieben.")
    except Exception as e:
        print(f"Fehler beim Schreiben in die JSON-Datei: {e}")
        messagebox.showerror("Fehler", f"Konnte Benutzerdaten nicht in JSON speichern: {str(e)}")


def show_login():
    """Zeigt die Eingabefelder für Login an."""
    clear_fields()
    window_title.set("Login")
    submit_button.config(text="Login", command=lambda: submit("login"))


def show_sign_in():
    """Zeigt die Eingabefelder für Sign In an."""
    clear_fields()
    window_title.set("Sign In")
    submit_button.config(text="Sign In", command=lambda: submit("signin"))


def clear_fields():
    """Löscht die Eingabefelder."""
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)


def user_action(username, password, action):
    """Verarbeitet Login oder Sign In über API-Aufrufe und schreibt Daten in JSON."""
    # Benutzernamen validieren (nur Buchstaben und Zahlen)
    if not validate_username(username):
        messagebox.showerror("Fehler", "Benutzername darf nur Buchstaben (a-z, A-Z) und Zahlen (0-9) enthalten.")
        return False, None

    # Passwortvalidierung nur bei Sign In
    if action == "signin" and not validate_password(password):
        messagebox.showerror("Fehler",
                             "Passwort muss mindestens 8 Zeichen lang sein und einen Großbuchstaben, Kleinbuchstaben, eine Zahl und ein Sonderzeichen enthalten.")
        return False, None

    try:
        if action == "login":
            response = requests.get(BASE_URL, headers=HEADERS, verify=False)
            if response.status_code != 200:
                try:
                    error_msg = response.json().get("message", "Fehler beim Abrufen der Benutzer.")
                except ValueError:
                    error_msg = response.text or "Unbekannter Fehler."
                messagebox.showerror("Login Fehler", error_msg)
                return False, None

            try:
                users = response.json()
                matching_user = next((user for user in users if user.get("username") == username), None)
                if matching_user is None:
                    messagebox.showerror("Login Fehler", "Benutzername nicht gefunden.")
                    return False, None
                if matching_user.get("password") == password:
                    messagebox.showinfo("Erfolg", "Login erfolgreich!")
                    # Schreibe die Benutzerdaten in die JSON-Datei
                    write_user_to_json(matching_user)
                    return True, matching_user
                else:
                    messagebox.showerror("Login Fehler", "Falsches Passwort.")
                    return False, None
            except ValueError:
                messagebox.showerror("Login Fehler", "Ungültige API-Antwort.")
                return False, None

        elif action == "signin":
            data = {
                "username": username,
                "password": password
            }
            response = requests.post(BASE_URL, json=data, headers=HEADERS, verify=False)
            if response.status_code in [200, 201]:
                messagebox.showinfo("Erfolg", "Registrierung erfolgreich!")
                # Hole die neuen Benutzerdaten (angenommen, die API gibt die neuen Daten zurück)
                new_user_data = response.json()
                # Schreibe die neuen Benutzerdaten in die JSON-Datei
                write_user_to_json(new_user_data)
                return True, new_user_data
            else:
                try:
                    error_msg = response.json().get("message", "Registrierung fehlgeschlagen.")
                except ValueError:
                    error_msg = response.text or "Unbekannter Fehler."
                messagebox.showerror("Sign In Fehler", error_msg)
                return False, None

    except requests.RequestException as e:
        messagebox.showerror("Netzwerkfehler", f"Verbindungsfehler: {str(e)}")
        return False, None


def submit(action):
    """Verarbeitet die Eingabe und startet Lobby.py."""
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        messagebox.showerror("Fehler", "Bitte Benutzername und Passwort eingeben.")
        return

    # Zeige Bestätigung (optional)
    messagebox.showinfo("Eingabe", f"{action.capitalize()} - Benutzername: {username}, Passwort: {'*' * len(password)}")

    success, user_data = user_action(username, password, action)

    if success:
        root.destroy()
        try:
            from Casino.Lobby.Scripts import Lobby
            Lobby.main()
        except Exception as e:
            print(f"Fehler beim Starten von Lobby: {e}")
            sys.exit()


# Erstelle das Hauptfenster
root = tk.Tk()
root.title("Benutzerdaten eingeben")
root.attributes('-fullscreen', True)  # Vollbildmodus
root.configure(bg="#2c3e50")  # Dunkler Hintergrund

# Variable für Fenstertitel
window_title = tk.StringVar()
window_title.set("Login")

# Titel-Label
tk.Label(root, textvariable=window_title, bg="#2c3e50", fg="white", font=("Arial", 14, "bold")).pack(pady=10)

# Buttons für Login/Sign In Auswahl
tk.Button(root, text="Login", command=show_login, bg="#3498db", fg="white", font=("Arial", 12)).pack(pady=5)
tk.Button(root, text="Sign In", command=show_sign_in, bg="#3498db", fg="white", font=("Arial", 12)).pack(pady=5)

# Labels und Eingabefelder
tk.Label(root, text="Benutzername:", bg="#2c3e50", fg="white", font=("Arial", 12)).pack(pady=10)
username_entry = tk.Entry(root, width=30, font=("Arial", 12))
username_entry.pack(pady=5)

tk.Label(root, text="Passwort:", bg="#2c3e50", fg="white", font=("Arial", 12)).pack(pady=10)
password_entry = tk.Entry(root, width=30, show="*", font=("Arial", 12))  # Passwort maskiert
password_entry.pack(pady=5)

# Submit-Button (wird dynamisch angepasst)
submit_button = tk.Button(root, text="Login", command=lambda: submit("login"), bg="#27ae60", fg="white",
                          font=("Arial", 12))
submit_button.pack(pady=20)

# Starte das Fenster
root.mainloop()