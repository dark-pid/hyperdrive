# Hyperdrive Database

The configure_hyperdrive.py file plays a crucial role in configuring and initializing the database system.

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

Before starting the config_database methods, it is important that all configuration variables have their correct values

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

It is necessary that postgresSQL is already installed and configured on the machine, and to use the methods it is important that there is a server created and named (DB_NAME). Then, use the command below in the terminal to call the method to create the tables in the database:

```
TO DO: put the command here after developing and testing the method
```

These tables can be seen in [https://github.com/dark-pid/hyperdrive/blob/develop/docs/diagrams/entities_on_and_off_chain.mmd](https://github.com/dark-pid/hyperdrive/blob/develop/docs/diagrams/entities_on_and_off_chain.mmd).

```
TO DO: put the command here after developing and testing the method
```

To insert data into the database tables, you must use the command below, passing a JSON with the values.

```
TO DO: put the command here after developing and testing the method
```

##### command parameters

> | name      |  type     | data type               |
> |----|---|---|
> | user_account    |  optional | json    |

##### Responses

> | http code     | content-type       | response |
> |----|---|---|
> | `200`         | `application/json; charset=utf-8` | TO DO: standardization to be considered after creating the method if necessary |
> | `40x`         | `application/json; charset=utf-8` | TO DO: standardization to be considered after creating the method if necessary |
> | `50x`         | `application/json; charset=utf-8` | TO DO: standardization to be considered after creating the method if necessary |


