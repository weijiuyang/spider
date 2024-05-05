
import redis
import json

red10 = redis.Redis(host='localhost', port=6379, db=10)
red11 = redis.Redis(host='localhost', port=6379, db=11)
red12 = redis.Redis(host='localhost', port=6379, db=12)
red13 = redis.Redis(host='localhost', port=6379, db=13)
red14 = redis.Redis(host='localhost', port=6379, db=14)
red15 = redis.Redis(host='localhost', port=6379, db=15)


title = f'XiuRen第8362期_模特安然anran白色紧身开胸上衣配开档黑丝秀柔美身段诱惑写真79P'
# title = f'XiuRen第8363期_女神杨晨晨Yome白色连衣长裙+白色情趣薄纱秀丰腴身材诱惑写真82P'
title = f'[YouMi尤蜜荟]Vol_1048_模特赵可欣baby性感超短JK制服配白色丝袜秀曼妙身姿完美写真51P'

redislist = [red10, red11, red12, red13, red14, red15]

for _ in redislist:
    item = _.get(title)
    if isinstance(item, bytes):  # 确认是二进制数据
        try:
            print(item.decode('utf-8'))  # 解码并打印
        except UnicodeDecodeError:
            print("解码错误")
    else:
        print(item)  # 如果不是二进制数据，直接打印



