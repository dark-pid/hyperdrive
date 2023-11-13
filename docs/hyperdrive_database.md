# Hyperdrive Database

## How to run

<details>
<summary>System Requirements</summary>
    <ul>
        <li> python 3.10 </li>
        <li>flask-sqlalchemy 3.1.1</li>
        <li> PostgresSQL 16 </li>
    </ul>
</details>

## parameter settings

In HyperDrive it is possible to configure the connection to the Database through the following configuration variables:

| parameter name | description | parameter value by default |
| --- | --- | --- |
| DB_HOST | configures the IP address or hostname of the PostgreSQL server | 127.0.0.1 |
| DB_PORT | configures the port used to connect to the PostgreSQL server | 5432 |
| DB_PASS | configures PostgreSQL database user password | postgres |
| DB_USER | configures the username used to authenticate the connection to the PostgreSQL database | postgres |
| DB_NAME | configures the name of the PostgreSQL database to which the project will connect | hyperdrive |

The system administrator user can modify the default values ​​of the environment variables using the following method, present in the configure_hyperdrive.py file:

#### config variables

<details>

##### Parameters

> | name      |  type     | data type               |
> |----|---|---|
> | DB_HOST     |  optional | str    |
> | DB_PORT     |  optional | str    |
> | DB_PASS     |  optional | str    |
> | DB_USER          |  optional | str   |
> | DB_NAME          |  optional | str   |

If the user does not pass any of the parameters, it will continue with its default value

</details>

## create database

By configuring the environment variables and having PostgresSQL active on the machine, the system administrator user will be able to initialize the following function to create the database tables

<details>

##### create tables

the function has no parameters, it creates the following tables in the database

</details>
