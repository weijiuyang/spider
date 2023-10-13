import os
import py7zr 
import re

# import patoolib

password = "cosor.top"

pd = r'cosor.top'
path = '/home/vajor/zip/'
print(os.listdir(path))
for one in sorted(os.listdir(path)):
    if one[0] != '.' and one[-2:] == '7z' :
        print(path +one )
        # patoolib.extract_archive(path +one, outdir="your_directory", password=pd)
        # exit()
        with py7zr.SevenZipFile(path + one, mode='r', password=pd) as z: 
            print(path + one)
            z.extractall(path)
            os.remove(path + one)
for one in os.listdir(path):
    if one[0] != '.' :
        with py7zr.SevenZipFile(path + one, mode='r', password=pd) as z: 
            os.rename(path+one, path+one+'.7z')

for one in os.listdir(path):
    if one[0] != '.' :
        with py7zr.SevenZipFile(path + one, mode='r', password=pd) as z: 
            z.extractall(path)
            os.remove(path + one)

for one in  os.listdir(path):
    if one[0] != '.' :
        namelist = []
        for two in os.listdir(path + one):
            
            if two[-3:] == 'txt' or two[-3:] == 'url':
                # print(two)
                os.remove(path + one +r'/' + two)
            elif two[-3:] == 'png' or two[-3:] == 'jpg' :
                size = int(os.stat(path + one +r'/' + two).st_size) // 1000000 
                # print(size)
                if size  ==  0 :
                    print(two)
                    os.remove(path + one +r'/' + two)
                else:
                    first = re.sub(u"([^\u0030-\u0039])", "", two.split('.')[0])
                    print(first)
                    # if cover picture is large, then rename it 0 picture
                    if first == "":
                        first = "0"
                    else:
                        while first[0] == '0':
                            first = first[1:]
                    os.rename(path + one +r'/' + two , path + one +r'/' + first )
                    namelist.append(first)
        namelist.sort()
        # print(namelist)
        count = 1
        onetrue = one.split('[')[0]
        for two in namelist:
            os.rename(path + one +r'/' + str(two), path + one +r'/' + onetrue + r' (' + str(count) + r')' + '.jpg')
            count += 1
        
                



# print(os.listdir(path))
# for one in os.listdir(path):
#     if one[0] != '.' :
#         os.rename(path+one, path+one+'.7z')
