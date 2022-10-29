import RedisClient as rc
import time
from statistics import mean, stdev

R_HOST='localhost'
R_PORT=6379
R_DB=0

REDIS_INSTANCE = rc.RedisClient(host=R_HOST, port=R_PORT, db_num=R_DB)

def latency(instance, query, num_iterations=10):

    #no latency commands from redis are implemented in redis-py
    #use a timer from python and calculate time from query inputted to query outputted
    #could include total latency, query parsing latency, cubing latency

    latencies = [0]*num_iterations

    for i in range(num_iterations):
        start_time = time.time()
        instance.query_redis(query)
        end_time = time.time()
        latencies[i] = end_time - start_time

    return mean(latencies), min(latencies), max(latencies), stdev(latencies)

def memory(instance):
   
    #adds up all the memory usage
    #not sure if this is entirely correct because 
    #used_memory_dataset from info memory command is different and
    #dataset.bytes from memory stats is different
    #there are default values for both but even when i calculate the true impact
    #of the database on memory, it does not even out
    #they are slightly off if its any consolation, maybe extra memory is needed for other processes?

    totalMemory = 0

    for key in instance.scan_iter("movie:*"):
    # delete the key
        totalMemory += instance.memory_usage(key)
    
    print("Total memory usage of CUBE: ",totalMemory)
    
def correctness(instance):

    print("cor")

    #pseudocode for correctness
    
    #create proper cubed database and import
    #compare proper database to cubed database on redis
    #check if theyre the same by iterating over

def check_metrics(instance):

    print("""Check metrics of CUBE
    lat - latency metrics
    mem - memory metrics
    cor - correctness metrics""")
    raw = input()

    while(raw != "s"):

        if raw == "lat":
            latency(instance)
        elif raw == "mem":
            memory(instance)
        elif raw == "cor":
            correctness(instance)

        raw = input()

def main():

    # 'SELECT AVG(rating), release_year, genre FROM movie GROUP BY CUBE(release_year, genre); query for movies dataset
    # 'SELECT AVG(last_login), country, gender FROM u GROUP BY CUBE(country, gender);' query for users dataset ('users' and 'use' are keywords in SQL so not allowed)
    # 'SELECT AVG(height), STDEV(num_whiskers), eye_color, fur_color FROM cat GROUP BY CUBE(eye_color, fur_color);' query for generated cat data

    print(latency(REDIS_INSTANCE, 'SELECT AVG(height), STDEV(num_whiskers), eye_color, fur_color FROM cat GROUP BY CUBE(eye_color, fur_color);', 10))
    
    # check_metrics(redis_instance)

if __name__ == "__main__":
    main()
    