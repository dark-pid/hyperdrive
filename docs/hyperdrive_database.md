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

In configure_hyperdrive.py it is possible to configure the connection to the Database through the following configuration variables present in variables_database.py:

| parameter name | description | parameter value by default |
| --- | --- | --- |
| DB_HOST | configures the IP address or hostname of the PostgreSQL server | 127.0.0.1 |
| DB_PORT | configures the port used to connect to the PostgreSQL server | 5432 |
| DB_PASS | configures PostgreSQL database user password | postgres |
| DB_USER | configures the username used to authenticate the connection to the PostgreSQL database | postgres |
| DB_NAME | configures the name of the PostgreSQL database to which the project will connect | hyperdrive |

In the configure_hyperdrive.py file it is possible to modify the default values ​​of the environment variables using the command:

```
TO DO: put the command here after developing and testing the method
```

##### command parameters

> | name      |  type     | data type               |
> |----|---|---|
> | DB_HOST     |  optional | str    |
> | DB_PORT     |  optional | str    |
> | DB_PASS     |  optional | str    |
> | DB_USER          |  optional | str   |
> | DB_NAME          |  optional | str   |

If the user does not pass any of the parameters, it will continue with its default value


## Create and Populate the Database

Once the database variables have been defined it will be possible to create a database using the create_database method which can be called using the command:

```
TO DO: put the command here after developing and testing the method
```

the function has no parameters and will use Flask SQLAlchemy to create the database. It is important that the environment variables, described previously, are configured with the correct values.

It is very important that the database is created so that the necessary tables for this database can be created. These tables can be seen in [https://github.com/dark-pid/hyperdrive/blob/develop/docs/diagrams/entities_on_and_off_chain.mmd](https://github.com/dark-pid/hyperdrive/blob/develop/docs/diagrams/entities_on_and_off_chain.mmd). The configure_hyperdrive.py file is responsible for creating these tables with the following command:

```
TO DO: put the command here after developing and testing the method
```

To insert data into the database tables, you must use the command below, passing a JSON with the values.

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

```
TO DO: put the command here after developing and testing the method
```
