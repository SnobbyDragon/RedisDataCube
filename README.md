# RedisDataCube

## Adding data to redis instance

1. Cd into redis-datasets directory
2. Pull it?
3. While in the directory input the commands below

```console
$redis-cli -h localhost -p 6379 < ./import_movies.redis


$redis-cli -h localhost -p 6379 < ./import_actors.redis
```
