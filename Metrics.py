import redis

from Router import setup

def latency(instance):

    #no latency commands from redis are implemented in redis-py
    #use a timer from python and calculate time from query inputted to query outputted
    #could include total latency, query parsing latency, cubing latency

    return 0

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

    redis_instance = setup()
    
    check_metrics(redis_instance)

if __name__ == "__main__":
    main()
    