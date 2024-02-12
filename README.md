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

