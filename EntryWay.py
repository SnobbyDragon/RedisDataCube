import redis
import sqlparse

def setup():
  return redis.Redis(host='localhost', port=6379, db=0)

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
    redis_instance = setup()
    # test
    redis_instance.set('hello', 'redis')
    query_redis(redis_instance)

if __name__ == "__main__":
    main()
