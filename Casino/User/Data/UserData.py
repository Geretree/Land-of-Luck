import tkinter as tk
from tkinter import messagebox
import sys
import os
import requests
import urllib3

# Füge den Projektroot-Pfad hinzu, um Casino.Lobby.Scripts zu importieren
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
sys.path.append(project_root)

#from Casino.Lobby.Scripts import Lobby



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
    """Verarbeitet Login oder Sign In über API-Aufrufe."""
    try:
        if action == "login":
            # Hole alle Benutzer mit der GET-Anfrage (wie in list_users())
            response = requests.get(BASE_URL, headers=HEADERS, verify=False)

            # Prüfe die Antwort
            if response.status_code != 200:
                try:
                    error_msg = response.json().get("message", "Fehler beim Abrufen der Benutzer.")
                except ValueError:
                    error_msg = response.text or "Unbekannter Fehler."
                messagebox.showerror("Login Fehler", error_msg)
                return False

            # Filtere die Benutzerliste nach Benutzername
            try:
                users = response.json()  # Angenommen, es ist eine Liste von Benutzern
                matching_user = next((user for user in users if user.get("username") == username), None)

                if matching_user is None:
                    messagebox.showerror("Login Fehler", "Benutzername nicht gefunden.")
                    return False

                # Vergleiche das Passwort (angenommen, es ist im Klartext)
                if matching_user.get("password") == password:
                    messagebox.showinfo("Erfolg", "Login erfolgreich!")
                    return True  # Erfolg, um Lobby.main() zu starten
                else:
                    messagebox.showerror("Login Fehler", "Falsches Passwort.")
                    return False
            except ValueError:
                messagebox.showerror("Login Fehler", "Ungültige API-Antwort.")
                return False

        elif action == "signin":
            # API-Anfrage zum Speichern des neuen Benutzers
            data = {
                "username": username,
                "password": password
            }
            response = requests.post(BASE_URL, json=data, headers=HEADERS, verify=False)

            # Prüfe die Antwort
            if response.status_code in [200, 201]:  # 201 Created ist üblich für POST
                messagebox.showinfo("Erfolg", "Registrierung erfolgreich!")
                return True  # Erfolg, um Lobby.main() zu starten
            else:
                try:
                    error_msg = response.json().get("message", "Registrierung fehlgeschlagen.")
                except ValueError:
                    error_msg = response.text or "Unbekannter Fehler."
                messagebox.showerror("Sign In Fehler", error_msg)
                return False

    except requests.RequestException as e:
        messagebox.showerror("Netzwerkfehler", f"Verbindungsfehler: {str(e)}")
        return False


def submit(action):
    """Verarbeitet die Eingabe und startet Lobby.py."""
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        messagebox.showerror("Fehler", "Bitte Benutzername und Passwort eingeben.")
        return

    # Zeige Bestätigung (optional)
    messagebox.showinfo("Eingabe", f"{action.capitalize()} - Benutzername: {username}, Passwort: {'*' * len(password)}")

    success = user_action(username, password, action)

    if success:
        # Schließe das tkinter-Fenster
        root.destroy()

        # Starte das Lobby-Skript
        try:
            from Casino.Lobby.Scripts import Lobby  # <-- Import NUR HIER!
            Lobby.main()
        except Exception as e:
            print(f"Fehler beim Starten von Lobby: {e}")
            sys.exit()


# Erstelle das Hauptfenster
root = tk.Tk()
root.title("Benutzerdaten eingeben")
root.geometry("400x300")  # Fenstergröße
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