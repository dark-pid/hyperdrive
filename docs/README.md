## Hyperdrive API

### Implementation Status

| name                     |  function     | method | status |
|:-                        | :-:           | :-:    | :-: | 
|[Assing PID](#assing_pid) | no_parameter  | sync   | :heavy_check_mark: |
|[Assing PID](#assing_pid) | external_pid  | sync   | ⬜ |
|[Assing PID](#assing_pid) | payload       | sync   | ⬜ |
|[Get PID](#get_pid)       | ark           | sync   | :heavy_check_mark: |
|[Get PID](#get_pid)       | hash_pid      | sync   | :heavy_check_mark: |
|[Set](#set)               | external_pid  | sync   | ⬜ |
|[Set](#set)               | payload       | sync   | ⬜ |



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
> | api_auth_key     |  required | str    | the api auth key  |
> | external_pid     |  optional | str    | external pid   |
> | payload          |  optional | json   | pid paylload  |

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
> | api_auth_key     |  required | str    | the api auth key  |
> | external_pid     |  optional | str    | external pid   |
> | payload          |  optional | json   | pid paylload  |

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