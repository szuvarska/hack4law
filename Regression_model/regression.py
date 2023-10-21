import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

file_path1 = '../Data/decisions_only.csv'

# Read the CSV file into a DataFrame
df1 = pd.read_csv(file_path1, sep=";")
df1 = df1.dropna(subset=['sumOfMoney'])

file_path2 = '../Data/with_uzasadnienie2.csv'

# Read the CSV file into a DataFrame
df2 = pd.read_csv(file_path2, sep=";")
df2 = df2[["id","uzasadnienie"]]

df = pd.merge(df1, df2, on='id', how='inner')

# Save the DataFrame to CSV
df.to_csv('../Data/decisions_with_uzasadnienie.csv', sep=';', encoding='utf-8-sig')

# vectorizer = TfidfVectorizer()
# X = vectorizer.fit_transform(df['uzasadnienie'])
#
# X_train, X_test, y_train, y_test = train_test_split(X, df['sumOfMoney'], test_size=0.2, random_state=42)
#
# model = LinearRegression()
# model.fit(X_train, y_train)
#
# y_pred = model.predict(X_test)
#
# mae = mean_absolute_error(y_test, y_pred)
# mse = mean_squared_error(y_test, y_pred)
# r2 = r2_score(y_test, y_pred)
#
# print(f"MAE: {mae}")
# print(f"MSE: {mse}")
# print(f"R-squared: {r2}")
#
# # Save the model to a file
# joblib.dump(model, 'regression_model.pkl')

