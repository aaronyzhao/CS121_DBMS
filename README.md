# CS121_DBMS

Data was generated using a Python script. The corresponding menu closely aligns with CAVAs offerings and the descriptions, ingredients, and quantities required were all made up as a figment of Aaron's imagination. They are all stored in the data file.

To begin, we provide 2 separate ways of setting up this program. 

The first is an "easy start" by typing "SOURCE start.sql;" into the sql command line, it will create a new database, switch to it, set up the database according to the ER diagram and load in all corresponding data. Alternatively, if users wish to test all parts of the project at once, type "SOURCE comprehensive_test.sql;" which will do all that start.sql does and additionally execute "setup-passwords.sql", "grant-permissions.sql", "queries.sql", and "setup-routines.sql". 

### CLI instructions
1. Before beginning with the CLI, we need to enter MySQL and run `SOURCE comprehensive_test.sql;`, which sets up the database, loads all data, and sets up passwords, permissions, queries, and routines. 
2. To begin, you will need to install the one singular package dependency: `pip3 install mysql`
3. Now you can fully interact with the CLI. For admin CLI, `python3 app-admin.py`. For client CLI, `python3 app-client.py`.
4. Regardless of admin CLI or client CLI, the instructions will only prompt you for single letters or numbers to navigate and interact with the CLI and complete tasks. 
