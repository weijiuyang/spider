print("ttt")

import shutil
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




def remove(remove_website):
    for name  in infos:
        red10 = redis_connections['red10'].get(name).decode('utf-8') if redis_connections['red10'].get(name) else None
        website = redis_connections['red11'].get(name).decode('utf-8') if redis_connections['red11'].get(name) else None

        column = redis_connections['red12'].get(name).decode('utf-8') if redis_connections['red12'].get(name) else None
        girl = redis_connections['red13'].get(name).decode('utf-8') if redis_connections['red13'].get(name) else None
        keywords = redis_connections['red14'].get(name).decode('utf-8') if redis_connections['red14'].get(name) else None
        description = redis_connections['red15'].get(name).decode('utf-8') if redis_connections['red15'].get(name) else None
        print(red10)
        print(website)
        
        print(column)

        print(girl)
        print(keywords)
        print(description)

        if website == remove_website:
            print(name)
            shutil.rmtree(os.path.join(path, name))
            # exit()

        # exit()