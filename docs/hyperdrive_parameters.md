# HyperDrive Parameters

> *Table of Contents:*
> - [HyperDrive Operation Mode](#operation-mode)
> - [HyperDrive Validations](#validations)

This page details the HyperDrive parameters.

## Operation Mode

- Sync
- Async

## Validations


| PARAMETER                                                         | VALIDATION METHODS        |
| ---                                                               | ---                       |
| [HYPERDRIVE_URL_VALIDATION](#url-validations)                     | BASIC, NONE               |
| [HYPERDRIVE_EXTERNAL_PID_VALIDATION](#external-pid-validatation)  | BASIC, NONE               |
| [HYPERDRIVE_PAYLOAD_VALIDATION](#payload-validation)              | BASIC, NONE               |



### URL Validations

The HyperDrive can perform check the URL of a dARK PID, we assume a simple validation schema detailed below.

The URL must comply with the following regex:

>```python
>     regex = ("((http|https)://)(www.)?" +
>             "[a-zA-Z0-9@:%._\\+~#?&//=]" +
>             "{2,256}\\.[a-z]" +
>             "{2,6}\\b([-a-zA-Z0-9@:%" +
>             "._\\+~#?&//=]*)")
>```


This pid validation method must be configured using a system variable `HYPERDRIVE_URL_VALIDATION`. If the variable is unset it must consider **NONE** validation method.

The HYPERDRIVE_URL_VALIDATION must be :

| parameter value | description | default  |
| --- | --- | --- |
| NONE| No validation will be performed | ✅  |
| BASIC | Perform the validation described here | ❌ |


### External PID Validatation

The HyperDrive can perform check the External PID of a dARK PID, we assume a simple validation schema detailed below.

We need that all pid starts with `<protocol>:/<pid>`. 

> - The `<protocol>` designates the pid system that handles/generates the pid (e.g., DOI)
> - The `<pid>` is the pid

For example, the `doi:/10.1016/j.datak.2023.102180` the `protocol==doi`, and `pid==10.1016/j.datak.2023.102180`. **The Hyperdrive will only forward the `<pid>` part to the blockchain.

**For this HyperDrive version, we will only accept the DOI as external pids.**

This pid validation method must be configured using a system variable `HYPERDRIVE_EXTERNAL_PID_VALIDATION`. If the variable is unset, it must consider the **NONE** validation method.

The HYPERDRIVE_EXTERNAL_PID_VALIDATION must be :

| parameter value | description | default  |
| --- | --- | --- |
| NONE| No validation will be performed | ✅  |
| BASIC | Perform the validation described here | ❌ |

### Payload Validation

The HyperDrive can perform check the PAYLOAD of a dARK PID, we assume a simple validation schema detailed below.

- Check if the user submitted a valid JSON.

This pid validation method must be configured using a system variable `HYPERDRIVE_PAYLOAD_VALIDATION`. If the variable is unset, it must consider the **NONE** validation method.

The HYPERDRIVE_PAYLOAD_VALIDATION must be :

| parameter value | description | default  |
| --- | --- | --- |
| NONE| No validation will be performed | ✅  |
| BASIC | Perform the validation described here | ❌ |

