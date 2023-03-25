# RestAPI-Hospital

Steps to setup the project:
1. Install poetry package (version 1.4.1)
2. Install requirements: `poetry install`
3. Activate environment: `poetry shell`
4. The migration file already exists, use `alembic upgrade heads` to apply the migration (it may be applied already)
    After running the comand, you should see one of this messages:
    
    a)
    ```
    INFO [alembic.runtime.migration] Context impl PostgresqlImpl.
    INFO  [alembic.runtime.migration] Will assume transactional DDL.
    INFO  [alembic.runtime.migration] Running upgrade  -> 8cdb4f9a9715, empty message
    ```
    b)
    ```
    INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
    INFO  [alembic.runtime.migration] Will assume transactional DDL.
    ```
5. Run the server: `poetry run uvicorn api.endpoints:app --reload`
6. Access the server: http://localhost:8000/docs


Endpoints documentation
1. Authenticate with general access:

Username: `user`

Password: `pass`
![image](https://user-images.githubusercontent.com/128868275/227668576-6173ad2f-f3f3-4f2b-87e0-5e5e958fb339.png)

2. Create new doctors, patients, assistants and treatments entities:
![image](https://user-images.githubusercontent.com/128868275/227669063-6ce62fdd-a392-4ee5-b263-26aef33670ca.png)

![image](https://user-images.githubusercontent.com/128868275/227669581-3cb0deb8-8601-427c-a64e-7c96e62e4333.png)


3. In order to assign a treatment (and use the DELETE and PATCH treatment) you need to assign a pacient to a doctor first.


![image](https://user-images.githubusercontent.com/128868275/227674858-4472a137-ef14-46ae-98dd-6038f7f95af6.png)


Additional info

To create new migrations:
1. `alembic downgrade base`
2. Go to /migrations/versions and delete the migration file
3. `alembic revision --autogenerate`
4. `alembic upgrade heads`


To see the database you can use the management tool for PostgreSQL:

download link: https://www.enterprisedb.com/downloads/postgres-postgresql-downloads

setup: https://www.postgresqltutorial.com/postgresql-getting-started/install-postgresql/
