
# Madrasa Community Dictionary Repository

Welcome to the Madrasa community dictionary repository!

This project is an initiative by Madrasa to migrate the technology of the Spoken Arabic Dictionary from ASP Classic to Python Flask.

## Compilation Instructions (DEV Mode)

### Step 1: Install Python
Ensure you have Python 3.7 or newer installed on your system.

### Step 2: Clone the Repository
Clone the repository locally from GitHub:
```bash
git clone https://github.com/madrasafree/milon_flask
```

### Step 3: Install Libraries
Install the required libraries:
```bash
pip install -r milon_flask/requirements.txt
```

### Step 4: Install PostgreSQL
Install the PostgreSQL DB Server Engine:
[PostgreSQL Download](https://www.postgresql.org/download/)

### Step 5: Open Firewall Port for PostgreSQL
Follow instructions to open the PostgreSQL port:
[PostgreSQL Port Secure Remote Access](https://www.project-open.com/en/howto-postgresql-port-secure-remote-access)

### Step 6: Configure pgAdmin 4
Open the pgAdmin 4 control panel at `http://127.0.0.1:50454/browser/#`

1. Set a password (e.g., `1234`)
2. Create a new server:
   - Navigate to `Object -> Create -> Server`
   - Set the following details:
     - Server Name: `madrasa_flask`
     - Host Address: `127.0.0.1`
     - Port: `5432`
     - Username: `postgres`
     - Maintenance database: `postgres`

3. Create new empty tables:
   - In the browser, find `madrasa_flask/Databases/postgres/Schemas`
   - Right-click and select `Query Tool`
   - Paste and run the query from the repository located at `/milon_flask/source/build/create_tables.sql`

4. Confirm the tables:
   - Navigate to `madrasa_flask -> Databases -> postgres -> Schemas -> public -> Tables`

### Step 7: Edit Configuration
Edit `source/config/config.py` with the following details:
- Host Address
- Port_DB
- Port_APP (`5431`)
- Username
- Maintenance database

### Step 8: Set Environment Variable
Add a password to Windows Environment Variables under the name: `MADRASA_SERVER_KEY_SECRET_DEV`

### Step 9: Install Microsoft Access Database Engine
Install the Microsoft Access Database Engine:
[Microsoft Access Database Engine Download](https://www.microsoft.com/en-us/download/details.aspx?id=54920)

### Step 10: Load PostgreSQL with Dictionary Database
1. Edit `source/scripts/import_db_from_windows.py` to load the relevant table under the `# Editable Variables` section.
2. Navigate to the source directory:
   ```bash
   cd source
   ```
3. Run the import script:
   ```bash
   python build/import_db_from_windows.py
   ```

### Step 11: Start the Dictionary
1. Navigate to the source directory:
   ```bash
   cd source
   ```
2. Start the dictionary locally:
   ```bash
   python -m main
   ```

### Step 12: Open in Browser
Open Chrome and navigate to `http://127.0.0.1:5431/`

---

Feel free to reach out if you encounter any issues or need further assistance. Happy coding!
