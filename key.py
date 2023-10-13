#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 20:40:02 2020

@author: vajorstack
"""
import re

def keys(text):

    key=text.select('meta[name="keywords"]')[0]['content'].split(',')
    title = text.head.title.text.split('_')[1]

    description=text.select('meta[name="description"]')[0]['content'].split('    ')[-1]
    print(key)
    column=key[2]
    pattern = r'\d+'
    match = re.search(pattern,column)
    institutions = {'尤果网':'尤果网','ugirls':'尤果网','果团网':'果团网','girlt':'果团网','喵糖映画':'喵糖映画',\
                    'bololi':'波萝社','波萝社':'波萝社','xiuren':'秀人网','秀人网':'秀人网','mygril':'美媛馆','美媛馆':'美媛馆',\
                    'youwu':'尤物馆','尤物馆':'尤物馆','imiss':'爱蜜社',"爱蜜社":'爱蜜社','蜜桃':'miitao蜜桃社','蜜桃社':'蜜桃社',\
                    'uxing':'优星馆',"优星馆":"优星馆",'tukmo':'兔几盟','兔几盟':'兔几盟','feilin':'嗲囡囡','嗲囡囡':'嗲囡囡',\
                    'mistar':'魅妍社','魅妍社':'魅妍社','wings':'影私荟','影私荟':'影私荟','leyuan':'星乐园','星乐园':'星乐园',\
                    'mfstar':'模范学院','模范学院':'模范学院','huayan':'花の颜','花の颜':'花の颜','dkgirl':'御女郎',\
                    '御女郎':'御女郎','candy':'网红馆','网红馆':'网红馆','partycat':'轰趴猫','轰趴猫':'轰趴猫','cosplay':'Cosplay',\
                    'xgyw':'散图','micat':'猫萌榜','猫萌榜':'猫萌榜' ,'xingyan':'星颜社', '星颜社': '星颜社',\
					'xiaoyu':'画语界', '画语界':'画语界', 'youmi':'优蜜荟', '优蜜荟':'优蜜荟', }
    column = column.lower()
    print(column)
    institution_name = '性感尤物'
    for institution in institutions:
        if institution in column:
            institution_name = institutions[institution]
            break

    # institution = column.

    print("key  3")
    print(institution_name)
    print(institution_name.lower())
    institution_name = institution_name.lower()
    print(institution_name)
    print("key  4")

    mnname=key[1].strip('资料')
    keywords=set()
    school=text.title.text.split('_')[0]
    # print(key)
    print("key  5")
    change_name_list={"恩率babe":"徐cake","恩率":"徐cake"}
    if mnname in change_name_list:
        mnname=change_name_list[mnname]
    print("key  6")

    in_list=['黄色','白丝','户外','黑色','白色','粉色','吊带','浴室','蕾丝','翘臀','清纯','粉红','兔女郎','居家','红色','情趣','真空','女仆','情人节','护士',\
              '古装','沙滩','热裤', '海边','露背毛衣','丁字裤','奶油','短裙','旗袍','缕空','黑丝','霸气','美少女','比基尼','大海','灰色','连身裙',"半脱","蓝色",\
                '胶布',"美腿","薄纱","端午","民国","全裸",'日系','婚纱','连衣裙','胶带']
    replace_list={'全脱':"全裸","乳":"美胸","胸":"美胸","和服":"和服","遮点":"遮点","胴体":"全裸","无内":"全裸","捆绑":"捆绑","警":"女警","JK":"JK","OL":"OL","短牛仔裤":"热裤",
                  "三点式":"比基尼","学生装":"JK","合集":"合集","萝莉":"萝莉","剑道":"剑道","甜美":"甜美","运动":"运动","职场":"OL","秘书":"OL",
                  "Cos":"cos","COS":"cos","cos":"cos",'屁沟':"裸臀","裸下半身":"裸臀","职业装":"OL","连体":"死库水",'黄':'黄色'}
    print("key  7")

    for one in replace_list:
        if one in description:
            keywords.add(replace_list[one])
    for one in replace_list:
        if one in title:
            keywords.add(replace_list[one])
    for one in in_list:
        if one in description:
            keywords.add(one)
    for one in in_list:
        if one in title:
            keywords.add(one)
    print("key  8")
                
    return keywords,description,column,mnname
                
                
                
                
