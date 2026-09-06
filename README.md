# Python bikergroups WebAPP

![GitHub repo size](https://img.shields.io/github/repo-size/dsolartec/python-bikergroups-webapp)
![GitHub License](https://img.shields.io/github/license/dsolartec/python-bikergroups-webapp)

## Requirements

- [Python >=3.14](https://www.python.org/downloads/)
- [Poetry >=2.4.1](https://python-poetry.org/docs/#installation)
- [PostgreSQL >=18](https://www.postgresql.org/download/)
- [SASS Compiler](https://sass-lang.com/install)

## Running project (Development mode)

### 1. Compile and watch changes for SCSS main file

```bash
sass app/static/scss/main.scss app/static/css/main.css --watch
```

### 2. Install dependencies using Poetry

```bash
poetry install
```

### 3. Configure local_settings.py

Clone the file `local_settings.example.py` and rename it to `local_settings.py`, then change the values of each variable according to your environment.

### 4. Run Flask application

```bash
poetry run flask run --host 0.0.0.0 --port 5000
```

> **IMPORTANT:** If you want to populate the databases tables and initial data add `LOAD_INITIAL_DATABASES_DATA=true` at the beginning of the command line.

## Running project (Production mode)

### 1. Compile SCSS main file

```bash
sass app/static/scss/main.scss app/static/css/main.css --style compressed
```

### 2. Configure environment secrets

```env
POSTGRESQL_CONNECTION_URI=
FLASK_SECRET_KEY=
```

### 3. Read the "[Deploying to production](https://flask.palletsprojects.com/en/stable/deploying/)" Flask guide
