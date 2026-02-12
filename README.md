# Astronomy Picture of the Day (APOD) ETL Pipeline with Airflow
![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-017CEE?style=flat&logo=apacheairflow&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![NASA API](https://img.shields.io/badge/NASA%20API-0B3D91?style=flat&logo=nasa&logoColor=white)
![ETL Pipeline](https://img.shields.io/badge/ETL%20Pipeline-2E7D32?style=flat)
![Git](https://img.shields.io/badge/Git-F05032?logo=git&logoColor=fff)

## Project Overview

This project implements an automated ETL (Extract, Transform, Load) pipeline using Apache Airflow to fetch daily astronomy data from NASA's Astronomy Picture of the Day (APOD) API and store it in a PostgreSQL database. The entire workflow is containerized using Docker for easy setup and reproducibility.

## Objectives

- **Extract**: Retrieve daily astronomy data from NASA's public APOD API
- **Transform**: Process and structure the API response for database storage
- **Load**: Insert transformed data into PostgreSQL for analysis and reporting
- **Orchestrate**: Manage the entire workflow using Apache Airflow's scheduling and monitoring capabilities

## Architecture
```text
╔═══════════════════════════════════════════════════════════════════╗
║                      ETL PIPELINE WORKFLOW                        ║
╚═══════════════════════════════════════════════════════════════════╝

    ╔══════════════════════════════════════════════════════════╗
    ║  1. CREATE TABLE                                         ║
    ║     └── PostgreSQL table creation if not exists          ║
    ╚══════════════════════════════════════════════════════════╝
                              ⬇
    ╔══════════════════════════════════════════════════════════╗
    ║  2. EXTRACT                                              ║
    ║     └── NASA APOD API → HttpOperator → JSON response     ║
    ╚══════════════════════════════════════════════════════════╝
                              ⬇
    ╔══════════════════════════════════════════════════════════╗
    ║  3. TRANSFORM                                            ║
    ║     └── Parse JSON → Select fields → Format for DB       ║
    ╚══════════════════════════════════════════════════════════╝
                              ⬇
    ╔══════════════════════════════════════════════════════════╗
    ║  4. LOAD                                                 ║
    ║     └── PostgresHook → INSERT into PostgreSQL table      ║
    ╚══════════════════════════════════════════════════════════╝
                              ⬇
    ╔══════════════════════════════════════════════════════════╗
    ║  5. ORCHESTRATE                                          ║
    ║     └── Apache Airflow on Astro → Daily schedule         ║
    ╚══════════════════════════════════════════════════════════╝
```

### Key Technologies
- **Apache Airflow**: Workflow orchestration and scheduling
- **PostgreSQL**: Relational database for data storage
- **Docker**: Containerization for environment consistency
- **NASA APOD API**: Public astronomy data source

## Project Structure
```bash
etl-pipeline-airflow/
├── dags/                    # Airflow DAG definitions
│   └── apod-etl.py    # Main ETL pipeline DAG
├── docker-compose.yml      # Multi-container setup
├── Dockerfile              # Airflow image customization
├── plugins/               # Custom Airflow operators/hooks
├── scripts/               # Utility scripts
└── README.md             # This file
```


## Setup Instructions

### Prerequisites
- Docker & Docker Compose
- Python 3.8+
- NASA API key (free from https://api.nasa.gov)

### Installation
1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd etl-pipeline-airflow
   ```
2. **Configure environment variables**
    Create a .env file:
    ```bash
    NASA_API_KEY=your_api_key_here
    POSTGRES_USER=airflow
    POSTGRES_PASSWORD=airflow
    POSTGRES_DB=airflow
    ```
3. **Build and start services**
    ```bash
    docker-compose up -d
    ```
4. **Access Airflow UI**
    ```bash
    Open http://localhost:8080  
    Username: admin
    Password: admin
    ```

## Pipeline Workflow
### DAG Tasks:
1. **Create Table:** Ensures PostgreSQL table exists
2. **Extract Data:** Fetches data from NASA APOD API
3. **Transform Data:** Processes and structures API response
4. **Load Data:** Inserts transformed data into PostgreSQL
5. **Data Validation:** Verifies data quality and completeness

## License
Educational project - adapt freely for learning purposes.
