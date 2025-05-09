# Casino/Lobby/Scripts/main.py
import asyncio
from Lobby import game  # importiert die Coroutine


def main():
    # Starte die Coroutine sauber über asyncio
    asyncio.run(game())

if __name__ == "__main__":
    main()

