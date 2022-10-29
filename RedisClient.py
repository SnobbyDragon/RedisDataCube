import redis
import sqlparse
import AggregateFunctions as af
from itertools import zip_longest

def setup(host, port, db_num):
  return redis.Redis(host, port, db_num, decode_responses=True)

class RedisClient:
  def __init__(self, host, port, db_num):
    self.host = host
    self.port = port
    self.db_num = db_num
    self.client = setup(host, port, db_num)

  def query_redis(self, raw):
    statements = sqlparse.split(raw)
    statement = statements[0] # just one statement at a time
    try:
      cube_params = self.extract_cube_params(statement)
    except ValueError as exception:
      print(exception)

    return self.cube(*cube_params)
    # return self.cube_to_string(self.cube(*cube_params))

    # translated = self.translate_statement(statements[0])
    # return sqlparse.format(translated, reindent=True, keyword_case='upper')

  def cube_to_string(self, cubeDict):
    '''
      Converts data cube dictionary of dictionaries to string format.
      Given the cube function example, yields the following string:

      color | breed   | AVG(weight)
      white | persian | 7
      black | bombay  | 7
      black | manx    | 7
      all   | persian | 7
      all   | manx    | 7
      white | all     | 6
      black | all     | 7
      all   | all     | 7
    '''

    iterCubeKeys = iter(cubeDict.keys())
    key = next(iterCubeKeys)
    cubeText = [None]*(len(cubeDict)+1)
    cubeText[0] = list(map(str, cubeDict[key].keys())) # column names
    cubeText[1] = list(map(str, cubeDict[key].values())) # first row

    # get max string per column to format later
    colWidths = [len(text) for text in cubeText[0]]
    for j, text in enumerate(cubeText[1]):
      colWidths[j] = max(colWidths[j], len(text))
    
    i = 2
    for key in iterCubeKeys:
      cubeText[i] = list(map(str, cubeDict[key].values()))
      for j, text in enumerate(cubeText[i]):
        colWidths[j] = max(colWidths[j], len(text))
      i += 1

    def formatRows(row):
      # row is a list of strings

      # pads each value in row with trailing whitespace until each value is of corresponding colWidth
      newRow = [row[i] + ' '*(width-len(row[i])) for i, width in enumerate(colWidths)]

      return ' | '.join(newRow)

    return '\n'.join(map(formatRows, cubeText))

  def cube(self, prefix, aggAttrs, aggFuncs, groupByAttrs):
    '''
      prefix = string denoting which "table" we are selecting from (prefix of Redis keys)
      aggAttrs = list of attributes we want to aggregate on and select (can contain duplicates if we perform multiple aggregations on one attribute)
      aggFuncs = list of aggregate functions corresponding to the attributes we want to aggregate on and select
      groupByAttrs = list of attributes we want to group by

      Returns data cube represented by a dictionary of dictionaries:
      {row = bitmask + id : {cols = groupByAttrs, aggFuncs(aggAttrs): value}}
      i.e. Given the following cat data:
      name      | color | breed   | weight
      mittens   | white | persian | 5
      inky      | black | bombay  | 7
      bob       | white | persian | 9
      mochi     | black | manx    | 7
      
      "SELECT color, breed, AVG(weight) FROM cat CUBE(color, breed);" yields the following dictionary:
      {
        'white-persian' : {
          'color' : 'white', 'breed' : 'persian', 'AVG(weight)' : 7
        },
        'black-bombay' : {
          'color' : 'black', 'breed' : 'bombay', 'AVG(weight)' : 7
        },
        'black-manx' : {
          'color' : 'black', 'breed' : 'manx', 'AVG(weight)' : 7
        },
        'white-all' : {
          'color' : 'white', 'breed' : 'all', 'AVG(weight)' : 6
        },
        'black-all' : {
          'color' : 'black', 'breed' : 'all', 'AVG(weight)' : 7
        },
        'all-persian' : {
          'color' : 'all', 'breed' : 'persian', 'AVG(weight)' : 7
        },
        'all-bombay' : {
          'color' : 'all', 'breed' : 'bombay', 'AVG(weight)' : 7
        },
        'all-manx' : {
          'color' : 'all', 'breed' : 'manx', 'AVG(weight)' : 7
        },
        'all-all' : {
          'color' : 'all', 'breed' : 'all', 'AVG(weight)' : 7
        }
      }

      Note that each row (key of first dictionary) contains n values separated by -
      that correspond to GROUP BY columns (the first n keys of the inner dictionaries).
    '''

    dataCube = {}

    # first get all rows (hashes) with keys starting with prefix
    client = self.client
    rows = self.get_rows(client, prefix) # TODO: consider finding all key prefixes and creating a map of {prefix: [list of keys]} upon startup

    # for each bitmask combination, perform group by and union to dataCube
    nBits = len(groupByAttrs)
    bitmask = (1 << nBits) - 1 # if bit = 0, then do not GROUP BY this attribute (this attribute is 'ALL'); starts with all 1
    while bitmask >= 0:
      groupBy = self.group_by(rows, aggAttrs, aggFuncs, groupByAttrs, format(bitmask, ''.join(['0', str(nBits), 'b'])))
      dataCube.update(groupBy)
      bitmask -= 1

    # print(dataCube)
    return dataCube

  def get_rows(self, client, prefix):
    '''
      Uses SCAN rather than KEYS for performance (if number of keys is large, KEYS is slow).
      Returns a list of rows (hashes) with keys starting with prefix.
      The rows are represented as dictionaries.
    '''
    rows = []

    def batch(scanIterable, batchSize):
      keys = [iter(scanIterable)]*batchSize
      return zip_longest(*keys)

    for keyBatch in batch(client.scan_iter(''.join([prefix, '*'])), 500):
      rows.extend(list(map(client.hgetall, filter(None, keyBatch)))) # TODO: maybe filter is inefficient (needed to get rid of None keys)

    return rows

  def group_by(self, rows, aggAttrs, aggFuncs, groupByAttrs, bitmask):
    '''
      Perform GROUP BY on the rows given bitmask combination.
      Returns a dictionary of dictionaries.

      Given the cube function example, if bitmask = 11, we get the following dictionary:
      {
        'white-persian' : {
          'color' : 'white', 'breed' : 'persian', 'AVG(weight)' : 7
        },
        'black-bombay' : {
          'color' : 'black', 'breed' : 'bombay', 'AVG(weight)' : 7
        },
        'black-manx' : {
          'color' : 'black', 'breed' : 'manx', 'AVG(weight)' : 7
        }
      }

      or if bitmask = 00, we get this dictionary:
      {
        'all-all' : {
          'color' : 'all', 'breed' : 'all', 'AVG(weight)' : 7
        }
      }
    '''

    result = {}
    buckets = {}

    # get attributes we will actually group by (not 'ALL'); 'ALL' denotes an 'ALL' attribute
    actualGroupByAttrs = ['ALL']*len(groupByAttrs)
    for i, attr in enumerate(groupByAttrs):
      if bitmask[i] == '1': # bit = 1 means we want to GROUP BY this attribute
        actualGroupByAttrs[i] = attr

    # put aggAttrs into buckets with unique groupByAttrs combinations that satisfy the bitmask
    for r in rows:
      bucket = '-'.join([r.get(actualGroupByAttrs[i], 'all') for i, attr in enumerate(groupByAttrs)]) # only uses groupByAttrs to make sure iteration order is same as later
      if bucket in buckets:
        # add aggAttrs of this tuple into bucket
        for attr in aggAttrs:
          if attr == '*': # * is only used for COUNT
            buckets[bucket][attr] += 1
          else:
            buckets[bucket][attr].append(r[attr])
      else:
        buckets[bucket] = {attr : 1 if attr == '*' else [r[attr]] for attr in aggAttrs}
    
    # perform aggFuncs[i] on aggAttrs[i] for each bucket
    for bucket in buckets:
      bucketVals = bucket.split('-')
      result[bucket] = {attr : bucketVals[i] for i, attr in enumerate(groupByAttrs)}
      result[bucket].update({''.join([func.upper(), '(', aggAttrs[i], ')']) : af.evaluate(buckets[bucket][aggAttrs[i]], func) for i, func in enumerate(aggFuncs)})

    return result

  def extract_cube_params(self, statement):
    '''
      From the SQL statement, extract which "table" we are selecting from, attributes we are cubing by
      and which attributes we are selecting and the aggregate functions to perform on them.

      The "table" will correspond to prefixes of the hashes in the Redis instance.
      We assume the Redis instance has hashes similar to tuples in a relation.

      Returns a tuple (prefix, aggAttrs, aggFuncs, groupByAttrs) for the cube function.

      Raises a value error if SQL statement is invalid. A statement is invalid if:
      - not a SELECT statement
      - contains no CUBE operation
      - FROM more than one table (currently only supports selecting from one table at a time)
      - CUBE attributes must also be SELECTed
          i.e. SELECT AVG(age) FROM customers GROUP BY CUBE(zipcode); is not allowed because we must SELECT zipcode
    '''

    tokens = sqlparse.parse(statement)[0].tokens
    ntokens = len(tokens)

    # finds the select keyword (skipping beginning whitespace)
    selectIndex = 0
    while tokens[selectIndex].value.isspace(): # skip whitespace
      selectIndex += 1
      if tokens[selectIndex].value.upper() != 'SELECT':
        raise ValueError('Only SELECT statements are supported.')
    selectToken = tokens[selectIndex]

    # finds a list of what we are selecting
    selectedColumnIndex = selectIndex + 1
    while tokens[selectedColumnIndex].value.isspace(): # skip whitespace
      selectedColumnIndex += 1
    selectedColumnTokens = tokens[selectedColumnIndex]
    if isinstance(selectedColumnTokens, sqlparse.sql.IdentifierList):
      selectedColumnTokens = [*selectedColumnTokens.get_identifiers()]
    else:
      selectedColumnTokens = [selectedColumnTokens]

    # finds what "table" we are selecting FROM
    fromTableIndex = selectedColumnIndex + 1
    while tokens[fromTableIndex].value.isspace(): # skip whitespace
      fromTableIndex += 1
    if tokens[fromTableIndex].value.upper() != 'FROM':
      raise ValueError('Expected FROM token after SELECT attributes.')
    fromTableIndex += 1 # skip FROM token
    while tokens[fromTableIndex].value.isspace(): # skip whitespace
      fromTableIndex += 1
    fromTableToken = tokens[fromTableIndex]
    if not isinstance(fromTableToken, sqlparse.sql.Identifier):
      raise ValueError('Expected relation name after FROM token. Got ', fromTableToken)

    # skips tokens between FROM table and CUBE
    startIndex = fromTableIndex + 1
    cubeIndex = startIndex
    while cubeIndex < ntokens and 'CUBE' not in tokens[cubeIndex].value.upper():
      cubeIndex += 1
    if cubeIndex >= ntokens:
      raise ValueError('No CUBE operation found!')
    cubeToken = tokens[cubeIndex]

    # finds a list of what we CUBE by
    cubeColumnTokens = [*cubeToken.get_parameters()]

    # sort selectedColumns in lexicographic order
    # put aggregate functionTokens at the end
    functionTokens = []
    identifierTokens = []
    for selectedColumnToken in selectedColumnTokens:
      if isinstance(selectedColumnToken, sqlparse.sql.Function):
        functionTokens.append(selectedColumnToken)
      else:
        identifierTokens.append(selectedColumnToken)
    identifierTokens.sort(key=lambda token: token.value)

    # verify cubeColumnTokens is the same as identifierTokens
    cubeColumnTokens.sort(key=lambda token: token.value)
    for i, col in enumerate(cubeColumnTokens):
      if col.value != identifierTokens[i].value:
        raise ValueError('Columns to CUBE by are different from columns to SELECT!')

    def getAggAttrs(functionToken):
      # gets aggregate function names from function tokens
      params = functionToken.get_parameters()
      if not params: # for some reason, * doesn't count as a parameter in sqlparse, so we make special case
        return '*'
      return params[0].value

    prefix = fromTableToken.value # prefix is just name of table
    aggAttrs = list(map(getAggAttrs, functionTokens)) # attributes inside aggregate functions after SELECT
    aggFuncs = list(map(lambda function: function.get_real_name(), functionTokens)) # aggregate functions after SELECT
    groupByAttrs = list(map(lambda token: token.value, cubeColumnTokens)) # names of attributes inside CUBE
    return (prefix, aggAttrs, aggFuncs, groupByAttrs)


  ##############################################################
  # ----------------------- DEPRECATED ----------------------- #
  ##############################################################
  def translate_statement(self, statement):
    '''
      Translates SQL CUBE statement to UNION and GROUP BY.
      ** No longer used, but similar logic in extract_attributes **
    '''
    tokens = sqlparse.parse(statement)[0].tokens
    ntokens = len(tokens)

    # finds the select keyword (skipping beginning whitespace)
    selectIndex = 0
    while tokens[selectIndex].value.isspace():
      selectIndex += 1
      if tokens[selectIndex].value.upper() != 'SELECT':
        return 'Only SELECT statements are supported. Skipping statement...'
        continue
    selectToken = tokens[selectIndex]

    # TODO: might have TOP before list of columns

    # finds a list of what we are selecting
    selectedColumnIndex = selectIndex + 1
    while tokens[selectedColumnIndex].value.isspace():
      selectedColumnIndex += 1
    selectedColumnTokens = tokens[selectedColumnIndex]
    if isinstance(selectedColumnTokens, sqlparse.sql.IdentifierList):
      selectedColumnTokens = [*selectedColumnTokens.get_identifiers()]
    else:
      selectedColumnTokens = [selectedColumnTokens]

    # finds tokens between selected columns and CUBE
    startIndex = selectedColumnIndex + 1
    cubeIndex = startIndex
    while cubeIndex < ntokens and 'CUBE' not in tokens[cubeIndex].value.upper():
      cubeIndex += 1
    if cubeIndex >= ntokens:
      return 'No CUBE operation found! Skipping statement...'
    middleTokens = tokens[startIndex:cubeIndex]
    cubeToken = tokens[cubeIndex]

    # finds a list of what we CUBE by
    cubeColumnTokens = [*cubeToken.get_parameters()]
    
    # sort selectedColumns in lexicographic order
    # put aggregate functionTokens at the end
    functionTokens = []
    identifierTokens = []
    for selectedColumnToken in selectedColumnTokens:
      if isinstance(selectedColumnToken, sqlparse.sql.Function):
        functionTokens.append(selectedColumnToken)
      else:
        identifierTokens.append(selectedColumnToken)
    identifierTokens.sort(key=lambda token: token.value)

    # TODO: add all group by columns into select if not already included?
    # verify cubeColumnTokens is the same as identifierTokens
    cubeColumnTokens.sort(key=lambda token: token.value)
    for i, col in enumerate(cubeColumnTokens):
      if col.value != identifierTokens[i].value:
        return 'Columns to CUBE by are different from columns to SELECT! Skipping statement...'

    # get combinations to find sub/grand totals
    nBits = len(identifierTokens)
    identifierTokensCombinations = [identifierTokens]
    bitmask = (1 << nBits) - 2
    allLiteral = sqlparse.sql.Token(sqlparse.tokens.String, 'All') 
    while bitmask > 0:
      identifierTokensCombination = [allLiteral]*nBits
      for i, bit in enumerate(list(format(bitmask, ''.join(['0', str(nBits), 'b'])))):
        if bit == '0':
          identifierTokensCombination[i] = identifierTokens[i]
      identifierTokensCombinations.append(identifierTokensCombination)
      bitmask -= 1
    identifierTokensCombinations.append([allLiteral]*nBits)

    # gets tokens after CUBE
    endIndex = cubeIndex + 1
    endTokens = tokens[endIndex:-1] # :-1 to exclude semicolon; TODO: deal with trailing whitespace

    # TODO: connect new SQL query to redis instead of print
    def makeIdentifierListToken(tokenList):
      # adds comma tokens inbetween each identifier token
      # returns an IdentifierList
      newTokenList = [tokenList[0]]
      for token in tokenList[1:]:
        newTokenList.append(sqlparse.sql.Token(sqlparse.tokens.Punctuation, ','))
        newTokenList.append(sqlparse.sql.Token(sqlparse.tokens.Whitespace, ' '))
        newTokenList.append(token)
      return sqlparse.sql.IdentifierList(newTokenList)

    def makeNewCubeToken(identifierTokensCombination):
      # gets rid of cube parameters corresponding to 'ALL'
      newTokenList = [sqlparse.sql.Identifier([sqlparse.sql.Token(sqlparse.tokens.Name, 'CUBE')])]
      parenthesisTokensList = [sqlparse.sql.Token(sqlparse.tokens.Punctuation, '(')]
      for identifierToken in identifierTokensCombination:
        if identifierToken.value.upper() == 'ALL':
          continue
        parenthesisTokensList.append(identifierToken)
        parenthesisTokensList.append(sqlparse.sql.Token(sqlparse.tokens.Punctuation, ','))
        parenthesisTokensList.append(sqlparse.sql.Token(sqlparse.tokens.Whitespace, ' '))
      parenthesisTokensList = parenthesisTokensList[:-2]
      parenthesisTokensList.append(sqlparse.sql.Token(sqlparse.tokens.Punctuation, ')'))
      parenthesisToken = sqlparse.sql.Parenthesis(parenthesisTokensList)
      newTokenList.append(parenthesisToken)
      return sqlparse.sql.Function(newTokenList)

    newTokens = [
      selectToken,
      makeIdentifierListToken(identifierTokensCombinations[0] + functionTokens),
      *middleTokens,
      cubeToken,
      *endTokens
    ]
    for identifierTokensCombination in identifierTokensCombinations[1:-1]:
      newTokens.append(sqlparse.sql.Token(sqlparse.tokens.Keyword, 'UNION'))
      newCubeToken = makeNewCubeToken(identifierTokensCombination)
      currTokens = [
        selectToken,
        makeIdentifierListToken(identifierTokensCombination + functionTokens),
        *middleTokens,
        newCubeToken,
        *endTokens
      ]
      newTokens.extend(currTokens)
    
    # if all 'ALL', then no CUBE needed
    newTokens.append(sqlparse.sql.Token(sqlparse.tokens.Keyword, 'UNION'))
    newTokens.extend([
        selectToken,
        makeIdentifierListToken(identifierTokensCombinations[-1] + functionTokens),
        *(middleTokens[:-3]), # delete GROUP BY
        # TODO: ^ only works if 'GROUP BY' is the exact end of list (trailing white space is a problem)
        sqlparse.sql.Token(sqlparse.tokens.Punctuation, ';')
    ])

    newQuery = ' '.join(list(map(lambda token: token.value, newTokens)))
    return newQuery
