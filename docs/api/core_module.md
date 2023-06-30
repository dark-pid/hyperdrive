 # Hyperdrive Core Module

 Description 
 - problema da data deposito
	- a "data" de criacao do pid fica prejudicada
	- inserir um campo para isso?


## Hyperdrive Core API Methods


### PID Manipulation

The user must be authenticated to use this methods

- Assing PID: request a PID to the hyperdrive

description


#### Assing PID
<details>
 <summary><code>GET</code> <code><b>/core/pid//new</b></code> <code>(retrieve a new PID)</code></summary>

##### Parameters

> | name      |  type     | data type               | description                                                           |
> |----|---|---|---|
> | api_auth_key     |  required | str   | the api auth key  |

##### Responses

> | http code     | content-type                      | response                                                            |
> |----|---|---|
> | `200`         | `text/plain;charset=UTF-8`        | `{"pid":"8008/fk3abd1344"}`                                |
> | `400`         | `application/json`                | `{"code":"400","message":"Bad Request"}` |
> | `405`         | `text/html;charset=utf-8`         | None |

##### Example cURL

> ```javascript
>  curl -X GET -H "Content-Type: application/json" http://localhost:8889/core/pid/new
> ```

</details>

------------------------------------------------------------------------------------------

#### Set External PID
<details>
 <summary><code>PUT</code> <code><b>/core/pid//set_external_pid/{ark_id}</b></code> <code>(update a ark with an external PID)</code></summary>

##### Parameters

> | name      |  type     | data type               | description                                                           |
> |----|---|---|---|
> | api_auth_key     |  required | str   | the api auth key  |
> | ark_id       |  required | str   | the ark pid to be updated  |
> | external_pids |  required | str (json)   | the external pid  |
>
> The json of the external_pids should contain a list with all pids that will be added to the PID. For example:
>
>``` json 
> { external_pids : ["10.101.3.88.786"] }
> ```
> or
> ``` json 
> { external_pids : ["10.101.3.88.786","10.101.3.88.787","10.101.3.88.788"] }
> ```

##### Responses

> | http code     | content-type | response |
> |----|---|---|
> | `200`         | `text/plain;charset=UTF-8`        | `{"code":"200", "tx":["0xff67912abd"] }` or `{"code":"200", [ "tx":["0xff67912abd","0xff67912aba"] }`|
> | `400`         | `application/json`                | `{"code":"400","message":"Bad Request"}` |

##### Example cURL

> ```javascript
>  curl -X PUT -H "Content-Type: application/json" --data @put.json http://localhost:8889/core/pid//set_external_pid/'8008/fk3abc123'/
> ```

</details>

------------------------------------------------------------------------------------------

#### Set External link
<details>
 <summary><code>PUT</code> <code><b>/core/pid//set_external_link/{ark_id}</b></code> <code>(update a ark with an external link/url)</code></summary>

##### Parameters

> | name      |  type     | data type               | description                                                           |
> |----|---|---|---|
> | api_auth_key     |  required | str   | the api auth key  |
> | ark_id       |  required | str   | the ark pid to be updated  |
> | external_links |  required | str (json)   | the external links  |
>
> The json of the external_links should contain a list with all urls that will be added to the PID. Fro example:
>
>``` json 
> { external_links : ["www.google.com"] }
> ```
> or
> ``` json 
> { external_links : ["10.101.3.88.786","10.101.3.88.787","10.101.3.88.788"] }
> ```

##### Responses

> | http code     | content-type | response |
> |----|---|---|
> | `200`         | `text/plain;charset=UTF-8`        | `{"code":"200", "tx":["0xff67912abd"] }` or `{"code":"200", [ "tx":["0xff67912abd","0xff67912aba"] }`|
> | `400`         | `application/json`                | `{"code":"400","message":"Bad Request"}` |

##### Example cURL

> ```javascript
>  curl -X PUT -H "Content-Type: application/json" --data @put.json http://localhost:8889/core/pid//set_external_pid/'8008/fk3abc123'/
> ```

</details>

------------------------------------------------------------------------------------------

#### Set Payload
<details>
 <summary><code>PUT</code> <code><b>/core/pid//set_payload/{ark_id}</b></code> <code>(update a ark with an payload)</code></summary>

##### Parameters

> | name      |  type     | data type               | description                                                           |
> |----|---|---|---|
> | api_auth_key     |  required | str   | the api auth key  |
> | ark_id       |  required | str   | the ark pid to be updated  |
> | payload |  required | str  | payload  |
>
> **The payload format will be defined**

##### Responses

> | http code     | content-type | response |
> |----|---|---|
> | `200`         | `text/plain;charset=UTF-8`        | `{"code":"200", "tx":["0xff67912abd"] }` |
> | `400`         | `application/json`                | `{"code":"400","message":"Bad Request"}` |


##### Example cURL

> ```javascript
>  curl -X PUT -H "Content-Type: application/json" --data @put.json http://localhost:8889/core/pid//set_payload/'8008/fk3abc123'/
> ```

</details>

------------------------------------------------------------------------------------------

#### Configure PID
<details>
 <summary><code>PUT</code> <code><b>/core/pid//deploy/{ark_id}</b></code> <code>(update all ark field - e.g., external pids,links and payload)</code></summary>

##### Parameters

> | name      |  type     | data type               | description                                                           |
> |----|---|---|---|
> | api_auth_key     |  required | str   | the api auth key  |
> | ark_id       |  required | str   | the ark pid to be updated  |
> | external_pids |  optional | str (json)   | the external pids  |
> | external_links |  optional | str (json)   | the external links  |
> | payload |  required | str  | payload  |
>
> **The payload format will be defined**

##### Responses

> | http code     | content-type | response |
> |----|---|---|
> | `200`         | `text/plain;charset=UTF-8`        | `response_json` |
> | `400`         | `application/json`                | `{"code":"400","message":"Bad Request"}` |
>
> the response json
> ```json
> {"code":"200", 
>	"tx_urls": [],
>	"tx_links": [],
>	"tx_payload": ["0xff67912abd"]
>}
> ```
> notice that __tx_urls__ and __tx_urls__ can be empty or contains a list of transactions

##### Example cURL

> ```javascript
>  curl -X PUT -H "Content-Type: application/json" --data @put.json http://localhost:8889/core/pid//set_payload/'8008/fk3abc123'/
> ```

</details>

------------------------------------------------------------------------------------------

<!-- ## s -->
