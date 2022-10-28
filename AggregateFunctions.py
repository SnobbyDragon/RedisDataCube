from statistics import mean, stdev

def count(c):
  # we already count ahead of time
  # TODO? maybe just get rid of this and handle COUNT(*) better
  return c

SQL_TO_FUNCTION = {
  'AVG' : mean,
  'COUNT' : count,
  'MAX' : max,
  'MIN' : min,
  'SUM' : sum,
  'STDEV' : stdev
}

def evaluate(attribute, function):
  return SQL_TO_FUNCTION[function.upper()](map(float, attribute)) # seems like aggregates are all on numerical data