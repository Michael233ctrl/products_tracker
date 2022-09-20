## DRF Products tracker 

---

#### Prepare env file:

```
POSTGRES_USER=<db_user>
POSTGRES_PASSWORD=<db_password>
POSTGRES_HOST=<db_host>
POSTGRES_PORT=<db_port>
POSTGRES_DB=<db>
SECRET_KEY=<secret_key>
```

#### Build project:
```shell
make build
```

#### Run migrations:
```shell
make migrate
```

#### Create superuser:
```shell
make user
```

#### Run project:
```shell
make up
```

#### Run tests:
```shell
make tests
```

#### API endpoints:
```
http://localhost:8000/api/categories/
http://localhost:8000/api/products/
http://localhost:8000/api/prices/
http://localhost:8000/swagger/
http://localhost:8000/redoc/
```
