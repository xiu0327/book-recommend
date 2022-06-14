import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle
import requests
import json

# 1. 데이터 불러오기 - 추후 API로 불러올 예정
dataset = pd.read_csv('ML/Salary_Data.csv')

# 2. 모델 설계 및 학습 - 테스트용으로 작성됨
X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, 1].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.33, random_state = 777)

salary_model = LinearRegression()
salary_model.fit(X_train, y_train)

y_pred = salary_model.predict(X_test)

# 3. pickle을 통한 모델 저장 - 아주 중요한 부분, 서버에 모델을 올려서 쓸 것이기 때문에 모델에 이상이 있으면 안됨 
# 경로 변경하지말고 모델 이름만 변경해서 사용할것
pickle.dump(salary_model, open('ML/model/salary_model.pkl','wb'))

# 4. 모델 작동 테스트 (선택사항)
model = pickle.load(open('ML/model/salary_model.pkl','rb'))
prediction = model.predict([[np.array(1.8)]])
output = prediction[0]
print(output) #43002.38816217249
