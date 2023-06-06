# dARK Hyperdrive

dARK Hyperdrive repository 

## Hyperdrive over view

``` mermaid
%%{init: {'theme': 'neutral' } }%%
graph LR
    DA[dARK]
    MR[IPFS]
    DS[DSPACE]
    HD[HyperDriver]

    %% subgraph TD SS ["Space Shuttles" ]
    %%     HD
    %% end
    
    subgraph TD GC ["Galaxy Center" ]
        DA
        MR
    end    

    DS --> | REQUEST| HD
    HD .-> DA
    HD .-> MR
    HD --> |RESPONSE| DS
```

## System requirements

- Python 3.8

## Deploy Instructions