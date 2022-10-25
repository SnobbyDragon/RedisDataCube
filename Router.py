import RedisClient as rc
from bottle import route, run, template, post, get

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
    print(query)
    return "success"

@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

def main():
    run(host='localhost', port=8080) 

if __name__ == "__main__":
    main()
