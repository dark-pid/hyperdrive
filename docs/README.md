# Hyperdrive

> _Table of Content:_
> - [Hyperdrive API](#hyperdrive-api) : API and messages description
>   - [Endpoints](#api-endpoints)
>   - [Messages](#api-messages)
> - [PID Dike Mechanism](#pid-dike-mechanism-pdm)
> - [Hyperdrive Transaction Verification Mechanism](#hyperdrive-transaction-verification-mechanism-htvm)




## Hyperdrive API

### Implementation Status

| name                     |  function     | method | status |
|:-                        | :-:           | :-:    | :-: |
|[assing_pid](#assing_pid) | no_parameter  | sync   | :bulb: |
|[assing_pid](#assing_pid) | no_parameter  | async  | :construction: |
|[assing_pid](#assing_pid) | external_url  | async  | :construction: |
|[assing_pid](#assing_pid) | external_pid  | async  | :construction: |
|[assing_pid](#assing_pid) | payload       | async  | :construction: |
|[get_pid](#get_pid)       | ark           | sync   | :heavy_check_mark: |
|[get_pid](#get_pid)       | hash_pid      | sync   | :heavy_check_mark: |
|[add](#add)               | external_pid  | sync   | :heavy_check_mark: |
|[add](#add)               | external_url  | sync   | :heavy_check_mark: |
|[set](#set)               | payload       | sync   | :heavy_check_mark: |
|[add](#add)               | external_pid  | async  | :heavy_check_mark: |
|[add](#add)               | external_url  | async  | :heavy_check_mark: |
|[set](#set)               | payload       | async  | :heavy_check_mark: |
|[login_user](#login_user) | email and password | sync   | :heavy_check_mark: |

**status :**
> - :heavy_check_mark: : done
> - :construction: : under construction
> - :bulb: : refactoring or improvement
> - :x: : not implemented
> - ⬜ : todo

### API Endpoints


The user must be authenticated to use this methods

- [Assing PID](#assing-pid): request a PID to the hyperdrive
- [Set](#set): set a PID attributes

The following method do not reequire authentication
- [Get](#get_pid): retrieve a PID



#### Assing PID
<details>
 <summary><code>POST</code> <code><b>/core/new</b></code> <code>(retrieve a new PID)</code></summary>

##### header parameter

> | name      |  type     | data type               | description                                                           |
> |----|---|---|---|
> | Authorization     |  required | str    | the api auth key  |

NOTE: if authentication is disabled, it will not be mandatory to use Authorization. When sending the JWT token in Authorization, ensure that "Bearer" is sent before the token (see example)

##### Parameters

> | name      |  type     | data type               | description                                                           |
> |----|---|---|---|
> | external_url     |  optional | str    | external url   |
> | external_pid     |  optional | str    | external pid   |
> | payload          |  optional | json   | pid paylload  |

##### Responses

> | http code     | content-type       | response |
> |----|---|---|
> | `200`         | `application/json; charset=utf-8` | see response [paramerter detail](#api-messages) |
> | `40x`         | `application/json; charset=utf-8` | see response [paramerter detail](#api-messages) |
> | `50x`         | `application/json; charset=utf-8` | see response [paramerter detail](#api-messages) |


##### Example cURL [POST]

> ```javascript
>  curl -X POST http://localhost:8080/core/new -H 'Content-Type: application/json ' -H 'Authorization: Bearer $your_access_token' -d '{"external_pid":"doi-number"}'
> ```


##### Example browser [GET]

> ```
>  http://http://localhost:8080/core/new?external_pid=doi-number
> ```
</details>

#### ADD
<details>
 <summary><code>POST</code> <code><b>/core/add/{ark}|{hash_pid}</b></code> <code>(add an attribute to PID)</code></summary>

##### header parameter

> | name      |  type     | data type               | description                                                           |
> |----|---|---|---|
> | Authorization     |  required | str    | the api auth key  |

NOTE: if authentication is disabled, it will not be mandatory to use Authorization. When sending the JWT token in Authorization, ensure that "Bearer" is sent before the token (see example)

##### Parameters

> | name      |  type     | data type               | description                                                           |
> |----|---|---|---|
> | external_url     |  optional | str    | external url   |
> | external_pid     |  optional | str    | external pid   |

##### Responses

> | http code     | content-type       | response |
> |----|---|---|
> | `200`         | `application/json; charset=utf-8` | see response [paramerter detail](#api-messages) |
> | `40x`         | `application/json; charset=utf-8` | see response [paramerter detail](#api-messages) |
> | `50x`         | `application/json; charset=utf-8` | see response [paramerter detail](#api-messages) |


##### Example cURL [POST]

> ```javascript
>  curl -X POST http://localhost:8080/core/add/8008/fk3abd1344 -H 'Content-Type: application/json' -H 'Authorization: Bearer $your_access_token' -d '{"external_pid":"doi-number"}'
> ```

</details>


#### SET
<details>
 <summary><code>POST</code> <code><b>/core/set/{ark}|{hash_pid}</b></code> <code>(set PID attribute)</code></summary>

##### header parameter

> | name      |  type     | data type               | description                                                           |
> |----|---|---|---|
> | Authorization     |  required | str    | the api auth key  |

NOTE: if authentication is disabled, it will not be mandatory to use Authorization. When sending the JWT token in Authorization, ensure that "Bearer" is sent before the token (see example)

##### Parameters

> | name      |  type     | data type               | description                                                           |
> |----|---|---|---|
> | external_url     |  optional | str    | external url   |
> | payload          |  optional | json   | pid paylload   |

##### Responses

> | http code     | content-type       | response |
> |----|---|---|
> | `200`         | `application/json; charset=utf-8` | see response [paramerter detail](#api-messages) |
> | `40x`         | `application/json; charset=utf-8` | see response [paramerter detail](#api-messages) |
> | `50x`         | `application/json; charset=utf-8` | see response [paramerter detail](#api-messages) |


##### Example cURL [POST]

> ```javascript
>  curl -X POST http://localhost:8080/core/set/8008/fk3abd1344 -H 'Content-Type: application/json' -H 'Authorization: Bearer $your_access_token' -d '{"external_pid":"doi-number"}'
> ```

</details>

#### GET PID
<details>
 <summary><code>GET</code> <code><b>/core/get/{ark}|{hash_pid}</b></code> <code>(retrieve a PID from blockchain)</code></summary>

##### Parameters

> | name      |  type     | data type               | description                                                           |
> |----|---|---|---|
> | ark     |  required | str   | ark_id   |
> | hash_pid     |  required | str   | hash_pid  |

##### Responses

> | http code     | content-type       | response |
> |----|---|---|
> | `200`         | `application/json; charset=utf-8` | see response [paramerter detail](#api-messages) |
> | `40x`         | `application/json; charset=utf-8` | see response [paramerter detail](#api-messages) |
> | `50x`         | `application/json; charset=utf-8` | see response [paramerter detail](#api-messages) |

##### Example [GET]

> ```
>  http://http://localhost:8080/core/get/0xd5e7a6c7f0a45e40d910d2cf1fa3d7f18e5f3a21257e0bbb115308dfb9ac75ab
> ```

> ```
>  http://http://localhost:8080/core/get/8008/fk3abd1344
> ```
</details>

## User Access

### user auth method

Through this method the user authenticates:

- [Login User](#login-user): authenticates the user using their data in the database.


#### Login User

<details>
 <summary><code>POST</code> <code><b>/user/login</b></code> <code>(authenticate user)</code></summary>

##### Parameters

> | name      |  type     | data type               | description                                                           |
> |----|---|---|---|
> | email    |  required | str    | user identification email  |
> | password     |  required | str    | user identification password  |


##### Responses

> | http code     | content-type       | response |
> |----|---|---|
> | `200`         | `application/json; charset=utf-8` | see response [paramerter detail](#api-messages) |
> | `40x`         | `application/json; charset=utf-8` | see response [paramerter detail](#api-messages) |
> | `50x`         | `application/json; charset=utf-8` | see response [paramerter detail](#api-messages) |

NOTE: The user login method response presents some Messages API parameters explained in [paramerter detail](#api-messages) . Below are only the parameters that are exclusive to the method and an example response.

| parameter | description | type | values   |
| ---       | ---         | ---  | ---      |
| api_auth_key       | the access token that references the user | str | token JWT |
| refresh_auth_key       | allows access token renewal without the need for the user to log in again | str | resfresh token JWT |

Below we present the parameters in more detail:

> 1. api_auth_key: this parameter refers to the JWT access token that authorizes the user to access the Hyperdrive API methods. It is returned as a string and is available in synchronous and asynchronous modes.
> 1. refresh_auth_key: This parameter allows the access token to be renewed without the need for the user to log in again.

Finally the response message will have the following structure:


```json
{
 action: athenticate,
 api_auth_key : eyJhbGciOnR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI.6R95X82cQPuN7MvZqP0DQjG1BY2a3vI,
 refresh_auth_key : eyJhbGciOnR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI.6R95X82cQPuN7MvZqP0DQjG1BY2a3vI,
 status : executed|rejeceted,
 error_code : 500,
 error_msg : invalid credentials,
}
```


##### Example cURL [POST]

> ```javascript
>  curl -X POST http://$API_HOST:$API_PORT/user/login -H 'Content-Type: application/json' -d '{"email":"valid_email", "password" : "valid_password" }'
> ```
</details>

### API Messages

In this section we present the HyperDrive response, in the following table we summarize all response elements/parameters: <br>

| parameter | description | type | atribute availability | values   |
| ---       | ---         | ---  | ---      | --- |
| pid       | the pid that the action refers. | str | sync and async|  |
| pid_hash_index       | the pid hash values | str | sync and async|  |
| hyperdrive_op_mode | the hyperdrive operation mode has two possible response | str | sync and async|     - sync: if the HyperDrive is in syncronized mode <br> - async : if the HyperDrive is in asyncronized mode |
| action | the action that is requested | json | sync and async |   - new_pid <br>    - add_url <br>    - add_external_pid<br>     - set_payload<br> | json |
| parameters | the request parameters  | json | sync and async | - external_url <br> - external_pid <br> - payload <br> | - |
| status | the status of the request | str | sync and async | - executed (sync mode status) <br> - queued (async mode status) <br> - rejected (error messages)
| transaction_hash | the blockchain transaction hash | str | async | the transaction hash is hex number avaliable only in `async mode` |
| error_code | the error code     | str | sync and async | only if the status is `rejected`  |
| error_msg | the error message   | str | sync and async | only if the status is `rejected`  |

Understanding these parameters is crucial for effectively interacting with the API and utilizing its capabilities, in the following we provide further detail of the messages:

> 1. pid: This parameter represents a unique identifier for a specific object. It's returned as a string and is available in both synchronous and asynchronous modes.
> 1. pid_hash_index: This parameter holds a blockchain internal index of the PID.
> 1. hyperdrive_op_mode: : The 'hyperdrive_op_mode' parameter indicates the operational mode of HyperDrive. It can be either "sync" or "async," signifying synchronized or asynchronous operation, respectively.
> 1. action: specifies the action requested through the API. It can take on various values, including "set_payload," "new_pid," "add_url," and "add_external_pid." These values indicate different operations or tasks that the API can perform. This parameter is represented in JSON format and is available in both sync and async modes.
> 1. parameters: Contains additional information required for the requested action. It's structured as JSON and may include values such as 'pid,' 'external_url,' and 'payload.' These values vary depending on the specific action requested.
> 1. status: reflects the status of the API request. It can have one of three values: "executed" (indicating successful execution in sync mode), "queued" (suggesting the task is awaiting processing in async mode), or "rejected" (implying that the request encountered an error).
> 1. transaction_hash: In asynchronous mode, the 'transaction_hash' parameter comes into play. It holds the blockchain transaction hash, represented as a hexadecimal number. If the HyperDrive is executing over the sync mode the parameter will not be presented in API response.
> 1. error_code : this parameter is only avalible if an error occur ( if the status is `rejected`)
> 1. error_msg : this parameter is only avalible if an error occur ( if the status is `rejected`)


Finally the response message will have the following structure:


```json
{
 pid: 8008/fk3abd1344 ,
 pid_hash_index : 0xffffff,
 hyperdrive_op_mode: [sync|async],
 action: set_payload|new_pid|add_url|add_external_pid
 parameters : { pid: 8033/fk819 , external_url : dark.io/xpto } ,
 status : executed|queued|rejeceted,
 transaction_hash : 0xffff,
 error_code : 500,
 error_msg : Blockchain is down,
}
```

## PID Dike Mechanism (PDM)

Need to be deailed

## Hyperdrive Transaction Verification Mechanism (HTVM)

Need to be deailed


