# Hyperdrive 


## Hyperdrive API

### Implementation Status

| name                     |  function     | method | status | release |
|:-                        | :-:           | :-:    | :-: | :-: |
|[assing_pid](#assing_pid) | no_parameter  | sync   | :heavy_check_mark: | 0.0.1 |
|[assing_pid](#assing_pid) | external_url  | sync   | ⬜ | - |
|[assing_pid](#assing_pid) | external_pid  | sync   | ⬜ | - |
|[assing_pid](#assing_pid) | payload       | sync   | ⬜ | - |
|[get_pid](#get_pid)       | ark           | sync   | :heavy_check_mark: | 0.0.1 |
|[get_pid](#get_pid)       | hash_pid      | sync   | :heavy_check_mark: | 0.0.1 |
|[set](#set)               | external_pid  | sync   | :heavy_check_mark: | 0.0.2 |
|[set](#set)               | external_url  | sync   | :heavy_check_mark: | 0.0.2 |
|[set](#set)               | payload       | sync   | :heavy_check_mark: | 0.0.2 | 
|[add](#add)               | external_pid  | sync   | ⬜ | - |
|[add](#set)               | external_url  | async  | ⬜ | - |
|[set](#set)               | payload       | async  | ⬜ | - |
|[add](#add)               | external_pid  | async  | ⬜ | - |

**status :**
> - :heavy_check_mark: : done
> - :x: : not implemented
> - ⬜ : todo

### Core


The user must be authenticated to use this methods

- Assing PID: request a PID to the hyperdrive

description


#### Assing PID
<details>
 <summary><code>POST</code> <code><b>/core/new</b></code> <code>(retrieve a new PID)</code></summary>

##### Parameters

> | name      |  type     | data type               | description                                                           |
> |----|---|---|---|
> | api_auth_key     |  required | str    | the api auth key (in future releases)  |
> | external_url     |  optional | str    | external url   |
> | external_pid     |  optional | str    | external pid   |
> | payload          |  optional | json   | pid paylload   |

##### Responses

> | http code     | content-type                      | response                                                            |
> |----|---|---|
> | `200`         | `text/plain;charset=UTF-8`        | `{"pid":"8008/fk3abd1344"}`                                |
> | `400`         | `application/json`                | `{"code":"400","message":"Bad Request"}` |
> | `405`         | `text/html;charset=utf-8`         | None |

##### Example cURL [POST]

> ```javascript
>  curl -X POST http://localhost:8080/core/new -H 'Content-Type: application/json' -d '{"external_pid":"doi-number"}'
> ```

##### Example browser [GET]

> ```
>  http://http://localhost:8080/core/new?external_pid=doi-number
> ```
</details>


#### SET
<details>
 <summary><code>POST</code> <code><b>/core/set/{ark}|{hash_pid}</b></code> <code>(set PID attribute)</code></summary>

##### Parameters

> | name      |  type     | data type               | description                                                           |
> |----|---|---|---|
> | api_auth_key     |  required | str    | the api auth key (in future releases)  |
> | external_url     |  optional | str    | external url   |
> | payload          |  optional | json   | pid paylload   |


##### Responses

> | http code     | content-type                      | response                                                            |
> |----|---|---|
> | `200`         | `text/plain;charset=UTF-8`        | `{"pid":"8008/fk3abd1344" , action: "external_pid_add" , transcation_recipt: "0xffff"}`                                |
> | `200`         | `text/plain;charset=UTF-8`        | `{"pid":"8008/fk3abd1344" , action: "payload_add", transcation_recipt: "0xffff"}`                                |
> | `400`         | `application/json`                | `{"code":"400","message":"Bad Request"}` |
> | `405`         | `text/html;charset=utf-8`         | None |

##### Example cURL [POST]

> ```javascript
>  curl -X POST http://localhost:8080/core/set/8008/fk3abd1344 -H 'Content-Type: application/json' -d '{"external_pid":"doi-number"}'
> ```

</details>

#### ADD
<details>
 <summary><code>POST</code> <code><b>/core/add/{ark}|{hash_pid}</b></code> <code>(add a attribute to PID)</code></summary>

##### Parameters

> | name      |  type     | data type               | description                                                           |
> |----|---|---|---|
> | api_auth_key     |  required | str    | the api auth key (in future releases)  |
> | external_pid     |  optional | str    | external pid   |


##### Responses

> | http code     | content-type                      | response                                                            |
> |----|---|---|
> | `200`         | `text/plain;charset=UTF-8`        | `{"pid":"8008/fk3abd1344" , action: "external_pid_add" , transcation_recipt: "0xffff"}`                                |
> | `200`         | `text/plain;charset=UTF-8`        | `{"pid":"8008/fk3abd1344" , action: "payload_add", transcation_recipt: "0xffff"}`                                |
> | `400`         | `application/json`                | `{"code":"400","message":"Bad Request"}` |
> | `405`         | `text/html;charset=utf-8`         | None |

##### Example cURL [POST]

> ```javascript
>  curl -X POST http://localhost:8080/core/set/8008/fk3abd1344 -H 'Content-Type: application/json' -d '{"external_pid":"doi-number"}'
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

> | http code     | content-type                      | response                                                            |
> |----|---|---|
> | `200`         | `text/plain;charset=UTF-8`        | `{"pid":"8008/fk3abd1344"}`                                |
> | `400`         | `application/json`                | `{"code":"400","message":"Bad Request"}` |
> | `405`         | `text/html;charset=utf-8`         | None |
##### Example [GET]

> ```
>  http://http://localhost:8080/core/get/0xd5e7a6c7f0a45e40d910d2cf1fa3d7f18e5f3a21257e0bbb115308dfb9ac75ab
> ```

> ```
>  http://http://localhost:8080/core/get/8008/fk3abd1344
> ```
</details>

### API Response messages


> | http code     | content-type                      | response                                                            |
> |----|---|---|
> | `200`         | `text/plain;charset=UTF-8`        | `{"pid":"8008/fk3abd1344", "actions"}`                                |
> | `400`         | `application/json`                | `{"code":"400","message":"Bad Request"}` |
> | `405`         | `text/html;charset=utf-8`         | None |


## Hyperdrive Transaction Verification Mechanism (HTVM)

Need to be deailed
