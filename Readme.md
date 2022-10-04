# How to use

## Setup

### This step is not necessary when the executable has already been created.

First, create a virtual python environment, using - for example - pipenv. Here, it might be useful to make pipenv use the .lock file, since installing dependencies with the Pipfile itself may lead to errors.

```bash
pipenv install --ignore-pipfile
```

Alternatively, you may use the requirements.txt file.

```bash
pipenv install -r 'requirements.txt'
```

Then, create a .env file. It should contain the following environment variables:

1. URI
2. USERNAME
3. PASSWORD

Create an executable with

```bash
pyinstaller --onefile main.py
```

## Running the program

When running the program, you need to specify the path where your config file is located

```bash
./main -c 'path/to/config.json'
```
or

```bash
python main.py -c 'path/to/config.json'
```

## Config

The config file contains

1. The query to be executed
2. The last time the query was executed using the program
3. A default time as fallback
4. The name of the csv file to be saved.

Note that you should include "%DATETIME%" in the query if you want to filter the conversions by time and date. In case the time of the last update cannot be extracted, the program uses the default time. You can also manually control this behaviour with

```bash
-f
```

or

```bash
--force
```

## What the program does

The program uses the neo4j module to create a class Neo4jDB. While the main file does not use this functionality, the class does support writing to the database from queries. In the current implementaion, the login credentials are read from the .env file and used to establish a connection to the database. The data is then stored internally as a pandas dataframe and a csv is saved in the Data folder.
