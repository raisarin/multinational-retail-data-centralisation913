# Multinational Retail Data Centralisation 
Extracting and cleaning data from the data source 

Creating database schema 

Querying the data 

## Table of Contents 
1. [Installation instructions](#installation-instructions)
2. [Usage instructions](#usage-instructions)
3. [File structure](#file-structure)
4. [License information](#license-information)


## Installation instructions 
There are a few applications that are required for the project. 

1. PostgreSQL and pgAdmin
* [PostgreSQL](https://www.postgresql.org/download/ "https://www.postgresql.org/download/") and 
[pgAdmin](https://www.pgadmin.org/download/ "https://www.pgadmin.org/download/") will be used to manipulate the dataset stored locally or from online. 

2. AWS Command Line Interface
* [AWD CLI](https://aws.amazon.com/cli/ "https://aws.amazon.com/cli/") is used to communicate with the Amazon services.

3. Miniconda 
* [Miniconda](https://docs.conda.io/projects/miniconda/en/latest/ "https://docs.conda.io/projects/miniconda/en/latest/") helps set up virtual environments to install necessary packages to run the project. 
## Usage instructions
1. Clone the repository
```
git clone https://github.com/raisarin/multinational-retail-data-centralisation913.git
```
2. Create a new conda environment for the project with configuration
```
conda env create -n mrdc --file mrdc_env.yaml 
```
3. Run main.py to start the project 
```
python main.py 
```
## File structure
    .
    ├─database_schema/
    │　├─dim_card_details.sql
    │　├─dim_date_times.sql
    │　├─dim_products.sql
    │　├─dim_store_details.sql
    │　├─dim_users.sql
    │　├─foreign_key.sql
    │　├─orders_table.sql
    │　└─primary_key.sql
    ├─.gitignore
    ├─data_cleaning.py
    ├─data_extraction.py
    ├─database_utils.py
    ├─main.py
    ├─mrdc_env.yaml
    └─README.md

## License information
