# Changelog

All notable changes to this project will be documented in this file.

### [0.0.2] 20/10/2023

Assyncronous version of the HyperDrive.

1. Added assyncrnous operation mode flag (`HYPERDRIVE_OPERATION_MODE` , detailed in issue #17). 
2. New (and refactored method):
    - [ x ] get new pid
    - [ x ] set external url
    - [ x ] add external pid
    - [ x ] set payload
3. Changes in hyperdrive return parameters (for further detail [see](docs/README.md))
4. New unt test

For further detail see our [documentation](docs/hyperdrive_parameters.md).

### [0.0.1] 14/09/2023

Syncronized  Version of the HyperDrive:

- [ x ] get new pid
- [ x ] set external url
- [ x ] set external pid
- [ x ] set payload

Validations

| VALIDATION                          | DESCRIPTIO                  |
| ---                                 | ---                         |
| HYPERDRIVE_URL_VALIDATION           | check if is a valid url     |
| HYPERDRIVE_EXTERNAL_PID_VALIDATION  | check if is a doi           |
| HYPERDRIVE_PAYLOAD_VALIDATION       | check if is a valid json    |

For further detail see our [documentation](docs/hyperdrive_parameters.md).