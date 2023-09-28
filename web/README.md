Adding Environment Variables
============================

```
1. We have seperate config files for each environment, and seperate file for default configuration.
2. To add an env variable, use the following syntax: 

"env|NAME_OF_VARIABLE"
```

Using alembic for DB Migrations
=============
```
cd ocr
add this in alembic.ini: script_location = migrations
alembic --config migrations/alembic.ini <cmd> (this command should be run from ocr/app path. so cd ocr/app)
commands starting with alembic should be run from cd ocr/app
commands starting with python should be run from cd ocr
```

### Some commands for reference:

#### Create new migration:
```
1. alembic --config migrations/alembic.ini revision -m "create ingestion run logs"
2. python -m app.web.migrate db upgrade head
```
#### get history of migrations:
```
1. python -m app.web.migrate db history
```

#### display current revision:
```
1. python -m app.web.migrate db current
```

#### Run migrations offline:
```
1. python -m app.web.migrate db history => to get starting and ending range
2. python -m app.web.migrate db upgrade <start range>:<end range> --sql
```

# Tests
## Unit Testing
- We are using `pytest` for unit tests and `pytest-mock` for mocks
- Refer [pytest-mock](https://changhsinlee.com/pytest-mock/) and 
  [tips and tricks for unit tests(python && pytest)](https://medium.com/worldsensing-techblog/tips-and-tricks-for-unit-tests-b35af5ba79b1) 
- define any fixture used by multiple unit tests in `app/web/tests/unit/conftest.py` file . Know more about [fixture](https://docs.pytest.org/en/stable/fixture.html)  
- For running tests:
  ```
  cd $VIRTUAL_ENV/ocr/app
  pytest
  ```

## Integration Test
- For running the integration tests, execute the below commands from command line
  ```
  $  export TEST_LEVEL=integration
  $  pytest
  ```
