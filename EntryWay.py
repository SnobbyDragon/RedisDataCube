import redis
import sqlparse
from bottle import route, run, template

def setup():
  return redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

REDIS_INSTANCE = setup()

@route('/api/v1/redis')
def index():
  val = REDIS_INSTANCE.get("hello")
  rv = [{ "hello": val}]
  print(rv)
  return dict(data=rv)

@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)


def query_redis(instance):
  print("Input SQL query or STOP to quit")
  raw = input()
  while(raw != "STOP"):
    # case statement or something that consumes sqlparse output
    statements = sqlparse.split(raw)
    print(statements)
    print("Input SQL query or STOP to quit")
    raw = input()

  print("Quitting...")


def main():
    # test
    run(host='localhost', port=8080) 
    # query_redis(redis_instance)

if __name__ == "__main__":
    main()
