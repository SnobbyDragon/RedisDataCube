import redis

def setup():
  return redis.Redis(host='localhost', port=6379, db=0)

def main():
    redis_instance = setup()
    # test
    redis_instance.set('hello', 'redis')

if __name__ == "__main__":
    main()
