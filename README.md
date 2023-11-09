# Hyperdrive

dARK Hyperdrive repository


## How to run

<details>
<summary>System Requirements</summary>
    <ul>
        <li> python 3.10 </li>
        <li> pip </li>
        <li> docker </li>
        <li> docker-compose </li>
        <li> PostgresSQL 16 </li>
    </ul>
</details>

### Docker execution

**build**
```
docker compose build
```

**run**
```
docker compose up -d
```

### Manual

**linux**
> ```
> $ cd hyperdrive
> $ pip install -r requirements
> $ cd app
> $ python api_server.py
> ```

**windows**
> ```
> cd hyperdrive
> pip install -r requirements
> cd app
> python.exe api_server.py
>```

### HyperDriver Configuration

see the [HyperDrive configuration parameters detail](docs/configuration_parameter.md).

### Screenshots

**Hyperdrive Query**

![](docs/figures/misc/payload_v0.png)
