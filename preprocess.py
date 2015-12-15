# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 10:23:32 2015

@author: ices
"""
import os
os.chdir('E:/gd_Bus/part2/')

import pandas as pd
from pandas import Series,DataFrame
import numpy as np

#得到的线路数据
LINE = '6'

#%pwd
train_data = pd.read_csv('origins_data\gd_train_data.txt',names=['Use_city','Line_name','Terminal_id','Card_id','Create_city','Deal_time','Card_type'])
print train_data[:5]

# 此段应该也可以用 replace() 函数得到,传入列表或字典
#weather['Wday'] = weather['Wday'].repleace(['多云','霾','阴','中雨','阵雨','雷阵雨','小到中雨','小雨','大雨','中到大雨','大到暴雨'].[1,2,2,2,3,3,3,3,3,4,4,4])
def conver_w(wx):
    if wx=='晴':
        return 1
    elif wx in ['多云','霾','阴']:
        return 2
    elif wx in ['中雨','阵雨','雷阵雨','小到中雨','小雨']:
        return 3
    elif wx in ['大雨','中到大雨','大到暴雨']:
        return 4
    else:
        return 0
def conver_wdf(wdfx):
    if wdfx in ['无持续风向微风转3-4级','无持续风向≤3级']:
        return 1
    elif wdfx in ['北风4-5级','北风微风转3-4级','东北风3-4级','北风3-4级']:
        return 3
    elif wdfx in ['东南风3-4级','东风4-5级']:
        return 2
    else:
        return 0
        
#---按照路线、时间统计------------------
#count_line = DataFram()
grouped = train_data.groupby(by=['Line_name','Deal_time'])
counts_line = {}
for (line,time),group in grouped:
    counts_line.setdefault('Line_name',[]).append(line)
    #counts_line.setdefault('Deal_time',[]).append(time)
    timestr = '%d' %time
    counts_line.setdefault('year',[]).append(int(timestr[:4]))
    counts_line.setdefault('month',[]).append(int(timestr[4:6]))
    counts_line.setdefault('day',[]).append(int(timestr[6:8]))
    counts_line.setdefault('hours',[]).append(int(timestr[8:10]))
    counts_line.setdefault('hours2',[]).append(int(timestr[8:10]) * int(timestr[8:10]))
    counts_line.setdefault('counts',[]).append(len(group))
    #lines = lines.append(line) #会出错，初始时，lines为Null，Null没有append方法

counts_line = DataFrame(counts_line,columns=['Line_name','year','month','day','hours','counts','hours2'])
counts_line = counts_line[ counts_line['hours'] >5 ]
counts_line = counts_line[ counts_line['hours'] <22 ]
print counts_line[:3]

#-获得线路10的时间-刷卡序列
line10_list = counts_line[counts_line['Line_name'] == '线路'+LINE ]
line10_list = line10_list.drop('Line_name',axis = 1) # 丢掉线路名称列
print line10_list[:3]
print line10_list.dtypes

#测试某天6~21时间段出行情况
#test = line10_list[2:18] #20140801,06~21(去掉了05,00,22,23)
#oneday = [ x+6 for x in np.arange(30) if (x+5) < 21]
#plt.plot(oneday,test['counts'])


#---处理天气数据-----
#col_names=['Date_time','Weather','Temperature','Wind_direction_force']
col_names=['year','month','day','Wday','Wnight','Tday','Tnight','WDFday','WDFnight']
weather = pd.read_csv('origins_data\gd_weather_report.txt',sep='[,/]',names = col_names)
print weather[:3]

print '多少天？',len(weather) #184天
print '多少种天气?' #12种天气
Wday_types = set(weather['Wday'].unique()) #.unique()之后是一个数组
Wnight_types = set(weather['Wnight'].unique())
Wtypes = Wday_types | Wnight_types
Wtypes = list(Wtypes)
Wtypes = Series(np.arange(1,len(Wtypes)+1), index=Wtypes )  #得到天气名称，标号 序列
print Wtypes ##有时候乱码
print weather['Wnight'].value_counts() #统计晚上天气出现频率--乱码
#weather['Wday'] = weather['Wday'].map(Wtypes)  #传入 series或字典，进行映射
#weather['Wnight'] = weather['Wnight'].map(Wtypes)
weather['Wday'] = weather['Wday'].map(conver_w)  #传入映射函数
weather['Wnight'] = weather['Wnight'].map(conver_w)  #传入映射函数


print '多少种风向风力?' #8种
Wdf_day_types = set(weather['WDFday'].unique())
Wdf_night_types = set(weather['WDFnight'].unique())
Wdf_types = Wdf_day_types | Wdf_night_types
Wdf_types = list(Wdf_types)
#Wdf_types = np.array(Wdf_types)
Wdf_types = Series(np.arange(1,len(Wdf_types)+1), index=Wdf_types )
print Wdf_types
print weather['WDFday'].value_counts()

weather['WDFday'] = weather['WDFday'].map(conver_wdf)  #传入映射函数
weather['WDFnight'] = weather['WDFnight'].map(conver_wdf)  #传入映射函数

print '温度范围？'
#去掉℃
#weather['Tday'] = [ int(filter(lambda x:x.isdigit(),tem)) for tem in  weather['Tday'].values]
#weather['Tnight'] = [ int(filter(lambda x:x.isdigit(),tem)) for tem in  weather['Tnight'].values]
# 去掉℃  也可以用矢量化的字符串操作
weather['Tday'] = weather['Tday'].str.replace('℃','').map(int)
weather['Tnight'] = weather['Tnight'].str.replace('℃','').map(int)
#统计温度最低、最高
maxT = max(weather['Tday']) if max(weather['Tday'])>max(weather['Tnight']) else max(weather['Tnight'])
minT = min(weather['Tday']) if min(weather['Tday'])<min(weather['Tnight']) else min(weather['Tnight'])
print '最高气温：', maxT, '最低气温：', minT

f2 = lambda x: ( x - minT) / 5 +1
weather['Tday'] = weather['Tday'].map(f2)
weather['Tnight'] = weather['Tnight'].map(f2)

'''#for循环写法-------------------------   
#--将天气、风力换成标号
#温度分桶处理 4~36，差32，每5度作为分割
for i in range(0,len(weather)):
    #weather.ix[i,'Wday'] = int( Wtypes[ weather.ix[i,'Wday'] ] )#转换为对应的标签
    #weather.ix[i,'Wnight'] = int( Wtypes[ weather.ix[i,'Wnight'] ] )#转换为对应的标签
    #weather.ix[i,'WDFday'] = int( Wdf_types[ weather.ix[i,'WDFday'] ] )#转换为对应的标签
    #weather.ix[i,'WDFnight'] = int( Wdf_types[ weather.ix[i,'WDFnight'] ] )#转换为对应的标签
    #dividing bucket分桶处理，，将某些近似天气合并
    weather.ix[i,'Wday'] = conver_w(weather.ix[i,'Wday'])
    weather.ix[i,'Wnight'] = conver_w(weather.ix[i,'Wnight'])
    weather.ix[i,'WDFday'] = conver_wdf(weather.ix[i,'WDFday'])
    weather.ix[i,'WDFnight'] = conver_wdf(weather.ix[i,'WDFnight'])
    #去掉℃
    #weather.ix[i,'Tday'] = int(filter(lambda x:x.isdigit(),weather.ix[i,'Tday']))
    #weather.ix[i,'Tnight'] = int(filter(lambda x:x.isdigit(),weather.ix[i,'Tnight']))
    weather.ix[i,'Tday'] = (( weather.ix[i,'Tday'] - minT ) / 5) +1
    weather.ix[i,'Tnight'] = (( weather.ix[i,'Tnight'] - minT ) / 5) +1
'''
for i in range(0,len(weather)):
    weather['avgT'] = (weather['Tnight'] + weather['Tday'])/2

print weather[:3]
print weather.dtypes #单个元素改类型int，没有成功

#生成扩展特征: 从 2014-08-01 ~ 2015-01-07
#添加 星期几，是否是节假日，是否调休等特征
#星期几、是否是工作日、是否是节日，节日第几天，每周工作第几日、当月第几个工作日
extend_feature = {}
howmuchday = len(weather) #184天天气，，但是1月7号之后的数据目前并不需要
#--星期几--
extend_feature['week'] = list(np.arange(1,8)) * (howmuchday/7 +1)
extend_feature['week'] = extend_feature['week'][:len(weather)-3]
extend_feature['week'] = [5,6,7] + extend_feature['week'] #8月1号，星期5
#--是否是节日
#中秋节，09-6~8  国庆节，10-1~7，元旦，1-1~3
extend_feature['isFestival'] = [0]*howmuchday
extend_feature['isFestival'][36:36+3] = [1]*3
extend_feature['isFestival'][61:61+7] = [1]*7
extend_feature['isFestival'][153:153+3] = [1]*3
#--节日第几天
extend_feature['dayFestival'] = [0]*howmuchday
extend_feature['dayFestival'][36:36+3] = [1,2,3] #中秋节
extend_feature['dayFestival'][61:61+7] = [1,1,2,2,2,3,3] #国庆节？？？设置为1~7可能并没有帮助
extend_feature['dayFestival'][153:153+3] = [1,2,3]  #元旦
#--是否是工作日
extend_feature['isWork'] = [ int(x<6) for x in extend_feature['week']]
extend_feature['isWork'][36:36+3] = [0]*3
extend_feature['isWork'][61:61+7] = [0]*7
extend_feature['isWork'][61+10] = 1 ##调休
extend_feature['isWork'][153:153+3] = [0]*3
extend_feature['isWork'][153+3] = 1  #调休
#--每周工作第几日-----？？？
extend_feature['firstWork'] = [ x for x in extend_feature['week']]
#extend_feature[ extend_feature['firstWork']<6 ] = 0 没起作用
for i in np.arange(0,len(extend_feature['firstWork'])):
    if extend_feature['firstWork'][i]>5:
        extend_feature['firstWork'][i] = 0
extend_feature['firstWork'][39:39+4] = [1,2,3,4]
extend_feature['firstWork'][61-2:61] = [1,2]
extend_feature['firstWork'][61+7:61+7+4] = [1,2,3,4]
extend_feature['firstWork'][153-3:153] = [1,2,3]
extend_feature['firstWork'][153+3:153+3+6] = [1,2,3,4,5,6]
#---每周最后几个工作日---
extend_feature['lastWork'] = [ x for x in extend_feature['week']]
#extend_feature[ extend_feature['firstWork']<6 ] = 0 没起作用
for i in np.arange(0,len(extend_feature['lastWork'])):
    if extend_feature['lastWork'][i]>5:
        extend_feature['lastWork'][i] = 0
    else:
        extend_feature['lastWork'][i] = 6 - extend_feature['lastWork'][i]
extend_feature['lastWork'][39:39+4] = [4,3,2,1]
extend_feature['lastWork'][61-2:61] = [2,1]
extend_feature['lastWork'][61+7:61+7+4] = [4,3,2,1]
extend_feature['lastWork'][153-3:153] = [3,2,1]
extend_feature['lastWork'][153+3:153+3+6] = [6,5,4,3,2,1]
#--每周最后几个工作日---
#--当月第几个工作日----？？？
extend_feature = DataFrame(extend_feature,columns=['week','isFestival','dayFestival','isWork','firstWork','lastWork'])

#----将天气特征与扩展特征合并
merge_day_feature = pd.merge(weather, extend_feature, left_index=True, right_index=True)

#merge_train_data = pd.merge(line10_list,weather[weather['year']<2015])  #没有合并扩展特征
merge_train_data = pd.merge(line10_list,merge_day_feature[merge_day_feature['year']<2015])
#print merge_train_data[:5]
#merge_train_data.dtypes

# 不会将 DataFrame中的Object转为int，暂且用现存文件，再读文件方式得到
merge_train_data.to_csv('preprocess\merge_train_data'+LINE+'.txt',sep=',')
merge_train_data = pd.read_csv('preprocess\merge_train_data'+LINE+'.txt',index_col=0) #包含索引列,让索引列作为行索引
print '---merge_train_data:---'
print merge_train_data[:5] 
print merge_train_data.dtypes


#得到测试时间的 year，month，day，hour
test_line10_list = {}
howmuch = 7*16
test_line10_list['year'] = [2015] *7*16
test_line10_list['month'] = [1] *7*16
test_line10_list['day'] = list(np.arange(1,8)) * 16
test_line10_list['hours'] = list(np.arange(6,22)) * 7
test_line10_list['hours2'] = [ x**2 for x in list(np.arange(6,22)) ] * 7
test_line10_list = pd.DataFrame(test_line10_list, columns=['year','month','day','hours','hours2'])
#test_line10_list = pd.DataFrame(test_line10_list, columns=['year','month','day','hours'])
#merge_test_data = pd.merge(test_line10_list,weather[weather['year']==2015])
merge_test_data = pd.merge(test_line10_list,merge_day_feature[merge_day_feature['year']==2015])
merge_test_data.to_csv('preprocess\merge_test_data'+LINE+'.txt')  # 存到文件，，进行预测调试时，不用重复进行上诉处理，可直接读文件获得
merge_test_data = pd.read_csv('preprocess\merge_test_data'+LINE+'.txt',index_col=0) #检验下
print '---merge_test_data:---'
print merge_test_data[:5]
print merge_test_data.dtypes