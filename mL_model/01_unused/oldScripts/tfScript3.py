import tensorflow as tf
import tensorflow_decision_forests as tfdf
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Define feature classifications and mappings
quality_mapping = {
        'Ex': 5,
        'Gd': 4,
        'TA': 3,
        'Fa': 2,
        'Po': 1,
    }
quality_features = ['ExterQual', 'ExterCond', 'HeatingQC', 'KitchenQual']
col_keep_mode_impute = ['MSZoning', 'Utilities', 'Electrical', 'Exterior1st', 'Exterior2nd', 'KitchenQual', 'Functional', 'SaleType']
col_keep_zero_fill = ['BsmtFinSF1', 'BsmtFinSF2', 'BsmtUnfSF', 'TotalBsmtSF',
                          'BsmtFullBath', 'BsmtHalfBath', 'GarageCars', 'GarageArea']
# Handle missing values
def handle_missing_values(df):
    missing_data = df.isnull().sum()
    cols_to_drop = missing_data[missing_data > 5].index
    print("cols to drop: ", cols_to_drop)
    cols_to_keep = missing_data[(missing_data > 0) & (missing_data <= 5)].index
    print("cols to keep: ", cols_to_keep)
    df = df.drop(columns=cols_to_drop)

    for col in cols_to_keep:
        if col in col_keep_mode_impute:
            df[col] = df[col].fillna(df[col].mode()[0])
        elif col in col_keep_zero_fill:
            df[col] = df[col].fillna(0)
        else:
            df[col] = df[col].fillna(df[col].mean())

    print('Missing values left:', df.isnull().sum().max())
    return df

# Feature engineering
def engineer_features(df):
    df['Age'] = df['YrSold'] - df['YearBuilt']
    df['RemodAge'] = df['YrSold'] - df['YearRemodAdd']
    
    return df

def convert_to_numerical(df):
    for feature in quality_features:
        df[feature] = df[feature].map(quality_mapping)

    # Convert remaining categorical variables to numerical using Label Encoding
    label_encoders = {}
    categorical_cols = df.select_dtypes(include=['object']).columns

    for col in categorical_cols:
        label_encoders[col] = LabelEncoder()
        df[col] = label_encoders[col].fit_transform(df[col])
    return df

# LOAD TRAINING DATA #
train_fp = "train.csv"
train_df = pd.read_csv(train_fp)

# handle missing values
train_df = handle_missing_values(train_df)
  
# Feature engineering
train_df = engineer_features(train_df)

# Convert categorical features to numerical
train_df = convert_to_numerical(train_df)

# Drop Id and separate features and target vars
X = train_df.drop(['SalePrice', 'Id'], axis=1)
y = train_df['SalePrice']

# Normalize numerical features
scaler = StandardScaler()
numerical_features = X.select_dtypes(include=['int64', 'float64']).columns
X[numerical_features] = scaler.fit_transform(X[numerical_features])


# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=10)

print(f"{len(X_train)} examples in training, {len(X_test)} examples in testing.")

# Combine X and y into a single DataFrame for training and testing
train_dataset = pd.concat([X_train, y_train], axis=1)
test_dataset = pd.concat([X_test, y_test], axis=1)

# Convert to TensorFlow dataset
train_tf_dataset = tfdf.keras.pd_dataframe_to_tf_dataset(train_dataset, label="SalePrice", task=tfdf.keras.Task.REGRESSION)
test_tf_dataset = tfdf.keras.pd_dataframe_to_tf_dataset(test_dataset, label="SalePrice", task=tfdf.keras.Task.REGRESSION)

import optuna

def objective(trial):
    # Define hyperparameters to optimize
    num_trees = trial.suggest_int('num_trees', 100, 2000)
    max_depth = trial.suggest_int('max_depth', 3, 50)
    
    # Create and train model with these hyperparameters
    model = tfdf.keras.RandomForestModel(
        task=tfdf.keras.Task.REGRESSION,
        num_trees=num_trees,
        max_depth=max_depth
    )
    model.fit(train_tf_dataset)
    
    # Evaluate model
    y_pred = model.predict(test_tf_dataset)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    
    return rmse

# Create a study object and optimize the objective function
study = optuna.create_study(direction='minimize')
study.optimize(objective, n_trials=100)

# Print the best parameters
print('Best trial:')
trial = study.best_trial
print('  Value: ', trial.value)
print('  Params: ')
for key, value in trial.params.items():
    print('    {}: {}'.format(key, value))
    
# # Define the model
# model = tfdf.keras.RandomForestModel(task=tfdf.keras.Task.REGRESSION, num_trees=1000)
# model.compile(metrics=["mse"])

# # Train the model
# model.fit(train_tf_dataset)
# y_pred = model.predict(test_tf_dataset)
# rmse = np.sqrt(mean_squared_error(y_test, y_pred))
# print("RMSE:", rmse)

# # Load test data
# test_file_path = "test.csv"
# test_data = pd.read_csv(test_file_path)

# # Handle missing values in test data
# test_data = handle_missing_values(test_data)

# # Feature engineering
# test_data = engineer_features(test_data)

# # Convert categorical features to numerical
# test_data = convert_to_numerical(test_data)

# # Drop Id
# X_test_final = test_data.drop('Id', axis=1)
# test_ids = test_data['Id']

# # Normalize numerical features
# X_test_final[numerical_features] = scaler.transform(X_test_final[numerical_features])

# # Convert to TensorFlow dataset
# test_tf_final_dataset = tfdf.keras.pd_dataframe_to_tf_dataset(X_test_final, task=tfdf.keras.Task.REGRESSION)

# # Make predictions
# preds = model.predict(test_tf_final_dataset)

# # Create submission dataframe
# output = pd.DataFrame({'Id': test_ids, 'SalePrice': preds.squeeze()})

# print(output.head())

# # Save to csv
# output.to_csv('submissionTf3.csv', index=False)
# print('saved to "submissionTf3.csv"')