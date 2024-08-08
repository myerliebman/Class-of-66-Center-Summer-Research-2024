# Runs localtest and calculates the correlation coefficeint and coefficient of determination
# Creates a linear regression model using an 80/20 test and train split and outputs model test data


import pandas as pd

from sklearn.linear_model import LinearRegression

from localtest import differences_kWh, temp_list

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

df = pd.DataFrame({'Energy': differences_kWh,
                   'Temperature': temp_list})

#print(df)

#initiate linear regression model
model = LinearRegression()

#define predictor and response variables
X, y = df[["Temperature"]], df["Energy"]

#fit regression model
model.fit(X, y)

# Calculate R-squared of regression model
r_squared = model.score(X, y)
print(f"\nCoefficient of determination (R^2): {r_squared}")

# Calculate correlation coefficient
r = df['Energy'].corr(df['Temperature'])
print(f"Correlation coefficient (r): {r}")


###Linear Regression Model
print("\nModel Testing Data:")

#Split data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#Create linear regression model
model = LinearRegression()

#Fit model to training data
model.fit(X_train, y_train)

#Make predictions on test data
y_pred = model.predict(X_test)

#Caluclate Mean Squared Error (MSE) and R-squared (R^2)
mse = mean_squared_error(y_test, y_pred)
r_squared = r2_score(y_test, y_pred)

#Display MSE and R^2
print(f'Mean Squared Error (MSE): {mse:.2f}')
print(f'R-squared (R^2): {r_squared:.2f}')
