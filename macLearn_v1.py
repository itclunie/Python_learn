import csv, sys, os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier as RFC
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

def numeralize(df):
	for myCol in df:
		if type(df[myCol][0]) != np.int64 and myCol != 'u_id' and myCol != 'overunder':
			colFacd = pd.factorize(df[myCol])
			df[myCol] = colFacd[0]
	return df

def csv2lst(csv_Path):
	with open(csv_Path, 'r') as output:
		reader = csv.reader(output, lineterminator = '\n')
		lst = list(reader)
	return lst

# Load dfs
colHeads = ['u_id','age','workclass','1fnlwgt','education','education-num','marital-status','occupation','relationship','race','sex','capital-gain','capital-loss','hours-per-week','native-country','overunder']

df_Trn = pd.read_csv('over50k - test.csv', names=colHeads)
df_Tst = pd.read_csv('over50k - test.csv', names=colHeads)
testDataLst = csv2lst('over50k - test.csv')

dfTrn = numeralize(df_Trn) #make strings int
dfTst = numeralize(df_Tst)

arrayTrn = dfTrn.values # make np arrays
arrayTst = dfTst.values
trainData = arrayTrn[:,1:15] #values
trainAnswers = arrayTrn[:,15] #class
testData = arrayTst[:,1:15]
testAnswers = arrayTst[:,15]
testIndex = arrayTst[:,0]

models = []
models.append(['LR', LogisticRegression(), [] ])
models.append(['LDA', LinearDiscriminantAnalysis(), [] ])
models.append(['KNN', KNeighborsClassifier(), [] ])
models.append(['CART', DecisionTreeClassifier(), [] ])
models.append(['NB', GaussianNB(), [] ])
models.append(['SVM', SVC(), [] ])
models.append(['RFC', RFC(n_jobs=2,n_estimators=50), [] ])

cnt = 0
for name, model, predictions in models:
	model.fit(trainData, trainAnswers)
	predictions = model.predict(testData)
	score = accuracy_score(testAnswers, predictions)

	models[cnt][2] = predictions #store predictions back into models list
	models[cnt].append(score)
	print(name, score)
	cnt += 1

writeOut = []
for i in range(len(testDataLst)):
	writeOut.append([testDataLst[i], testIndex[i], testAnswers[i], models[0][2][i], models[1][2][i], models[2][2][i], models[3][2][i], models[4][2][i], models[5][2][i], models[5][2][i] ])

df2csv = pd.DataFrame(writeOut, columns=['LestData','testIndex','testAnswers','LR_pred','LDA_pred','KNN_pred','CART_pred','NB_pred','SVM_pred','RFC_pred'])
df2csv.to_csv('pred.csv', index=False)

