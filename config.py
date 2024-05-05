

import platform
import sys 
# print(os.name)
# print(platform.system())
if platform.system() == 'Linux':

    path = r"/home/vajor/t7/albumn"
    previewpath = r"/home/vajor/t7/preview"
    
    backpath = r"/home/vajor/backup/%s"
    # print(path,backpath)
else:
    model = sys.argv[0].split('/')[-1][:-3]

    path=r"/Users/vajor/Desktop/Pictures/%s/images" % model
    backpath=r"/Users/vajor/Desktop/Pictures/%s/backup" % model




