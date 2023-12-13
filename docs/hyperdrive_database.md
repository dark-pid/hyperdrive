# Hyperdrive Database

The configure_database.py file plays a crucial role in the initial configuration of the database system.

## How to run

<details>
<summary>System Requirements</summary>
    <ul>
        <li> python 3.10 </li>
        <li> flask-sqlalchemy 3.1.1</li>
        <li> PostgresSQL 16 </li>
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

In the folder called database it is important that there is a CSV file named users. Each line of this file must contain the user data that will be added to the database once it is created with the configure_database.py file.

Then just run the configure_database.py file so that the database creates all the important tables for the hyperdrive as well as adding the user data present in the users.csv file.

NOTE: check the users.csv file present on the hyperdrive to understand how it should be. It is important to keep line one present in the example and each user on one line in the file.

```
>> cd app
>> python configure_database.py
```

These tables can be seen in [https://github.com/dark-pid/hyperdrive/blob/develop/docs/diagrams/entities_on_and_off_chain.mmd](https://github.com/dark-pid/hyperdrive/blob/develop/docs/diagrams/entities_on_and_off_chain.mmd).
