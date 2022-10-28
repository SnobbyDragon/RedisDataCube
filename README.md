# RedisDataCube

## Installation

### Python setup
- redis `pip install redis`
- sqlparse `pip install sqlparse`
- bottle `pip install bottle`
- Run `python Router.py`

### React setup
1. cd into `redis-front`
   1. `Npm install`
2. Run `npm run build`

## Adding data to redis instance

1. Pull the `redis-data` submodule using
```
git submodule update
```
2. Navigate to the `movie-database` folder
```
cd redis-datasets/movie-database
```
3. While in the directory input the commands below to import movie data

```console
redis-cli -h localhost -p 6379 < ./import_movies.redis
redis-cli -h localhost -p 6379 < ./import_actors.redis
```
Make sure your local Redis server is running using `redis-server`

## Example Query
After adding data and starting the app via `python Router.py`, navigate to
```
   http://localhost:8080/api/v1/redis/SELECT AVG(rating), release_year, genre FROM movie GROUP BY CUBE(release_year, genre);
```
to perform the query `SELECT AVG(rating), release_year, genre FROM movie GROUP BY CUBE(release_year, genre);`.
This query finds the average rating of movies by release year and genre.