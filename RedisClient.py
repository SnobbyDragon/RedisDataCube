import redis
import sqlparse

def setup(host, port, db_num):
  return redis.Redis(host, port, db_num, decode_responses=True)

class RedisClient:
  def __init__(self, host, port, db_num):
    self.host = host
    self.port = port
    self.db_num = db_num
    self.client = setup(host, port, db_num)

  def query_redis():
    print("Input SQL query or STOP to quit")
    raw = input()
    while(raw != "STOP"):
      # case statement or something that consumes sqlparse output
      statements = sqlparse.split(raw)
      print(statements)
      print("Input SQL query or STOP to quit")
      raw = input()

    print("Quitting...")
