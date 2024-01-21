Dear Developers,
Welcome to Madrasa community dictionary repository!

To compile the repository locally in DEV mode one must:
1. Install "Python" environment 3.7 or newer.
2. Clone the Repository locally from Github:
	https://github.com/madrasafree/milon_flask
3. Install the libraries:
	pip install -r /milon_flask/requirements.txt
4. Install "PostgreSQL" DB Server Engine:
	https://www.postgresql.org/download/
5. Open Firewall Port for PostgreSQL:
	https://www.project-open.com/en/howto-postgresql-port-secure-remote-access
6. Open "pgAdmin 4" control panel: (Address: http://127.0.0.1:50454/browser/#)
	a. Set a password (1234)
	b. Create new server:
		Object -> Create -> Server:
		Server Name (madrasa_flask), Host Address (127.0.0.1), Port (5432), Username (postgres), Maintenance database (postgres).
	c. Create new empty tables:
		In Browser, find madrasa_flask/Databases/postgres/Schemas -> Right Click -> Query Tool -> paste and run the Query from repository under /milon_flask/research/create_tables.sql
	d. Confirm you find the tables:
		Browser -> "madrasa_flask" -> Databases -> postgres -> Schemas -> pubic -> Tables
7. Edit source/arabic_words_db.py with Host Address, Port, Username, Maintenance database.
8. Add Password to Windows "Environment Variables" under name: "MADRASA_SERVER_KEY_SECRET_DEV"
9. Edit source/main.py with Host Address and different Port (5431).
10. Install "Microsoft Access Database Engine":
	https://www.microsoft.com/en-us/download/details.aspx?id=54920
11. Load PostgreSQL with Dictionary DataBase file .mdb by running:
	a. Edit source/scripts/import_db_from_windows.py to load the relevant table under "# Editable Variables" section.
	b. cd source
	c. python scripts/import_db_from_windows.py
12. Start-up the dictionary locally by running:
	a. cd source
	b. python -m main
13. Open from Chrome the host address (http://127.0.0.1:5431/)