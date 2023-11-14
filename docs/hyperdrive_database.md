# Hyperdrive Database

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

In HyperDrive it is possible to configure the connection to the Database through the following configuration variables:

| parameter name | description | parameter value by default |
| --- | --- | --- |
| DB_HOST | configures the IP address or hostname of the PostgreSQL server | 127.0.0.1 |
| DB_PORT | configures the port used to connect to the PostgreSQL server | 5432 |
| DB_PASS | configures PostgreSQL database user password | postgres |
| DB_USER | configures the username used to authenticate the connection to the PostgreSQL database | postgres |
| DB_NAME | configures the name of the PostgreSQL database to which the project will connect | hyperdrive |

The system administrator user can modify the default values ​​of the environment variables using the following method, present in the configure_hyperdrive.py file:

<details>

<summary>config variables</summary>

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

By setting the environment variables and having PostgresSQL active on the machine, the system administrator user will be able to initialize the following function to create the database

<details>

<summary>create database</summary>

the function has no parameters and will use Flask SQLAlchemy to create the database. It is important that the environment variables, described previously, are configured with the correct values.

</details>
</br>
After that, it will be able to create tables in the database using the following method
</br>
</br>
<details>

<summary>create tables</summary>

the function has no parameters, it creates the following tables specified in the diagram available at

[https://github.com/dark-pid/hyperdrive/blob/develop/docs/diagrams/entities_on_and_off_chain.mmd](https://github.com/dark-pid/hyperdrive/blob/develop/docs/diagrams/entities_on_and_off_chain.mmd)

</details>
</br>
<details>

<summary>create user account</summary>

The function receives as a parameter the data of one user at a time to be inserted into the database by the system administrator user

##### Parameters

> | name      |  type     | data type               |
> |----|---|---|
> | Name    |  required | str    |
> | Organization    |  required | str    |
> | Email    |  required | str    |
> | wallet_private_key    |  required | str    |

</details>
