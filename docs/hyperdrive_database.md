# Hyperdrive Database

To initialize the database it is important to follow some steps. Additionally, there are some requirements that need to be installed.

## How to run

<details>
<summary>System Requirements</summary>
    <ul>
        <li> python 3.10</li>
        <li> flask-sqlalchemy 3.1.1</li>
        <li> PostgresSQL 16</li>
        <li> psycopg2-binary 2.9.9</li>
        <li> Flask-Bcrypt 1.0.1</li>
        <li> Flask-Migrate 4.0.5</li>
        <li> flask-marshmallow 0.15.0</li>
        <li> marshmallow-sqlalchemy 0.29.0</li>
    </ul>
</details>

## parameter settings

Before starting config_database, it is important that all configuration variables have their correct values.

| parameter name | description | parameter value by default |
| --- | --- | --- |
| DB_HOST | configures the IP address or hostname of the PostgreSQL server | 127.0.0.1 |
| DB_PORT | configures the port used to connect to the PostgreSQL server | 5432 |
| DB_PASS | configures PostgreSQL database user password | postgres |
| DB_USER | configures the username used to authenticate the connection to the PostgreSQL database | postgres |
| DB_NAME | configures the name of the PostgreSQL database to which the project will connect | hyperdrive |

To modify the default value of the variables, you need to open a terminal in the project folder and then start a python instance. Finally, in the following example you will find the commands for modifying variables.

```
>>> python
>>> import os
>>> os.environ["DB_HOST"] = "value"
>>> os.environ["DB_PORT"] = "value"
>>> os.environ["DB_PASS"] = "value"
>>> os.environ["DB_USER"] = "value"
>>> os.environ["DB_NAME"] = "value"
>>> quit()
```

If the user does not configure these variables, they will continue with their default values


## Create and Populate the Database

PostgresQL must already be installed and configured on the machine, and to use the methods it is important that there is a database created and named (DB_NAME) in postgres.

In the folder called database it is important that there is a CSV file named users. Each line of this file must contain the user data that will be added to the database once it is created.

NOTE: check the users.csv file present on the hyperdrive to understand how it should be. It is important to keep line one present in the example and each user on one line in the file.

Follow the commands below to create the tables in the database and then fill in the user table using a csv file:

```
>> cd app
>> python api_server.py
>> flask --app instance_app db upgrade
>> python import_csv.py
```

These tables can be seen in [https://github.com/dark-pid/hyperdrive/blob/develop/docs/diagrams/entities_on_and_off_chain.mmd](https://github.com/dark-pid/hyperdrive/blob/develop/docs/diagrams/entities_on_and_off_chain.mmd).
