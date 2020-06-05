# MovieFlix2020_E17144_Stylianou_Ioannis
Απαλλακτική εργασία πληροφοριακών συστημάτων

SETUP Mongo Image
-
```
  docker pull mongo
  docker run -d -p 27017:27017 --name mongodb mongo
  docker start mongodb
  docker stop mongodb
```

COPY json data files 
-
```
  docker cp "Information-Systems-Lab\lab5\flask\data\movies.json" mongodb:/movies.json
  docker exec -it mongodb mongoimport --db=InfoSys --collection=Movies --drop --file=movies.json 
  docker cp "Information-Systems-Lab\lab5\flask\data\users.json" mongodb:/users.json
  docker exec -it mongodb mongoimport --db=InfoSys --collection=Users --drop --file=users.json 
```

VIEW Data in Mongodb Shell
-
```
  docker exec -it mongodb mongo
  use InfoSys
  show collections
  db.Movies.find()
  db.Users.find()
```

Mathematical Knowledge - Sum Recalculation
-

  https://math.stackexchange.com/questions/22348/how-to-add-and-subtract-values-from-an-average
  
  adding a value in sum of n:
  s' = s + (value -s) /n+1

  removing a value from sum of n:
  s' = (ns-value)/n-1
