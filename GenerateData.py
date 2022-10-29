import redis
import random
import Metadata as md

R_HOST='localhost'
R_PORT=6379
R_DB=0

redis = redis.Redis(R_HOST, R_PORT, R_DB, decode_responses=True)

def generate_data(prefix, nkeys, attributes):
  '''
    Inserts nkeys number of hashes to the Redis database.
    Each hash's key begins with prefix.
    Each hash will have attributes (dictionary mapping string --> dictionary). The keys will be the attribute name.

    attributes[key] = {
      'type' : 'string' | 'integer' | 'decimal',
      ...
    }

    If the attribute is a string,
    attributes[key] = {
      'type' : 'string',
      'values' : ['value1', 'value2', ...] (guaranteed each value appears at least once, so num unique values must be <= nkeys)
    }

    If the attribute is an integer,
    attributes[key] = {
      'type' : 'integer',
      'min' : minimum value allowed,
      'max' : maximum value allowed
    }

    If the attribute is a decimal,
    attributes[key] = {
      'type' : 'decimal',
      'min' : minimum value allowed,
      'max' : maximum value allowed,
      'precision' : number of decimal places
    }
  '''

  for i in range(nkeys):
    redis.hset(''.join([prefix, ':', str(i)]), mapping={
      attribute : generate_attribute_value(attributes[attribute], i)
      for attribute in attributes
    })

def generate_attribute_value(metadata, index):
  if metadata['type'] == 'string':
    l = len(metadata['values'])
    if index < l:
      return metadata['values'][index] # guarantee at least one key of each value
    return metadata['values'][random.randint(0, l-1)] # if guaranteed, pick a random value
  elif metadata['type'] == 'integer':
    return random.randint(metadata['min'], metadata['max'])
  elif metadata['type'] == 'decimal':
    return round(random.uniform(metadata['min'], metadata['max']), metadata['precision'])
  else:
    print('invalid attribute type: ', metadata['type'], ' Exiting...')
    exit()

def main():
  # TODO: currently can only add to an empty database bc we don't check for redundant keys
  # print('Clear database first? y/n (yes/no)')
  # a = input()
  # if a == 'y':
  #   print('Clearing database...')
  #   redis.flushdb()
  # elif a == 'n':
  #   print('Will not clear database.')
  # else:
  #   print('y/n only. Exiting...')
  #   exit()

  redis.flushdb() # clears the database before generating data

  print('Generating data...')
  data = md.cat(500_000) # parameter is number of keys in database.
  generate_data(data['prefix'], data['nkeys'], data['attributes'])
  print('Done!')
  
if __name__ == "__main__":
    main()