import RedisClient as rc
from bottle import route, run, template, post, get
import re

R_HOST='localhost'
R_PORT=6379
R_DB=0

REDIS_INSTANCE = rc.RedisClient(host=R_HOST, port=R_PORT, db_num=R_DB)

@route('/api/v1/redis')
def index():
  val = REDIS_INSTANCE.client.get("hello")
  rv = [{ "hello": val}]
  print(rv)
  return dict(data=rv)

@get('/api/v1/redis/<query>')
def do_query(query):
    cubeText = REDIS_INSTANCE.query_redis(query)
    return template('<pre>{{text}}</pre>', text=cubeText)

@get('/api/v1/redis/keys')
def index():
    keys = []
    for key in REDIS_INSTANCE.client.keys():
        possible_key = re.sub(":\d+", "", key)
        if possible_key not in keys:
            keys.append(possible_key)
    return dict(data=keys)

@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

def main():
    run(host='localhost', port=8080) 

if __name__ == "__main__":
    main()
