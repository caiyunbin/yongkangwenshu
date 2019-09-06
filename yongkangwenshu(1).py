# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 19:39:20 2019

@author: Caiyunbin
"""
import re 
import pandas as pd
from math import isnan

'''
##这一步是处理不包含某一些文字的内容，十分重要的一个技能
new_data = ori_data[~ori_data['内容'].str.contains('^以调解方式|^确认|^人民法院认为|^离婚诉讼|^涉及国家机密')][['序号','案件ID','案件概括','案件编号','审判时间','原告','原告律师机构','原告律师','原告法定代理人','被告','被告律师机构','被告律师','内容']]

new_data.to_excel(excel_writer = r"C:\\Users\\Administrator\\Desktop\\袁老师法律文书\\yongkang_clean.xlsx",
                  sheet_name = '永康清洗',
                  index = False,
                  columns =['案件ID','案件概括','案件编号','审判时间','原告','原告律师机构','原告律师','原告法定代理人','被告','被告律师机构','被告律师','内容'] )
'''

##加载源数据
ori_data = pd.read_excel(r'C:\\Users\\Administrator\\Desktop\\袁老师法律文书\\yongkang_clean.xlsx')
ori_data.columns = ['案件ID','案件概括','案件编号','审判时间','原告','原告律师机构','原告律师','原告法定代理人','被告','被告律师机构','被告律师','内容']

ori_data.head(20)
ori_data['内容'] = ori_data['内容'].astype('str')


##这一部分是处理借款过后的内容
ori_data1 = ori_data[['案件ID','案件概括','案件编号','审判时间','原告','原告律师机构','原告律师','原告法定代理人','被告','被告律师机构','被告律师']]

final_jiekuan1 = final_jiekuan[['还款','借款']]

final_jiekuan = pd.read_excel(r'C:\\Users\\Administrator\\Desktop\\袁老师法律文书\\final_jiekuan.xlsx')
final_jiekuan['内容'] = final_jiekuan['内容'].astype('str')



def quchuwuyong(x):
    con = x.replace('款','').replace('人民币','').replace('借款','').replace('共计','').replace('费','').replace('金','').replace('合计','').replace('元','').replace('本','').replace('借','').replace('美','')
    return con

jiekuan_clean = final_jiekuan['内容'].map(quchuwuyong)



def huankuan(x):
    if re.search('\d+',x,re.S) != None:
        res = x+'+利息'
        return res
    else:
        return  None

final_jiekuan['还款'] = jiekuan_clean.map(huankuan)


def chuliwan(x):
    if x!=None:
        if re.search('万',x,re.S) != None:
            m = float(x[:-1])*10000
            return m
        else:
            return float(x)
    else:
        return float(0)


final_jiekuan['借款'] = jiekuan_clean.map(chuliwan)


final_jiekuan.to_excel(excel_writer = r"C:\\Users\\Administrator\\Desktop\\袁老师法律文书\\final_jiekuan.xlsx")

final_jiekuan1['关系'] = ori_data['内容'].map(relationship)

def konghang(x):
    content = ''
    for l in x:
        l = l.strip()
        content +=l
    return content

ori_data['内容'] = ori_data['内容'].map(konghang)


df = pd.concat([ori_data1,final_jiekuan1],axis=1)

df.to_excel(excel_writer = r"C:\\Users\\Administrator\\Desktop\\袁老师法律文书\\永康整理版.xlsx",
                  sheet_name = '永康',
                  index = False,
                  columns =['案件ID','案件概括','案件编号','审判时间','原告','原告律师机构','原告律师','原告法定代理人','被告','被告律师机构','被告律师','还款','借款','关系'] )


result = df.dropna(subset=['借款'])

result.to_excel(excel_writer = r"C:\\Users\\Administrator\\Desktop\\袁老师法律文书\\永康无缺失值.xlsx",
                  sheet_name = '永康',
                  index = False,
                  columns =['案件ID','案件概括','案件编号','审判时间','原告','原告律师机构','原告律师','原告法定代理人','被告','被告律师机构','被告律师','还款','借款','关系'] )

###到此上面最终的文件就形成好了



##清理原告
def yuangao(x):
    con=x.replace(' ','').replace('\n','')
    pattern = re.compile('.*?原告：(.*?)。.*?')
    result = re.findall(pattern,con)
    result = '\n'.join(result)
    return result

##细致化的原告清理
def yuangao(x):
    con =  x.replace(' ','')
    pattern = re.compile('.*?原告：(.*?)。.*?')
    if pattern != None:
        result = re.findall(pattern,con)
        result = '\n'.join(result)
        return result
        if pattern == None:
            pattern = re.compile('.*?原告(.*?)。.*?')
            result = re.findall(pattern,con)
            result = '\n'.join(result)
            return result
        else:
            return None
            
##被告精细化处理
def beigao(x):
    con =  x.replace(' ','')
    pattern = re.compile('.*?被告：(.*?)。.*?')
    if pattern != None:
        result = re.findall(pattern,con)
        result = '\n'.join(result)
        return result
        if pattern == None:
            pattern = re.compile('.*?被告(.*?)。.*?')
            result = re.findall(pattern,con)
            result = '\n'.join(result)
            return result
        else:
            return None
    
##原告与被告的关系
def relationship(x):
    con =  x.replace(' ','').replace('/n','')
    pattern = re.compile('.*?与被告系(.*?)关系.*?')
    if pattern != None:
            result = re.findall(pattern,con)
            result = '\n'.join(result)
            return result
            if pattern ==None:
                pattern = re.compile('.*?与被告是(.*?)关系.*?')
                result = re.findall(pattern,con)
                result = '\n'.join(result)
                return result
                if pattern == None:
                    pattern = re.compile('.*?原告.*?与被告.*?是(.*?)关系.*?')
                    result = re.findall(pattern,con)
                    result = '\n'.join(result)
                    return result
                    if pattern == None:
                        pattern = re.compile('.*?原被告系(.*?)关系.*?')
                        result = re.findall(pattern,con)
                        result = '\n'.join(result)
                        return result
                        if pattern == None:
                            pattern = re.compile('.*?与原告是(.*?)关系.*?')
                            result = re.findall(pattern,con)
                            result = '\n'.join(result)
                            return result
                            if pattern == None:
                                pattern = re.compile('.*?原、被告系(.*?)关系.*?')
                                result = re.findall(pattern,con)
                                result = '\n'.join(result)
                                return result
                            else:
                                return None
     

##借款数量
def jiekuan_number(x):
    con =  x.replace(' ','').replace('/n','')
    pattern = re.compile('.*?借款(.*?)元.*?')     
    result = re.findall(pattern,con)
    print(type(result))
    return result
     
##从列表中取出
def douhao(x):
    con = x
    for item in x:
        return item
            


        
rela = ori_data['内容'].map(relationship)        
beigao = ori_data['内容'].map(beigao)
yuanga = ori_data['内容'].map(yuangao)

jiekuanjine = ori_data['内容'].map(jiekuan_number)   

chulihou.to_excel(excel_writer = r"C:\\Users\\Administrator\\Desktop\\袁老师法律文书\\借款.xlsx")

##关于借款金额细致化一步一步处理
def tiaomuchuli(x):
    if x!=None:
        if len(x)>12:
            if re.search('\d+万',x,re.S) != None:
                m = re.search('\d+万',x,re.S)
                return m.group()
            else:
                return x
        else:
            return x
    else:
        return None
    
    
final = chulihou.map(tiaomuchuli)    


def renmingbi(x):
    if x!=None:
        if len(x)>12:
            if re.search('人民币\d+',x,re.S) != None:
                m = re.search('人民币\d+',x,re.S)
                return m.group()
            else:
                return x
        else:
            return x
    else:
        return None

final1 = final.map(renmingbi)    


def benjin(x):
    if x!=None:
        if len(x)>12:
            if re.search('本金\d+',x,re.S) != None:
                m = re.search('本金\d+',x,re.S)
                return m.group()
            else:
                return x
        else:
            return x
    else:
        return None

final2 = final1.map(benjin)    

final2[final2.str.len()>12].count()



def kuan(x):
    if x!=None:
        if len(x)>12:
            if re.search('款\d+',x,re.S) != None:
                m = re.search('款\d+',x,re.S)
                return m.group()
            else:
                return x
        else:
            return x
    else:
        return None

final3 = final2.map(kuan)    

final3[final3.str.len()>12].count()

#还款部分的正则抽取
def huankuan_number(x):
    con =  x.replace(' ','').replace('/n','')
    pattern = re.compile('.*?判决如下：(.*?)。.*?')     
    result = re.findall(pattern,con)
    print(type(result))
    return result


huankuan = ori_data['内容'].map(huankuan_number)   

chulihou_huankuan = huankuan.map(douhao) 

def huanyuan(x):
    if x!=None:       
        if re.search('借款\d+元',x,re.S) != None:
            m = re.search('借款\d+元',x,re.S)
            return m.group()
        else:
            return x
    else:
        return None

after_extra = chulihou_huankuan.map(huanyuan) 
    
def huanwanyuan(x):
    if x!=None:       
        if re.search('借款\d+万元',x,re.S) != None:
            m = re.search('借款\d+万元',x,re.S)
            return m.group()
        else:
            return x
    else:
        return None

after_extra1 = after_extra.map(huanwanyuan) 


def huanryuan(x):
    if x!=None:       
        if re.search('人民币\d+元',x,re.S) != None:
            m = re.search('人民币\d+元',x,re.S)
            return m.group()
        else:
            return x
    else:
        return None

after_extra2 = after_extra1.map(huanryuan) 


def huanrwyuan(x):
    if x!=None:       
        if re.search('人民币\d+万元',x,re.S) != None:
            m = re.search('人民币\d+万元',x,re.S)
            return m.group()
        else:
            return x
    else:
        return None

after_extra3 = after_extra2.map(huanrwyuan) 


def huangjyuan(x):
    if x!=None:       
        if re.search('共计\d+元',x,re.S) != None:
            m = re.search('共计\d+元',x,re.S)
            return m.group()
        else:
            return x
    else:
        return None

after_extra4 = after_extra3.map(huangjyuan) 


def huangjwyuan(x):
    if x!=None:       
        if re.search('共计\d+万元',x,re.S) != None:
            m = re.search('共计\d+万元',x,re.S)
            return m.group()
        else:
            return x
    else:
        return None

after_extra5 = after_extra4.map(huangjwyuan) 


def huanbjyuan(x):
    if x!=None:       
        if re.search('本金\d+元',x,re.S) != None:
            m = re.search('本金\d+元',x,re.S)
            return m.group()
        else:
            return x
    else:
        return None

after_extra6 = after_extra5.map(huanbjyuan) 



def huanbjwyuan(x):
    if x!=None:       
        if re.search('本金\d+万元',x,re.S) != None:
            m = re.search('本金\d+万元',x,re.S)
            return m.group()
        else:
            return x
    else:
        return None

after_extra7 = after_extra6.map(huanbjwyuan) 



def huankyyuan(x):
    if x!=None:       
        if re.search('款\d+元',x,re.S) != None:
            m = re.search('款\d+元',x,re.S)
            return m.group()
        else:
            return x
    else:
        return None

after_extra8 = after_extra7.map(huankyyuan) 


def huankwyyuan(x):
    if x!=None:       
        if re.search('款\d+万元',x,re.S) != None:
            m = re.search('款\d+万元',x,re.S)
            return m.group()
        else:
            return x
    else:
        return None

after_extra10 = after_extra9.map(huankwyyuan) 


def huangjdyuan(x):
    if x!=None:       
        if re.search('共计\d+\.\d+元',x,re.S) != None:
            m = re.search('共计\d+\.\d+元',x,re.S)
            return m.group()
        else:
            return x
    else:
        return None

after_extra9 = after_extra8.map(huangjdyuan) 



def huankwydyuan(x):
    if x!=None:       
        if re.search('款\d+\.\d+元',x,re.S) != None:
            m = re.search('款\d+\.\d+元',x,re.S)
            return m.group()
        else:
            return x
    else:
        return None

after_extra11 = after_extra10.map(huankwydyuan) 


def huanrmbdyuan(x):
    if x!=None:       
        if re.search('人民币\d+\.\d+元',x,re.S) != None:
            m = re.search('人民币\d+\.\d+元',x,re.S)
            return m.group()
        else:
            return x
    else:
        return None

after_extra12 = after_extra11.map(huanrmbdyuan) 


def huanbjdyuan(x):
    if x!=None:       
        if re.search('本金\d+\.\d+元',x,re.S) != None:
            m = re.search('本金\d+\.\d+元',x,re.S)
            return m.group()
        else:
            return x
    else:
        return None

after_extra13 = after_extra12.map(huanbjdyuan) 


after_extra13[after_extra13.str.len()>12].count()


def huanfwyuan(x):
    if x!=None:       
        if re.search('费\d+万元',x,re.S) != None:
            m = re.search('费\d+万元',x,re.S)
            return m.group()
        else:
            return x
    else:
        return None

after_extra14 = after_extra13.map(huanfwyuan) 


def huanjyyuan(x):
    if x!=None:       
        if re.search('金\d+元',x,re.S) != None:
            m = re.search('金\d+元',x,re.S)
            return m.group()
        else:
            return x
    else:
        return None

after_extra15 = after_extra14.map(huanjyyuan) 



def huanjydyuan(x):
    if x!=None:       
        if re.search('金\d+\.\d+元',x,re.S) != None:
            m = re.search('金\d+\.\d+元',x,re.S)
            return m.group()
        else:
            return x
    else:
        return None

after_extra16 = after_extra15.map(huanjydyuan) 


def huanjydyuan(x):
    if x!=None:       
        if re.search('合计\d+\.\d+元',x,re.S) != None:
            m = re.search('合计\d+\.\d+元',x,re.S)
            return m.group()
        else:
            return x
    else:
        return None

after_extra17 = after_extra16.map(huanjydyuan) 


after_extra17[after_extra13.str.len()>17].count()


def bohuiyuangao(x):
    if x!=None:       
        if re.search('驳回.*?',x,re.S) != None:
            x=None
            return x
        else:
            return x
    else:
        return None

after_extra18 = after_extra17.map(bohuiyuangao) 

after_extra18[after_extra18.str.len()>17].count()



def huanrmbddyuan(x):
    if x!=None:       
        if re.search('人民币\d+\.\d+万元',x,re.S) != None:
            m = re.search('人民币\d+\.\d+万元',x,re.S)
            return m.group()
        else:
            return x
    else:
        return None

after_extra19 = after_extra18.map(huanrmbddyuan) 


after_extra19[after_extra19.str.len()>17].count()



def huanjkdwyyuan(x):
    if x!=None:       
        if re.search('借款\d+\.\d+万元',x,re.S) != None:
            m = re.search('借款\d+\.\d+万元',x,re.S)
            return m.group()
        else:
            return x
    else:
        return None

after_extra20 = after_extra19.map(huanjkdwyyuan) 


after_extra20[after_extra20.str.len()>17].count()


def lihun(x):
    if x!=None:       
        if re.search('离婚',x,re.S) != None:
            x=None
            return x
        else:
            return x
    else:
        return None

after_extra21 = after_extra20.map(lihun) 


after_extra21[after_extra21.str.len()>17].count()



def quzhifu(x):
    if x!=None:
        if len(x)>17:
            if re.search('支付',x,re.S) != None:
                return x
            else:
                return None
        else:
            return x
    else:
        return None


after_extra22 = after_extra21.map(quzhifu) 


after_extra22[after_extra22.str.len()>17].count()



after_extra22.to_excel(excel_writer = r"C:\\Users\\Administrator\\Desktop\\袁老师法律文书\\after_extra22.xlsx")

final3.to_excel(excel_writer = r"C:\\Users\\Administrator\\Desktop\\袁老师法律文书\\final3.xlsx")    

chulihou = jiekuanjine.map(tiaomuchuli) 


def huankuan(x):
    con =  x.replace(' ','').replace('/n','')
    pattern = re.compile('.*?判决如下：(.*?)。')
    result = re.findall(pattern,con)
    result = '\n'.join(result)
    return result

huankuan = ori_data['内容'].map(huankuan)   
    

f = open('C:\\Users\\Administrator\\Desktop\\袁老师法律文书\\yongkang.txt')
content = f.read()
con=content.replace(' ','').replace('\n','')
pattern = re.compile('.*?被告：(.*?)。.*?')






