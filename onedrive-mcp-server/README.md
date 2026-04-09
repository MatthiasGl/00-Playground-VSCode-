# OneDrive MCP Server

Ein Model Context Protocol (MCP) Server für die Integration mit OneDrive, der Dateien auflisten, hochladen und herunterladen kann.

## Sicherheit und Zugriffskontrolle

Der Server erlaubt nur Zugriff auf spezifische Pfade, die in der Datei `allowed_paths.txt` definiert sind. Alle untergeordneten Pfade dieser erlaubten Pfade haben Lese- und Schreibzugriff.

### Erlaubte Pfade konfigurieren
Bearbeite die Datei `allowed_paths.txt` im Projektverzeichnis:

```
/Dokumente
/Bilder
/Downloads
```

- Jede Zeile ist ein erlaubter Pfad.
- Pfade müssen mit `/` beginnen.
- Kommentare beginnen mit `#`.
- Alle Unterordner dieser Pfade sind automatisch erlaubt.

## Setup

1. **Azure App Registration erstellen**
   - Gehe zu [Azure Portal](https://portal.azure.com)
   - Erstelle eine neue App-Registrierung
   - Konfiguriere Redirect URI: `http://localhost:8000/auth/callback`
   - Füge Microsoft Graph API Berechtigungen hinzu:
     - `Files.Read.All` (Dateien lesen)
     - `Files.ReadWrite.All` (Dateien lesen und schreiben)
   - Speichere Client ID und Client Secret

2. **Abhängigkeiten installieren**
   ```bash
   pip install -e .
   # oder mit uv
   uv sync
   ```

3. **Umgebungsvariablen konfigurieren**
   ```bash
   cp .env.example .env
   # Bearbeite .env mit deinen Azure Credentials
   ```

4. **Server starten**
   ```bash
   python server.py
   # oder mit uv
   uv run server.py
   ```

## Verwendung

Der Server stellt folgende Tools zur Verfügung:

- `list_files(folder_path)` - Dateien in einem Ordner auflisten
- `upload_file(local_path, destination_path)` - Datei zu OneDrive hochladen
- `download_file(file_id, local_path)` - Datei von OneDrive herunterladen
- `delete_file(file_id)` - Datei von OneDrive löschen
- `get_file_info(file_id)` - Detaillierte Dateiinformationen abrufen

## API Berechtigungen

- **Files.Read.All** - Alle Dateien in OneDrive lesen
- **Files.ReadWrite.All** - Dateien lesen und schreiben
- **User.Read** - Benutzerprofil lesen