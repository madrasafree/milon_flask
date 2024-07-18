
# Madrasa Community Dictionary Repository

Welcome to the Madrasa community dictionary repository!

## Getting your environment ready (DEV Mode)

### Step 1: Install Docker and docker-compose
https://docs.docker.com/get-docker/
https://docs.docker.com/compose/install/


### Step 2: Clone the Repository
Clone the repository locally from GitHub:
```bash
git clone https://github.com/madrasafree/milon_flask
```

## Starting the app
### Step 1: Navigate to the app's directory (the root directory you downloaded from the repo)
### Step 2: Start the containers
   ```bash
   docker compose up -d
   ```
### Step 3: Wait for the db to build
In Docker, click on the db container and look at the logs. 
You will probably see many lines of "INSERT ...". <br />
Wait to see "dump load done", which means the db is ready.
### Step 4: Open the app
Open Chrome and navigate to `http://127.0.0.1:5431/`

---

Feel free to reach out if you encounter any issues or need further assistance. Happy coding!
