
import pymysql
import platform
import sys 
# print(os.name)
# print(platform.system())


connection = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='vajors123',
    database='vajor'
)



origin = "http://47.251.62.169:2007/fetch"
# origin = "http://139.224.37.10:2007/fetch"

if platform.system() == 'Linux':

    path = f'/home/vajor/images/albumn'
    previewpath = f"/home/vajor/images/preview"
    # print(path,backpath)
else:
    model = sys.argv[0].split('/')[-1][:-3]

    path=r"/Users/vajor/Desktop/Pictures/%s/images" % model
    backpath=r"/Users/vajor/Desktop/Pictures/%s/backup" % model


institutions = {'尤果网':'尤果网','ugirls':'尤果网','果团网':'果团网','girlt':'果团网','喵糖映画':'喵糖映画',\
                'bololi':'波萝社','波萝社':'波萝社','xiuren':'秀人网','秀人网':'秀人网','mygril':'美媛馆','美媛馆':'美媛馆',\
                'youwu':'尤物馆','尤物馆':'尤物馆','imiss':'爱蜜社',"爱蜜社":'爱蜜社','蜜桃':'miitao蜜桃社','蜜桃社':'蜜桃社',\
                'uxing':'优星馆',"优星馆":"优星馆",'tukmo':'兔几盟','兔几盟':'兔几盟','feilin':'嗲囡囡','嗲囡囡':'嗲囡囡',\
                'mistar':'魅妍社','魅妍社':'魅妍社','wings':'影私荟','影私荟':'影私荟','leyuan':'星乐园','星乐园':'星乐园',\
                'mfstar':'模范学院','模范学院':'模范学院','huayan':'花の颜','花の颜':'花の颜','dkgirl':'御女郎',\
                '御女郎':'御女郎','candy':'网红馆','网红馆':'网红馆','partycat':'轰趴猫','轰趴猫':'轰趴猫','cosplay':'Cosplay',\
                'xgyw':'散图','micat':'猫萌榜','猫萌榜':'猫萌榜' ,'xingyan':'星颜社', '星颜社': '星颜社',\
                'xiaoyu':'画语界', '画语界':'画语界', 'youmi':'优蜜荟', '优蜜荟':'优蜜荟',\
                'Pure Media' : 'Pure Media'}



girlname_dict = {'Yeha':'Yeha', '幼幼':'幼幼','Chunmomo':'蠢沫沫',\
        '桜井宁宁':'桜井宁宁','Sakurai Ningning':'桜井宁宁',\
        'Rinaijiao':'日奈娇','晕崽':'晕崽'}


remove_list = ['Cosplaytele', 'cosplaytele', '4khd', '4KHD']
keywords_list = ['内购']
