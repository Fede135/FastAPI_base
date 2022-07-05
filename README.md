# Documentation

## How to run the project?

In the root directory run:

`docker build -t fastapi .`

`docker run -p 80:80 fastapi`

## How to use the API?

Then go to `127.0.0.1:80/docs` to see documentation for the project. There you can try the 2 endpoints so far.

### Import League

POST `127.0.0.1:80/league/{league_code}/import`


IMPORTANT: In some cases the Football API response for information about squad retrieve empty values.

### Players

GET `127.0.0.1:80/league/{league_code}/players?team_name=<name/shortname>`


Also this endpoint is paginated. You can use page and size as query parameters, e,i:

GET `127.0.0.1:80/league/{league_code}/players?page=2`


## How to run the tests?

In the root directory run create a virtualenv running `python3 -m venv venv`. Then install the dependencies running
 `pip install -r requirements.txt`

Then run the tests with pytest, only running `pytest`

Be sure that your virtualenv is activated, if not run `source venv/bin/activate`

# Decisions and improvements

## Technology used
I decided to use `FastAPI`, because as the name said (joke), is any easy and fast way to build APIs with Python. Is easy 
also to build the schemas and to perform validations. The decision of use `mysqlalchemy` is because is a well know 
ORM in the industry and also have a great compatibility with `FastAPI` schemas and pagination.


## Singleton and Proxy

I decided to apply the Proxy pattern to allow control the access to the external API. But doing this I
realize that only I will need a unique instance of the Proxy, so I apply also the Singleton pattern only
to have a unique instance of the Proxy. With this a "wrap" and control the use of the `Proxy.get` method


## Improvements that could not be made due to lack of time

I wanted to have the SQLite database in a separate container and connect both containers using docker_compose.

Also I could not finish the 2 remaining endpoints.

Separate the main using `APIRoute`. With this I could have more granularity in the handle of the paths per domain,
and not to have all the endpoints logic in the same `main.py` file. This should apply also to the test files.

In case that was need it we can use a cache to scale the our API to support more traffic.
