import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report,accuracy_score,precision_score,recall_score
import joblib

df = pd.read_csv('../../Class/Day 14/churn.csv')
df = df.iloc[:,3:]
# print(df.shape)

df = df.drop(['Geography','Gender'],axis=1)
x = df.drop('Exited',axis=1)
y = df['Exited']

xtrain,xtest,ytrain,ytest = train_test_split(x,y,random_state=7,test_size=0.2)

lg = LogisticRegression(solver='newton-cholesky')

model = lg.fit(xtrain,ytrain)
pred = model.predict(xtest)
acc = accuracy_score(pred,ytest)
precision = precision_score(pred,ytest)
report = classification_report(pred,ytest)
recall = recall_score(pred,ytest)

print('\nClassification Report')
print('-'*68)
print(report)
print(f'Total Model Accuracy -  {acc:.2f}')
print(f'Total Model Precision -  {precision:.2f}')
print(f'Total Model Recall -  {recall:.2f}\n')

joblib.dump(model,'lr_model.joblib')
