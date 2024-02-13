# django-rest-api

## Stack
```
> Django REST
> JWT User Authentication
> PostgreSQL DB
> Redis for API caching
> Docker
> AWS EC2 Deployment
```


## API Calls Documentation
### Register
URL:
```
http://54.209.198.73/register/
```
POST Request:
```
{
    "username":"testUser2",
    "password":"testUserPassword2",
    "email":"testUser2@gmail.com"
}
```
Response: Status Code 201
```
{
    "password": "testUserPassword2",
    "last_login": null,
    "email": "testUser2@gmail.com",
    "username": "testUser2"
}
```

### Login
URL:
```
http://54.209.198.73/login/
```
POST Request:
```
{
    "username":"testUser2",
    "password":"testUserPassword2"
}
```
Resonse: Status Code 200
```
{
    "access_token": "eyJhbGc..."
}
```

### Write Data
URL:
```
http://54.209.198.73/data/
```
POST Request:
```
{
    "SKU": "BWAX",
    "name": "Beeswax",
    "category": "Raw Materials",
    "tags": [
        {"name": "tag1"}, 
        {"name": "tag2"}
        ],
    "stock_status": "In Stock",
    "available_stock": "400"
}
```
Response: Status Code 201
```
{
    "SKU": "BWAX",
    "name": "Beeswax",
    "category": "Raw Materials",
    "tags": [
        {
            "name": "tag1"
        },
        {
            "name": "tag2"
        }
    ],
    "stock_status": "In Stock",
    "available_stock": "400"
}
```

### Read Data
URL
```
http://54.209.198.73/data/
```
GET Request

Response:
```
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "SKU": "BWAX",
            "name": "Beeswax",
            "category": "Raw Materials",
            "tags": [
                {
                    "name": "tag1"
                },
                {
                    "name": "tag2"
                }
            ],
            "stock_status": "In Stock",
            "available_stock": "400"
        },
        {
            "SKU": "OCNCOT",
            "name": "Cotton-Ocean Print",
            "category": "Raw Materials",
            "tags": [
                {
                    "name": "tag1"
                },
                {
                    "name": "tag2"
                }
            ],
            "stock_status": "In Stock",
            "available_stock": "57"
        }
    ]
}
```


### Additional Filters
GET Requests

Paginantion:
```
http://54.209.198.73/data/?page=3
```

Filters: (category, SKU, stock_status, available_stock, name)
```
http://54.209.198.73/data/?category=Raw+Materials&SKU=&stock_status=&available_stock=&name=
```

Ordering: (name, SKU (ascending/descending))
```
http://54.209.198.73/data/?ordering=-name
http://54.209.198.73/data/?ordering=SKU
```

Search: (name, SKU)
```
http://54.209.198.73/data/?search=BWAX
http://54.209.198.73/data/?search=Ocean
```



## To run the project locally
```
$ git clone <url>
$ touch .env
```
Set up the following attributes in .env
```
DB_HOST=db
DB_NAME=dbname
DB_USER=postgres
DB_PASS=postgrespass
POSTGRES_DB=dbname
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgrespass
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@gmail.com
ADMIN_PASSWORD=adminpass
```
```
docker-compose up --build
```
