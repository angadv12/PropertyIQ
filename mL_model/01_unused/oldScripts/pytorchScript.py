import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import optuna

# define feature classifications
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

# handle missing values
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

# feature engineering
def engineer_features(df):
    df['Age'] = df['YrSold'] - df['YearBuilt']
    df['RemodAge'] = df['YrSold'] - df['YearRemodAdd']
    
    return df

# convert categorical features to numerical
def convert_to_numerical(df):
    for feature in quality_features:
        df[feature] = df[feature].map(quality_mapping)

    # convert remaining categorical using Label Encoding
    label_encoders = {}
    categorical_cols = df.select_dtypes(include=['object']).columns

    for col in categorical_cols:
        label_encoders[col] = LabelEncoder()
        df[col] = label_encoders[col].fit_transform(df[col])
    return df

# Load and preprocess data
data = pd.read_csv('train.csv')
data = handle_missing_values(data)
data = engineer_features(data)
data = convert_to_numerical(data)

# Separate features and target
X = data.drop(['SalePrice', 'Id'], axis=1)
y = data['SalePrice']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Convert to PyTorch tensors
X_train_tensor = torch.FloatTensor(X_train_scaled)
y_train_tensor = torch.FloatTensor(y_train.values).reshape(-1, 1)
X_test_tensor = torch.FloatTensor(X_test_scaled)
y_test_tensor = torch.FloatTensor(y_test.values).reshape(-1, 1)

# Define the neural network
class HousePriceNet(nn.Module):
    def __init__(self, input_dim, hidden_layers, dropout_rate):
        super(HousePriceNet, self).__init__()
        layers = []
        prev_dim = input_dim
        for hidden_dim in hidden_layers:
            layers.append(nn.Linear(prev_dim, hidden_dim))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(dropout_rate))
            prev_dim = hidden_dim
        layers.append(nn.Linear(prev_dim, 1))
        self.model = nn.Sequential(*layers)
        
    def forward(self, x):
        return self.model(x)


def objective(trial):
    # Define hyperparameters to optimize
    n_layers = trial.suggest_int('n_layers', 1, 5)
    hidden_layers = [trial.suggest_int(f'hidden_layer_{i}', 16, 256) for i in range(n_layers)]
    dropout_rate = trial.suggest_float('dropout_rate', 0.1, 0.5)
    learning_rate = trial.suggest_float('learning_rate', 1e-5, 1e-1, log=True)
    batch_size = trial.suggest_categorical('batch_size', [16, 32, 64, 128])
    
    # Initialize the model
    input_dim = X_train_scaled.shape[1]
    model = HousePriceNet(input_dim, hidden_layers, dropout_rate)
    
    # Define loss function and optimizer
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    
    # Training loop
    num_epochs = 100
    
    for epoch in range(num_epochs):
        model.train()
        for i in range(0, len(X_train_tensor), batch_size):
            batch_X = X_train_tensor[i:i+batch_size]
            batch_y = y_train_tensor[i:i+batch_size]
            
            outputs = model(batch_X)
            loss = criterion(outputs, batch_y)
            
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
    
    # Evaluation
    model.eval()
    with torch.no_grad():
        y_pred = model(X_test_tensor)
        rmse = torch.sqrt(criterion(y_pred, y_test_tensor))
    
    return rmse.item()

# Create a study object and optimize the objective function
study = optuna.create_study(direction='minimize')
study.optimize(objective, n_trials=100)

# Print the best parameters and the best value
print('Best trial:')
trial = study.best_trial
print('  Value: ', trial.value)
print('  Params: ')
for key, value in trial.params.items():
    print('    {}: {}'.format(key, value))

# Train the final model with the best parameters
best_params = study.best_params
input_dim = X_train_scaled.shape[1]
best_model = HousePriceNet(input_dim, 
                           [best_params[f'hidden_layer_{i}'] for i in range(best_params['n_layers'])],
                           best_params['dropout_rate'])

criterion = nn.MSELoss()
optimizer = optim.Adam(best_model.parameters(), lr=best_params['learning_rate'])

num_epochs = 100
batch_size = best_params['batch_size']

for epoch in range(num_epochs):
    best_model.train()
    for i in range(0, len(X_train_tensor), batch_size):
        batch_X = X_train_tensor[i:i+batch_size]
        batch_y = y_train_tensor[i:i+batch_size]
        
        outputs = best_model(batch_X)
        loss = criterion(outputs, batch_y)
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

# Final evaluation
best_model.eval()
with torch.no_grad():
    y_pred = best_model(X_test_tensor).numpy()
    y_true = y_test_tensor.numpy()

    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_true, y_pred)

    print(f'MAE: {mae:.4f}')
    print(f'MSE: {mse:.4f}')
    print(f'RMSE: {rmse:.4f}')
    print(f'R²: {r2:.4f}')

# Make predictions on test data
test_data = pd.read_csv('test.csv')
test_data = handle_missing_values(test_data)
test_data = engineer_features(test_data)
test_data = convert_to_numerical(test_data)

X_test_final = test_data.drop('Id', axis=1)
test_ids = test_data['Id']

X_test_final_scaled = scaler.transform(X_test_final)
X_test_final_tensor = torch.FloatTensor(X_test_final_scaled)

best_model.eval()
with torch.no_grad():
    preds = best_model(X_test_final_tensor).numpy()

# Create submission dataframe
output = pd.DataFrame({'Id': test_ids, 'SalePrice': preds.flatten()})
print(output.head())

# Save to csv
output.to_csv('submissionPyTorch.csv', index=False)
print('Saved to "submissionPyTorch.csv"')