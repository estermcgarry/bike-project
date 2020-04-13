from sklearn.externals import joblib 
  
# Load the model from the file 
model_from_joblib = joblib.load('model.pkl')  
  
X_test=[[0,0,0,1,0,0,1,0]]

# Use the loaded model to make predictions 
model_from_joblib.predict(X_test) 