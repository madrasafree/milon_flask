Dear Developers,
Welcome to Madrasa community dictionary repository!

To compile the repository one must:
1. Install "Python" environment 3.7 or newer.
2. Clone the Repository locally from Github:
	https://github.com/madrasafree/milon_flask
3. Install the libraries:
	pip install -r /milon_flask/requirements.txt
4. Install "PostgreSQL" DB Server Engine:
	https://www.postgresql.org/download/
5. Open Firewall Port for PostgreSQL:
	https://www.project-open.com/en/howto-postgresql-port-secure-remote-access
6. Open "pgAdmin 4" control panel:
	a. Set a password (1234)
	b. Create new server:
		Object -> Create -> Server:
		Server Name (madrasa_flask), Host Address (127.0.0.1), Port (5432), Username (postgres), Maintenance database (postgres).
	c. Create new empty tables:
		Tools -> Query Tool -> paste and run the Query from repository under /milon_flask/research/create_tables.sql
	d. Confirm you find the tables:
		Browser -> "madrasa_flask" -> Databases -> postgres -> Schemas -> pubic -> Tables
7. Edit source/arabic_words_db.py with Host Address, Port, Username, Password, Maintenance database.
8. Edit source/main.py with Host Address and different Port (5431).
9. Install "Microsoft Access Database Engine":
	https://www.microsoft.com/en-us/download/details.aspx?id=54920
10. Load PostgreSQL with Dictionary DataBase file .mdb by running:
	python -m research.import_db_from_windows
10. Start-up the dictionary locally by running:
	python -m source.main