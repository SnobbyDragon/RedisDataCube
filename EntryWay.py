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
    for statement in statements:
      tokens = sqlparse.parse(statement)[0].tokens
      ntokens = len(tokens)

      # finds the select keyword (skipping beginning whitespace)
      selectIndex = 0
      while tokens[selectIndex].value.isspace():
        selectIndex += 1
      if tokens[selectIndex].value.upper() != 'SELECT':
          print('Only SELECT statements are supported. Skipping statement...')
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
        print('No CUBE operation found! Skipping statement...')
        continue
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
      skipStatement = False
      cubeColumnTokens.sort(key=lambda token: token.value)
      for i, col in enumerate(cubeColumnTokens):
        if col.value != identifierTokens[i].value:
          print('Columns to CUBE by are different from columns to SELECT! Skipping statement...')
          skipStatement = True
          break
      if skipStatement:
        continue

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
      print(sqlparse.format(newQuery, reindent=True, keyword_case='upper'))

    print("Input SQL query or STOP to quit")
    raw = input()

  print("Quitting...")


def main():
    redis_instance = setup()
    # test
    redis_instance.set('hello', 'redis')
    query_redis(redis_instance)

if __name__ == "__main__":
    # main()

    # testing parsing; delete later
    query_redis(None)