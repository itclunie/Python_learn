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
colHeads = ["myid","Gross Margin %","Operating Income USD Mil","Operating Margin %","Net Income USD Mil","Earnings Per Share USD","Shares Mil","Book Value Per Share * USD","Operating Cash Flow USD Mil","Cap Spending USD Mil","Free Cash Flow USD Mil","COGS","Gross Margin","SG&A","Operating Margin","Net Int Inc & Other","EBT Margin","Net Margin %","Asset Turnover (Average)","Return on Assets %","Financial Leverage (Average)","Return on Equity %","Return on Invested Capital %","Year over Year","Cap Ex as a % of Sales","Free Cash Flow/Sales %","Free Cash Flow/Net Income","Cash & Short-Term Investments","Accounts Receivable","Other Current Assets","Total Current Assets","Net PP&E","Other Long-Term Assets","Accounts Payable","Accrued Liabilities","Other Short-Term Liabilities","Total Current Liabilities","Long-Term Debt","Other Long-Term Liabilities","Total Liabilities","Total Stockholders' Equity","Current Ratio","Quick Ratio","Financial Leverage","Debt/Equity","Days Sales Outstanding","Payables Period","Receivables Turnover","Fixed Assets Turnover","Asset Turnover","under=1"]


df_Trn = pd.read_csv('over50k - test.csv', names=colHeads)
df_Tst = pd.read_csv('over50k - test.csv', names=colHeads)
testDataLst = csv2lst('over50k - test.csv')

dfTrn = numeralize(df_Trn) #make strings int
dfTst = numeralize(df_Tst)

arrayTrn = dfTrn.values # make np arrays
arrayTst = dfTst.values
trainData = arrayTrn[:,1:50] #values
trainAnswers = arrayTrn[:,50] #class
testData = arrayTst[:,1:50]
testAnswers = arrayTst[:,50]
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


# (0, 'myid')
# (1, 'Gross Margin %')
# (2, 'Operating Income USD Mil')
# (3, 'Operating Margin %')
# (4, 'Net Income USD Mil')
# (5, 'Earnings Per Share USD')
# (6, 'Shares Mil')
# (7, 'Book Value Per Share * USD')
# (8, 'Operating Cash Flow USD Mil')
# (9, 'Cap Spending USD Mil')
# (10, 'Free Cash Flow USD Mil')
# (11, 'COGS')
# (12, 'Gross Margin')
# (13, 'SG&A')
# (14, 'Operating Margin')
# (15, 'Net Int Inc & Other')
# (16, 'EBT Margin')
# (17, 'Net Margin %')
# (18, 'Asset Turnover (Average)')
# (19, 'Return on Assets %')
# (20, 'Financial Leverage (Average)')
# (21, 'Return on Equity %')
# (22, 'Return on Invested Capital %')
# (23, 'Year over Year')
# (24, 'Cap Ex as a % of Sales')
# (25, 'Free Cash Flow/Sales %')
# (26, 'Free Cash Flow/Net Income')
# (27, 'Cash & Short-Term Investments')
# (28, 'Accounts Receivable')
# (29, 'Other Current Assets')
# (30, 'Total Current Assets')
# (31, 'Net PP&E')
# (32, 'Other Long-Term Assets')
# (33, 'Accounts Payable')
# (34, 'Accrued Liabilities')
# (35, 'Other Short-Term Liabilities')
# (36, 'Total Current Liabilities')
# (37, 'Long-Term Debt')
# (38, 'Other Long-Term Liabilities')
# (39, 'Total Liabilities')
# (40, "Total Stockholders' Equity")
# (41, 'Current Ratio')
# (42, 'Quick Ratio')
# (43, 'Financial Leverage')
# (44, 'Debt/Equity')
# (45, 'Days Sales Outstanding')
# (46, 'Payables Period')
# (47, 'Receivables Turnover')
# (48, 'Fixed Assets Turnover')
# (49, 'Asset Turnover')
# (50, 'under=1')