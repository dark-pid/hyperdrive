# Hyperdrive

dARK Hyperdrive repository 

## Hyperdrive overview

![](./figures/hyperdrive_overview.png)

## HyperDrive Goals and Functionalities

For further information see our [Hyperdrive functionalities page](./hyperdrive_funcionalities.md)

## Hyperdrive Modules

The hyperdrive module is organized into four modules, as the figure above presents.

![](./figures/architecture/arch_modules_overview.png)

Each module has its specific functionality:
1. Hyperdrive Core Moule: This module is responsible to performs PID registration operations (e.g., adding or updating PID metadata or requesting a new PID for a new item).
1. Hyperdrive Query Module: This module executes queries over the dARK metadata. 
1. Hyperdrive Authentication Module: This module authenticates and authorizes the users. Moreover, this module is responsible for converting and aligning the Hyperdrives users to the Blockchain users' accounts (also named wallets)
1. Hyperdrive Configuration Module: This module configures the Hyperdrive services. For example, create or disable SMA.

### Modules Details

TODO: The modules are further detailed in ... 

1. Hyperdrive Core Moule:
    - PID Resolution: Hyperdrive provide the means to resolve PIDs to their associated digital objects or resources. When a PID is accessed or queried, the Hyperdrive handles the resolution process, returning the relevant information or redirecting the user to the appropriate location. This enables seamless access to resources identified by PIDs, regardless of any underlying changes in storage locations or metadata.
    - PID Registration and Management: APIs allow users to register and manage PIDs programmatically. Through these APIs, applications can automate the process of assigning PIDs to digital objects, associating metadata with PIDs, updating or modifying PID records, and handling PID lifecycle events, such as deactivation or reassignment. This streamlines the management of PIDs and ensures their persistence and accuracy over time.
1. Hyperdrive Query Module:
    PID Metadata Retrieval: APIs enable the retrieval of metadata associated with PIDs. This metadata may include descriptive information about the digital object, such as title, author, date, or any other relevant attributes. By accessing this metadata programmatically through APIs, applications can enrich their functionality, provide context to users, and support advanced search and discovery features.
1. Hyperdrive Authentication Module
    - By leveraging Hyperdrive, applications can seamlessly interact with these infrastructure components, ensuring proper handling of requests, authentication, authorization, and adherence to PID-related standards and protocols.
    - TODO: ADD MORE INFO
1. Hyperdrive Configuration Module:
    - TODO: ADD MORE INFO


### Modules User Interecations

For further information see our [Hyperdrive user view page](./hyperdrive_modules_user_views.md)

## API Especification

The modules are further detailed in 

1. [Hyperdrive Core Moule](./api/core_module.md)
1. Hyperdrive Query Module
1. [Hyperdrive Authentication Module](./api/auth_module.md)
1. Hyperdrive Configuration Module

## System requirements

- Python 3.8 or superior

<details>
<summary>Documentation requirements</summary>

We are employ the MARP over the VSCode with the folowing extensions

1. [Markdown Preview Enhanced](https://github.com/shd101wyy/vscode-markdown-preview-enhanced)
1. [Markdown Mermaid](https://github.com/mjbvz/vscode-markdown-mermaid)
1. [MARP](https://github.com/marp-team/marp-vscode)
1. [Mermaid Editor](https://marketplace.visualstudio.com/items?itemName=tomoyukim.vscode-mermaid-editor)

### Mermaid Diagrams

1. Install the Mermaid Editor
2. Configure the vscode (Create or edit the .vscode configuration files)
    - create a folder .vscode
    - create or edit the settings.json file adding the folowing parameters

```json
{
    "mermaid-editor": {
        "generate": {
            "type": "png",
            "scale": 4.0
        }
    }
}
```

### MARP

#### Windows

1. Install scoop https://scoop.sh/

```
> Set-ExecutionPolicy RemoteSigned -Scope CurrentUser # Optional: Needed to run a remote script the first time
> irm get.scoop.sh | iex
```

2. Install MARP
```
scoop install marp
```

3. Export Files


```
marp .\presentation.md --pdf
marp .\presentation.md --html
```

If inside visual studio code use the full path of marp comand

```
C:\Users\thiag\scoop\shims\marp.exe .\presentation.md --pdf
```

TODO: add system marp to code ps path
</details>

## Deploy Instructions

