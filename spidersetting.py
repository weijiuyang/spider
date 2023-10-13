

import platform
import sys 
# print(os.name)
# print(platform.system())
if platform.system() == 'Linux':
    model = sys.argv[0].split('/')[-1][:-3]
    # print(model)
    path = r"/home/vajor/images/%s" % model
    backpath = r"/home/vajor/backup/%s" % model
    # print(path,backpath)
else:
    model = sys.argv[0].split('/')[-1][:-3]

    path=r"/Users/vajor/Desktop/Pictures/%s/images" % model
    backpath=r"/Users/vajor/Desktop/Pictures/%s/backup" % model




