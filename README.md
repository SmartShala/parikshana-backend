# parikshana-backend

backend of the next revolution, as seen on github

## TO run :

- `docker build . --tag django_web`
- `docker-compose up -d`

## ENV:

- `postgres_user` - `PostgreSQL` username
- `postgres_db` - `PostgreSQL` database name
- `postgres_password` - `PostgreSQL` password
- `pgadmin_default_email` - `PostgreSQL` admin email {For PGADMIN}
- `pgadmin_default_password` - `PostgreSQL` admin password {For PGADMIN}
- `secret_key` - `Django` SecretKey
- `minio_root_user` - `MinIO` username
- `minio_root_password` - `MinIO` password
- `minio_key` - `MinIO` access key
- `minio_secret` - `MinIO` secret key
- `minio_internal_endpoint` - `MinIO` internal endpoint
- `minio_external_endpoint` - `MinIO` external endpoint
- `base_url` - `Base URL` of the application
- `redis_host` - `Redis` host
- `redis_port` - `Redis` port
- `redis_username` - `Redis` username
- `redis_password` - `Redis` password
- `flower_username` - `Flower` username {Celery supervisor}
- `flower_password` - `Flower` password {Celery supervisor}

# Deployed on [DigitalOcean](http://146.190.10.10/)

# Proudly using [RedisLabs](http)

# Services :

- `/swagger` - `Swagger` OPENAPI Documentation
- `/api` - All API Endpoints
- `:9000` - `Min.IO` Object Storage
- `:8888` - Flower Server (Celery Viewer)
- `:9999` - `PGADMIN` Administrator
- `/silk` - `django-silky` for api profiling
