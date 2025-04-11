# Password Manager

A simple password manager built with Python to securely store and manage your credentials.

## Features

- Easy-to-use graphical interface (Tkinter)
- Securely store credentials (username/password)
- Local SQLite database
- Add, view, and delete entries

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/TheoCaudan/password_manager.git
   cd password_manager
   ```
2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

How It Works

1. Database Setup:

   - When first run, the app sets up a local SQLite database via db_setup.py to store credentials securely.

2. User Interface:

    - ui.py launches a Tkinter-based graphical window.

    - You can input, view, or delete credentials with buttons and input fields.

3. Backend Logic:

    - The logic in backend.py handles the interaction between the GUI and the database (e.g., saving, retrieving, and deleting records).

## Usage

To run the password manager:

   ```bash
   python ui.py
   ```
This opens the password manager GUI. From there:

- Enter service name, username, and password.

- Click "Add" to save it.

- Use "View All" to see saved entries.

- Use "Delete" to remove any record.

## File Structure

- backend.py: Handles the core functionality for managing passwords and interact with the database.

- db_setup.py: Initializes SQLite database for storing credentials.

- ui.py: Main graphical app.

- __init__.py: Initializes the Python package.

## License

This project is licensed under the MIT License. Use freely and modify as needed!
