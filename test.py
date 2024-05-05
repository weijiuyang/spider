print("ttt")


import redis
redis_connections = {
    'red9': redis.Redis(host='localhost', port=6379, db=9),

    'red10': redis.Redis(host='localhost', port=6379, db=10),
    'red11': redis.Redis(host='localhost', port=6379, db=11),
    'red12': redis.Redis(host='localhost', port=6379, db=12),
    'red13': redis.Redis(host='localhost', port=6379, db=13),
    'red14': redis.Redis(host='localhost', port=6379, db=14),
    'red15': redis.Redis(host='localhost', port=6379, db=15)
}
import os 
from config import *

infos = os.listdir(path)
print(len(infos))

origin = 'XiuRen第8428期_模特鱼子酱Fish浴池场景性感粉色布兜内衣秀惹火身材诱惑写真81P'
column = redis_connections['red12'].get(origin).decode('utf-8') if redis_connections['red12'].get(origin) else None
name = redis_connections['red13'].get(origin).decode('utf-8') if redis_connections['red13'].get(origin) else None
keywords = redis_connections['red14'].get(origin).decode('utf-8') if redis_connections['red14'].get(origin) else None
description = redis_connections['red15'].get(origin).decode('utf-8') if redis_connections['red15'].get(origin) else None
print(column)
print(name)
print(keywords)
print(description)



red12 = redis.Redis(host='localhost', port=6379, db=12) #column
red13 = redis.Redis(host='localhost', port=6379, db=13) #mnname
red14 = redis.Redis(host='localhost', port=6379, db=14) #keywords
red15 = redis.Redis(host='localhost', port=6379, db=15) #description
title = name
print(title)

print(red12.get(title))
print(red13.get(title))
print(red14.get(title))
print(red15.get(title))

exit()
# redis_connections['red9'].getkeys()
for name  in infos:

    column = redis_connections['red12'].get(name).decode('utf-8') if redis_connections['red12'].get(name) else None
    name = redis_connections['red13'].get(name).decode('utf-8') if redis_connections['red13'].get(name) else None
    keywords = redis_connections['red14'].get(name).decode('utf-8') if redis_connections['red14'].get(name) else None
    description = redis_connections['red15'].get(name).decode('utf-8') if redis_connections['red15'].get(name) else None
    print(column)
    print(name)
    print(keywords)
    print(description)
    # exit()