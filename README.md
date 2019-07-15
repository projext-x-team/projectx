# Python Packages
```
$ pip3 freeze 
$ pip3 install -r requirements.txt
```

# DB creation
```
$ python3
>>> from SwimmerModel import *
>>> db.create_all()
>>> exit()
$ cat db
```

# Test DB Models
```
$ python3
>>> from SwimmerModel import *
>>> Swimmer.add_swimmer(1, "s1","c1",10)
>>> Swimmer.get_all_swimmers()
Swimmer.add_swimmer("s2","c2",10)
```

# Run applications
```
$ python3 app.py
```
