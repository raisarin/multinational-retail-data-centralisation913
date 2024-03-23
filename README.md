# Multinational Retail Data Centralisation 
Extracting and cleaning data from online resources such as AWS buckets, online link and local database. Creating database schema to relation between different tables within the database ensuring robustness and integrity of the data. Querying the data using SQL to organise and present the dataset in order to be easily understood by the users.

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
    ├─query/
    │　├─task1.sql
    │　├─task2.sql
    │　├─task3.sql
    │　├─task4.sql
    │　├─task5.sql
    │　├─task6.sql
    │　├─task7.sql
    │　├─task8.sql
    │　└─task9.sql
    ├─utility/
    │　├─data_cleaning.py
    │　├─data_extraction.py
    │　└─database_utils.py 
    ├─.gitignore
    ├─main.py
    ├─mrdc_env.yaml
    └─README.md

* database_schema: Configure and connect the star-based schema of the database in milestone 3.

* query: SQL query results to show the results needed for milestone 4.

* utility: Extracting and cleaning data from data sources for milestone 2.

* main.py: Initialise the project. 

* mrdc_env.yaml: Miniconda environment setup configurations.

## License information
The MIT License (MIT)

Copyright (c) .NET Foundation and Contributors

All rights reserved.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.