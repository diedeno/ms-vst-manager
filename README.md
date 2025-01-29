# MuseScore VST Manager

## Introduction
The MuseScore VST Manager is a utility for managing VST plugin configurations in MuseScore. It provides a simple interface to enable, disable, delete, search, and back up plugin information.

## Features
- **Search Plugins**: Dynamically filter the plugin list by typing keywords.
- **Enable/Disable Plugins**: Toggle the enabled state of a plugin with a double-click.
- **Delete Plugins**: Remove plugins by clicking the X symbol.
- **Backup Configuration**: Save a timestamped backup of the JSON configuration file.
- **Save Changes**: Apply modifications to the JSON configuration file.
- **Sort Columns**: Click column headers to sort data.

## Requirements
- Python 3.10 or later
- Tkinter (usually included with Python)

## Installation
1. Download the `ms-vst-manager.py` script or `ms-vst-manager.pyw` (on Windows, use .pyw to suppress the terminal).
2. Verify that the JSON configuration file exists:
   - **Windows**: `%localappdata%\MuseScore\MuseScore4\known_audio_plugins.json`
   - **Linux**: `~/.local/share/MuseScore/MuseScore4/known_audio_plugins.json`
   - **macOS**: `~/Library/Application Support/MuseScore/MuseScore4/known_audio_plugins.json`

## Usage
### Running the Application
Run the script:
   - **Windows**: Double-click the `.pyw` file.
   - **macOS/Linux**: Run `python3 ms-vst-manager.py` in the terminal.


### User Interface
- **Columns**:
  - Category
  - ID (Plugin Name)
  - Vendor
  - Path
  - Enabled (✔ or ✘)
  - Error Code
  - Delete (X)
- **Search Bar**: Filters plugins as you type.
- **Control Buttons**:
  - `Backup`: Creates a backup of the JSON configuration file.
  - `Save`: Saves changes to the JSON configuration file.
  - `Exit`: Closes the application.

### Key Actions
- **Search**: Enter text in the search bar to filter the plugin list dynamically.
- **Enable/Disable**: Double-click the Enabled (✔ or ✘) column to toggle the state.
- **Delete**: Click the X symbol in the Delete column to remove a plugin (confirmation required).
- **Backup**: Click the `Backup` button to save a timestamped backup of the JSON file.
- **Save**: Click the `Save` button to save all changes to the JSON file.

## Troubleshooting
### Application Doesn’t Start
- Ensure Python 3.10 or later is installed.
- Verify Tkinter is available in your Python installation.
- Confirm that the JSON configuration file exists in the correct directory.

### No Plugins Displayed
- Check that the JSON file contains valid data.
- Verify file permissions to ensure the application can read the JSON file.

### Features Not Working
- Ensure the script is the latest version.
- Run the script in a terminal and look for error messages.

## License
This project is licensed under the **GPLv3**.


