# web-apps-hw5
Group Homework 5 for CSCI 4710 Web Applications 

This application uses PostgreSQL. Please make sure that it is installed on your machine.


To set up the database, run the following command. This command will run psql as the postgres user.

```
sudo -u postgres psql
```
You should now be in a psql prompt. The prompt lines should start with ```postgres=#```

```
create database hw5db;
create user admin5 with encrypted password 'web_apps';
grant all privileges on database hw5db to admin5;
```

These commands will create a database ```hw5db```, a user ```admin5```, and then give that user privileges on the database. All further database operations are handled by the application. 


To start the application, you'll first want to create a venv and install the needed tools. Run the following commands from within the same directory as this README.md file.

Create the virtual environment:
```
python3 -m venv venv
```

Activate the virtual environment:
```
source venv/bin/activate
```

Install required tools:
```
pip3 install -r requirements.txt
```

You can then run the application with the following command:
```
python3 main.py
```