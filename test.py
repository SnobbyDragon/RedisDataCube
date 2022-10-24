import sqlparse
import operator

raw = "SELECT c1,c2,c3,sum(c4) FROM table_name GROUP BY CUBE(c1, c2, c3);"

parsed = sqlparse.parse(raw)
length = len(parsed[0].tokens)
print(length)
print(parsed[0].tokens)

print(type(parsed[0].tokens))
for token in parsed[0].tokens:
  print(type(token))
  is_part_of_accepted_classes = isinstance(token, sqlparse.sql.Function) or isinstance(token, sqlparse.sql.IdentifierList)
  if(is_part_of_accepted_classes):
    print(token.value)
