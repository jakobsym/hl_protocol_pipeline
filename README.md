# HyperLiquid Protocol/Token Metrics Pipeline
- TBA

## Architecture
```mermaid
flowchart TB
    %% Orchestrator
    Airflow["Orchestrator TBD"]

    %% Data Sources (No subgraph box)
    FinAPI1["Defi Llama API"]
    FinAPI2["Hyperscan API"]
    AzureBlob[("Azure Blob Storage")]

    %% ETL Process (Middle Level)
    subgraph ETLContainer["ETL Docker Container"]
        direction LR
        E["Extract"] --> T["Transform"]
        T --> L["Load"]
    end

    %% Storage Layer (Bottom Level)
    subgraph Storage["Storage Layer"]
        TimescaleDB[("TimescaleDB<br/>Staging")]
        Snowflake[("Snowflake<br/>Data Warehouse")]
    end

    %% Main orchestration flow
    Airflow -->|"Orchestrates"| ETLContainer

    %% Data flow from sources to ETL Extract
    FinAPI1 --> E
    FinAPI2 --> E
    AzureBlob --> E

    %% ETL data flow
    E -->|"Raw data"| TimescaleDB
    %%T -->|"Read staged data"| TimescaleDB
    L -->|"Load processed data"| Snowflake

    %% Styling with black text
    classDef orchestrator fill:#ffebcd,stroke:#ff8c00,stroke-width:3px,color:#000000
    classDef process fill:#d5f5e3,stroke:#1e8449,stroke-width:2px,color:#000000
    classDef database fill:#fdebd0,stroke:#d35400,stroke-width:2px,color:#000000
    classDef warehouse fill:#e8f4fd,stroke:#1f77b4,stroke-width:2px,color:#000000
    classDef storage fill:#f9e79f,stroke:#b7950b,stroke-width:2px,color:#000000
    classDef external fill:#ebdef0,stroke:#8e44ad,stroke-width:2px,color:#000000
    classDef container fill:#f8f9f9,stroke:#5d6d7e,stroke-width:2px,stroke-dasharray:5,color:#000000

    class Airflow orchestrator
    class E,T,L process
    class TimescaleDB database
    class Snowflake warehouse
    class AzureBlob storage
    class FinAPI1,FinAPI2 external
    class ETLContainer,Storage container
```