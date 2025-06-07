# Kid-Me Projekt

Dies ist eine Anleitung, um das `fncoding/kid-me` Projekt lokal einzurichten und auszuführen.

## Über das Projekt

`kid-me` ist ein kleines Portfolio-Projekt, das als webbasierte Anwendung konzipiert ist. Nach dem Login gelangt man zu einem persönlichen Dashboard, das verschiedene Organisationshilfen für den Alltag bietet:

*   **Einkaufsliste:** Verwalte deinen Lebensmittelbestand zu Hause und organisiere deine Einkäufe.
*   **Ausgaben-Tracker (Expense):** Behalte den Überblick über deine Ausgaben.

Zukünftig sind folgende Funktionen geplant:
*   **Tagesnachrichten:** Hinterlasse kleine Nachrichten für deine Mitbewohner.
*   **Chat-Funktion:** Eine integrierte Chat-Möglichkeit.

## Voraussetzungen

Stelle sicher, dass die folgenden Werkzeuge auf deinem System installiert sind:

*   Git
*   Python 3.x (stelle sicher, dass Python und Pip zu deinem Systempfad hinzugefügt sind)

## Klonen des Repositories

1.  Öffne dein Terminal oder deine Kommandozeile.
2.  Klone das Repository mit dem folgenden Befehl:
    ```bash
    git clone https://github.com/fncoding/kid-me.git
    ```
3.  Wechsle in das neu erstellte Verzeichnis:
    ```bash
    cd kid-me
    ```

## Einrichtung und Starten des Projekts

1.  **Virtuelle Umgebung erstellen:**
    Eine virtuelle Umgebung hilft dabei, Projektabhängigkeiten isoliert zu halten. Erstelle eine im Hauptverzeichnis des Projekts (z.B. `kid-me`):
    ```bash
    # Für Windows (verwendet den Python Launcher)
    py -m venv ven

    # Für macOS/Linux
    python3 -m venv ven
    ```
    *(Hinweis: `ven` ist der Name der virtuellen Umgebung, wie in den ursprünglichen Anweisungen. Du kannst auch einen anderen Namen wie `venv` wählen und die folgenden Befehle entsprechend anpassen.)*

2.  **Virtuelle Umgebung aktivieren:**
    *   **Windows (PowerShell):**
        ```powershell
        .\ven\Scripts\Activate.ps1
        ```
        (Wenn die Ausführung von Skripten blockiert ist, musst du möglicherweise zuerst `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process` ausführen.)
    *   **Windows (CMD):**
        ```batch
        .\ven\Scripts\activate.bat
        ```
    *   **macOS/Linux (Bash/Zsh):**
        ```bash
        source ven/bin/activate
        ```
    Nach der Aktivierung sollte der Name der virtuellen Umgebung (z.B. `(ven)`) in deiner Terminal-Eingabeaufforderung erscheinen.

3.  **(Empfohlen) Abhängigkeiten installieren:**
    Wenn das Projekt eine `requirements.txt`-Datei enthält (was für Django-Projekte üblich ist), installiere die notwendigen Pakete:
    ```bash
    pip install -r requirements.txt
    ```
    *(Falls diese Datei nicht existiert oder Abhängigkeiten bereits anders verwaltet werden, kann dieser Schritt angepasst oder übersprungen werden.)*

4.  **Wechsle in das `src`-Verzeichnis:**
    Die Django-Projektdateien befinden sich im `src`-Ordner.
    ```bash
    cd src
    ```

5.  **Datenbankmigrationen anwenden:**
    Django verwendet Migrationen, um das Datenbankschema zu verwalten. Dieser Schritt ist oft notwendig, bevor der Server gestartet werden kann.
    ```bash
    # Für Windows (innerhalb der aktivierten Umgebung und im src-Verzeichnis)
    py manage.py migrate

    # Für macOS/Linux (innerhalb der aktivierten Umgebung und im src-Verzeichnis)
    python manage.py migrate
    ```

6.  **Entwicklungsserver starten:**
    Starte den Django-Entwicklungsserver:
    ```bash
    # Für Windows (innerhalb der aktivierten Umgebung und im src-Verzeichnis)
    py manage.py runserver

    # Für macOS/Linux (innerhalb der aktivierten Umgebung und im src-Verzeichnis)
    python manage.py runserver
    ```
    Standardmäßig läuft der Server unter `http://127.0.0.1:8000/`. Öffne diese Adresse in deinem Webbrowser, um die Anwendung zu sehen.

7.  **Beenden des Servers:**
    Drücke `CTRL+C` im Terminal, um den Server zu stoppen.

8.  **Deaktivieren der virtuellen Umgebung:**
    Wenn du mit der Arbeit fertig bist, kannst du die virtuelle Umgebung deaktivieren:
    ```bash
    deactivate
    ```

## Weitere Hinweise

*   Stelle sicher, dass du dich im richtigen Verzeichnis befindest, wenn du die Befehle ausführst. Die Pfade zur Aktivierung der virtuellen Umgebung und zum `manage.py`-Skript sind relativ zum Hauptverzeichnis des Projekts bzw. zum `src`-Verzeichnis.
*   Wenn du auf Probleme stößt, überprüfe die Fehlermeldungen im Terminal. Sie geben oft Hinweise auf die Ursache.
