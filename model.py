# Importing necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report ,roc_auc_score, roc_curve
from sklearn.metrics import precision_score, recall_score

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from imblearn.over_sampling import SMOTE

#Load dataset
df = pd.read_csv('Clean_Dataset.csv')

#To view first 5 rows of the dataset
df.head()
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder, StandardScaler
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import StratifiedShuffleSplit
# Load dataset
file_path = "Clean_Dataset.csv"
df = pd.read_csv(file_path)
# Drop the unwanted column
df = df.drop(columns=['Unnamed: 26'], errors='ignore')
# Handle categorical variables using Label Encoding/One-Hot Encoding
le = LabelEncoder()
# Encoding Gender and OTT Subscription as binary
df['GENDER'] = le.fit_transform(df['GENDER']) # 0 for Female, 1 for Male
df['OTT_SUBSCRIPTION'] = le.fit_transform(df['OTT_SUBSCRIPTION']) # 0 for No, 1 for Yes
# Encoding other categorical variables using One-Hot Encoding
categorical_columns = [
'SCHOOL_SECTION', 'PERSONAL_SMARTPHONE', 'TELEVISION_SCREEN_TIME',
'TELEVISION_CONTENT',
'SOCIAL_MEDIA_PLATFORM', 'PHONE_SCREEN_TIME', 'SOCIAL_MEDIA_CONTENT',
'MOBILE_GAMES',
'SLEEPING_TIME', 'WAKEUP_TIME', 'OUTDOOR_SPORTS', 'SLEEP_ISSUES',
'DISTRACTION_DURING_SLEEPING',
'EYES_STRAINED', 'SPECTACLES', 'SPECTACLE_NUMBER', 'RESTLESS',
'DISTRACTION_DURING_SEARCHING',
'CONCENTRATION', 'DEPRESSED', 'ANXIETY', 'BEHAVIOURAL_CHANGES',
'REPLICATE_SOCIAL_MEDIA'
]

df = pd.get_dummies(df, columns=categorical_columns)
# Create the target variable based on the three columns DEPRESSED_High,
# DEPRESSED_Moderate, DEPRESSED_Low

def create_depression_label(row):
    if row['DEPRESSED_High'] == 1:
        return 'High'
    elif row['DEPRESSED_Moderate'] == 1:
        return 'Moderate'
    elif row['DEPRESSED_Low'] == 1:
        return 'Low'
    else:
        return 'Unknown'
df['Depression'] = df.apply(create_depression_label, axis=1)
# Drop the individual DEPRESSED columns after creating the target variable
df.drop(['DEPRESSED_High', 'DEPRESSED_Moderate', 'DEPRESSED_Low'], axis=1,
inplace=True)
# Save the trained feature names before applying SMOTE
joblib.dump(df.drop(['Depression'], axis=1).columns.tolist(), "TRAINED_FEATURES.pkl")
# Handling Imbalanced Data using SMOTE
X = df.drop(['Depression'], axis=1)
y = df['Depression']
# Check class distribution
print("\nClass Distribution Before SMOTE:")
print(y.value_counts())
# Apply SMOTE for multi-class classification
smote = SMOTE(sampling_strategy='auto', random_state=42)
X_sm, y_sm = smote.fit_resample(X, y)
# Check class distribution after SMOTE
print("\nClass Distribution After SMOTE:")
print(pd.Series(y_sm).value_counts())
# Data Preprocessing (Scaling)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_sm)
# Create a stratified split with 80% training and 20% testing
stratified_split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
train_index, test_index = next(stratified_split.split(X_scaled, y_sm))
# Create training and testing sets
X_train, X_test = X_scaled[train_index], X_scaled[test_index]
y_train, y_test = y_sm[train_index], y_sm[test_index]
# Logistic Regression for multi-class classification
log_reg = LogisticRegression(multi_class='multinomial', solver='lbfgs')
log_reg.fit(X_train, y_train)
y_pred_logreg = log_reg.predict(X_test)
# Decision Tree Classifier
dt = DecisionTreeClassifier()
dt.fit(X_train, y_train)
y_pred_dt = dt.predict(X_test)
# Random Forest Classifier
rf = RandomForestClassifier()
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)
# Support Vector Machine (SVM) for multi-class classification
svc = SVC(probability=True)
svc.fit(X_train, y_train)
y_pred_svc = svc.predict(X_test)
# Function to evaluate model performance
def evaluate_model(y_test, y_pred, model_name):
    print(f"\n{model_name} Performance Metrics:")
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted') # For multi-class
    recall = recall_score(y_test, y_pred, average='weighted') # For multi-class
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
# Evaluate all models
evaluate_model(y_test, y_pred_logreg, "Logistic Regression")
evaluate_model(y_test, y_pred_dt, "Decision Tree")
evaluate_model(y_test, y_pred_rf, "Random Forest")
evaluate_model(y_test, y_pred_svc, "SVM")

import joblib
from sklearn.ensemble import RandomForestClassifier
# Sample dataset (replace with actual training data)
X_train, y_train = X_scaled[train_index], y_sm[train_index] # Load your dataset here
# Train the model
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
# Save the trained model
joblib.dump(rf, "RANDOM_FOREST_MODEL.pkl")
print("Model saved successfully!")

import joblib
from sklearn.preprocessing import StandardScaler # Change if you used MinMaxScaler
# Sample dataset (replace with actual training data)
X_train = X_scaled[train_index] # Load your dataset here
# Train and save the scaler
scaler = StandardScaler()
scaler.fit(X_train) # Fit on training data
# Save the scaler
joblib.dump(scaler, "SCALER.pkl")
print("Scaler saved successfully!")
import joblib
import pandas as pd
# Load the trained model and scaler
rf_model = joblib.load("RANDOM_FOREST_MODEL.pkl")
scaler = joblib.load("SCALER.pkl")
# Define the categorical feature names based on training data encoding
categorical_features = [
'SCHOOL_SECTION', 'PERSONAL_SMARTPHONE', 'TELEVISION_SCREEN_TIME',
'TELEVISION_CONTENT',
'SOCIAL_MEDIA_PLATFORM', 'PHONE_SCREEN_TIME', 'SOCIAL_MEDIA_CONTENT',
'MOBILE_GAMES',
'SLEEPING_TIME', 'WAKEUP_TIME', 'OUTDOOR_SPORTS', 'SLEEP_ISSUES',
'DISTRACTION_DURING_SLEEPING',
'EYES_STRAINED', 'SPECTACLES', 'SPECTACLE_NUMBER', 'RESTLESS',
'DISTRACTION_DURING_SEARCHING',
'CONCENTARTION', 'ANXIETY', 'BEHAVIOURAL_CHANGES',
'REPLICATE_SOCIAL_MEDIA'
]
# Define user input function
def get_user_input():
    print("\nEnter the following details:")
    # Take user inputs for the specific fields
    age = int(input("AGE (5 to 15 years): "))
    gender = input("GENDER (Male/Female): ")
    ott_subscription = input("OTT Subscription (Yes/No): ")
    # Encode Gender and OTT Subscription
    gender = 1 if gender.lower() == "male" else 0
    ott_subscription = 1 if ott_subscription.lower() == "yes" else 0
    # Collect categorical inputs (user can enter these)
    categorical_values = {}
    
    for feature in categorical_features:
        value = input(f"{feature}: ")
        categorical_values[feature] = value
    # Convert categorical input to one-hot encoding
    input_data = pd.DataFrame([categorical_values])
    # Perform one-hot encoding for categorical features
    input_data = pd.get_dummies(input_data)
    # Load the original feature names from the training dataset
    trained_features = joblib.load("TRAINED_FEATURES.pkl")
    # Ensure the input data matches the trained feature set
    missing_cols = set(trained_features) - set(input_data.columns)
    missing_data = pd.DataFrame(0, index=input_data.index, columns=list(missing_cols)) #
    # Convert set to list
    # Concatenate the missing columns with the input data
    input_data = pd.concat([input_data, missing_data], axis=1)
    # Reorder the columns to match the trained feature set
    input_data = input_data[trained_features] # Reorder columns to match training
    # Only insert AGE, GENDER, and OTT_SUBSCRIPTION if they don't already exist
    if "AGE" not in input_data.columns:
        input_data.insert(0, "AGE", age)
    if "GENDER" not in input_data.columns:
        input_data.insert(1, "GENDER", gender)
    if "OTT_SUBSCRIPTION" not in input_data.columns:
        input_data.insert(2, "OTT_SUBSCRIPTION", ott_subscription)
    return input_data

# Take user input
user_input = get_user_input()
# Scale the user input
user_input_scaled = scaler.transform(user_input)
# Predict the depression level
prediction = rf_model.predict(user_input_scaled)
# Output the result
print("\nPredicted Depression Level:", prediction[0])
