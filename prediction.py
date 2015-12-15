# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 10:27:55 2015

@author: ices
"""
import os
os.chdir('E:/gd_Bus/part2/')

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pandas import Series,DataFrame

#计算偏差、精度
def count_precision(Y_test,Y_predict):
    deviations = 0
    precision = 0
    for i in np.arange(0,len(Y_test)):
        cur_dev = abs(Y_test[i]-Y_predict[i])/Y_test[i]
        deviations = deviations + cur_dev
        if(cur_dev==0): #可以不要
            cur_pre = 10
        elif(cur_dev>0.3): #此项必须
            cur_pre = 0
        else:
            #cur_pre = 10*(1-cur_dev**3/(0.3**3))
            cur_pre = 10*(1-cur_dev**0.3/(0.3**0.3))
        precision = precision + cur_pre
    precision = precision / (10*len(Y_test))
    return deviations,precision

#获得合并的训练数据

#得到的线路数据
LINE = '6'

merge_train_data = pd.read_csv('preprocess\merge_train_data'+LINE+'.txt',index_col=0) #包含索引列,让索引列作为行索引
print '---merge_train_data:---'
print merge_train_data[:5] 
print merge_train_data.dtypes

merge_test_data = pd.read_csv('preprocess\merge_test_data'+LINE+'.txt',index_col=0).sort(columns=['month','day','hours']) #检验下
print '---merge_test_data:---'
print merge_test_data[:5]
print merge_test_data.dtypes

#--- 训练 回归 模型--用训练数据自测-------------------
#features = ['day','hours','Wday','Wnight','WDFday','WDFnight','Tday','Tnight','week','isWork','firstWork','lastWork','dayFestival']
#features = ['hours','isWork','week'] #
features = ['hours','isWork','avgT','Wday','lastWork','dayFestival'] #线路11
#features = ['hours','isWork','avgT','Wday','week','lastWork','dayFestival'] #线路6
#features = ['hours','isWork','isFestival','firstWork'] #线路6,线路11

'''
train_count = len(merge_train_data) - 7*16  #预测一周
#得到训练集、测试集的特征值、真实值（转为数组）
X_train = merge_train_data.ix[:train_count-1,features].values
Y_train = merge_train_data.ix[:train_count-1,['counts']].values.flatten() #得到的y是二维数组n行1列，，要转为一维数组

X_test  = merge_train_data.ix[train_count:,features].values
Y_test  = merge_train_data.ix[train_count:,['counts']].values.flatten()

'''
#得到中秋节第一天的索引--中秋节开始7天和要预测的目标7天比较像（3天假，4天班）-9月6号~9月12号
moonday = merge_train_data[ merge_train_data['month']== 9]  #index 538~649
moonday = moonday[ merge_train_data['day']<=12 ]
moonday = moonday[ merge_train_data['day']>=6 ]

X_test = moonday.ix[:,features].values
Y_test = moonday.ix[:,['counts']].values.flatten()

X_train1 = merge_train_data.ix[:537,features].values
X_train2 = merge_train_data.ix[650:,features].values
X_train = np.append(X_train1,X_train2,axis = 0)
Y_train1 = merge_train_data.ix[:537,['counts']].values.flatten() #得到的y是二维数组n行1列，，要转为一维数组
Y_train2 = merge_train_data.ix[650:,['counts']].values.flatten() #得到的y是二维数组n行1列，，要转为一维数组
Y_train = np.append(Y_train1,Y_train2,axis = 0)

'''
#对特征标准化
from sklearn import preprocessing
scaler = preprocessing.StandardScaler().fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)
'''
'''
#对特征编码，01 10--可能适合做分类
from sklearn import preprocessing
enc = preprocessing.OneHotEncoder()
enc.fit(X_train)
X_train = enc.transform(X_train).toarray()
X_test = enc.transform(X_test).toarray()
#X_test = X_train
#Y_test = Y_train
'''

'''
#---训练--SVM回归---
from sklearn import svm
clf = svm.SVR()
clf.fit(X_train, Y_train)
Y_predict = clf.predict(X_test)

X = np.arange(1,len(X_test)+1)
plt.plot(X,Y_test,label='true',c='b')
plt.hold('on')
plt.plot(X,Y_predict,label='predict',c='y')
plt.hold('off')
plt.show()

deviation,precision = count_precision(Y_test,Y_predict)
print 'SVM回归'
print '总偏差：',deviation
print '平均精度：',precision
'''

'''
#--决策树---
from sklearn import tree
clf = tree.DecisionTreeRegressor()
clf.fit(X_train, Y_train)
Y_predict = clf.predict(X_test)

# 发现决策树方式得到的结果并不稳定，，多次取平均
for i in np.arange(1,1000):
    clf = tree.DecisionTreeRegressor()
    clf.fit(X_train, Y_train)
    Y_predict = Y_predict + clf.predict(X_test)
Y_predict = Y_predict/1000

X = np.arange(1,len(X_test)+1)
plt.plot(X,Y_test,label='true',c='b')
plt.hold('on')
plt.plot(X,Y_predict,label='predict',c='r')
plt.hold('off')
plt.show()

deviation,precision = count_precision(Y_test,Y_predict)
print '决策树回归：'
print '总偏差：',deviation
print '平均精度：',precision
#--决策树---end
'''
'''
#--Bayesian Ridge Regression--
#from sklearn.metrics import mean_squared_error
from sklearn import linear_model

clf = linear_model.BayesianRidge()
clf.fit(X_train, Y_train)
Y_predict = clf.predict(X_test)

X = np.arange(1,len(X_test)+1)
plt.plot(X,Y_test,label='true',c='b')
plt.hold('on')
plt.plot(X,Y_predict,label='predict',c='r')
plt.hold('off')
plt.show()

deviation,precision = count_precision(Y_test,Y_predict)
print 'BayesianRidge回归:'
print '总偏差：',deviation
print '平均精度：',precision
#print '均方误差',mean_squared_error(Y_test, Y_predict)

#--Bayesian Ridge Regression--end
'''

#--RandomForestRegressor---
#from sklearn.ensemble import ExtraTreesRegressor
from sklearn.ensemble import RandomForestRegressor
#clf = ExtraTreesRegressor(n_estimators=1000)
clf = RandomForestRegressor(n_estimators=2000)
clf.fit(X_train, Y_train)
Y_predict = clf.predict(X_test)

X = np.arange(1,len(X_test)+1)
plt.plot(X,Y_test,label='true',c='b')
plt.hold('on')
plt.plot(X,Y_predict,label='predict',c='r')
plt.hold('off')
plt.show()

deviation,precision = count_precision(Y_test,Y_predict)
print '随机森林回归:'
print '总偏差：',deviation
print '平均精度：',precision


#--GradientBoostingRegressor---
from sklearn.ensemble import GradientBoostingRegressor
est = GradientBoostingRegressor(n_estimators=2000, learning_rate=0.8,max_depth=2, random_state=0, loss='ls')
est.fit(X_train, Y_train)
Y_predict = est.predict(X_test)

X = np.arange(1,len(X_test)+1)
plt.plot(X,Y_test,label='true',c='b')
plt.hold('on')
plt.plot(X,Y_predict,label='predict',c='r')
plt.hold('off')
plt.show()

deviation,precision = count_precision(Y_test,Y_predict)
print 'GradientBoosting回归:'
print '总偏差：',deviation
print '平均精度：',precision


#---得到结果---
X_train = merge_train_data.ix[:,features].values
Y_train = merge_train_data.ix[:,['counts']].values.flatten() #得到的y是二维数组n行1列，，要转为一维数组

X_test  = merge_test_data.ix[:,features].values

#from sklearn.ensemble import ExtraTreesRegressor
from sklearn.ensemble import RandomForestRegressor
#clf = ExtraTreesRegressor(n_estimators=1000)
clf = RandomForestRegressor(n_estimators=2000)
clf.fit(X_train, Y_train)
Y_predict = clf.predict(X_test)

plt.plot(X,Y_predict,label='predict',c='b')

Y_predict = [round(x) for x in Y_predict]
Y_predict_save = DataFrame(list(Y_predict),columns = ['line'+LINE])
Y_predict_save.to_csv('result\line'+LINE+'.txt')
