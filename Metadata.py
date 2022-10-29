def cat(nkeys):
  return {
    'prefix' : 'cat',
    'nkeys' : nkeys,
    'attributes' : {
      'name' : {
        'type' : 'string',
        'values' : ['Jaleah','Valentina','Karleigh','Alan','Rylee','Jaxyn','Rayne','Carlos','Layan','Shane','Maximo','Felicity','Rashad','Charis','Maddix','Oakley','Clifford','Kipton','Maelyn','Jalil','Lathan','Berkley','Josephine','Kirk','Shea','Saif','Wesley','Otto','Alisha','Audree','Elina','Devyn','Vivien','Mariano','Avah','Bowen','Damani','Henley','Myron','Montgomery','Mazie','Natalya','Katharine','Leonard','Jaidyn','Diya','Shay','Jackeline','Jamison','Arya','Ismail','Barron','Liberty','Darian','Kaison','Kyler','Reyansh','Erin','Lennox','Chael','Tariq','Kody','Yasir','Layna','Jamere','Levon','Aliza','Persephone','Etta','Layton','Arielle','Dasha','Kace','Darrell','Maksim','Nova','Raina','Kaelyn','Jaylynn','Joslyn','Tegan','Peter','Abrianna','Tejas','Devin','Jerry','Leila','Trenton','Gavyn','Lathan','Lucca','Antony','Jazmin','Marley','Maryam','Karolina','Reilly','Alexander','Jacob','Raylee']
      },
      'state' : {
        'type' : 'string',
        'values' : ['AK', 'AL', 'AR', 'AS', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA', 'GU', 'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MP', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UM', 'UT', 'VA', 'VI', 'VT', 'WA', 'WI', 'WV', 'WY']
      },
      'eye_color' : {
        'type' : 'string',
        'values' : ['red', 'blue', 'orange', 'brown', 'yellow']
      },
      'fur_color' : {
        'type' : 'string',
        'values' : ['red', 'blue', 'orange', 'brown', 'yellow', 'white', 'gray']
      },
      'height' : {
        'type' : 'decimal',
        'min' : 2.42,
        'max' : 26.08,
        'precision' : 2
      },
      'num_whiskers' : {
        'type' : 'integer',
        'min' : 0,
        'max' : 100
      }
    }
  }