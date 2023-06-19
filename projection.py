import csv
import pandas as pd
from sklearn.linear_model import LinearRegression

df = pd.read_csv('NBA player 2020-2021.csv')

per = df.loc[:, ['Player', 'G', 'PTS', 'TRB', 'AST', 'STL',
                 'BLK', 'TOV', 'FGA', 'FG', 'FTA', 'FT', '3PA', '3P']]
per.loc[:, 'PER'] = (
    (per['PTS']
     + per['TRB']
     + per['AST']
     + per['STL']
     + per['BLK']
     - (per['FGA'] - per['FG'])
     - (per['FTA'] - per['FT'])
     - per['TOV'])
    / per['G']
)

per['PER'] = per['PER'].round(2)

per.to_csv('pure_efficiency_stats_20_21.csv', index=False)

df_2 = pd.read_csv('NBA player 2021-2022.csv')

per_2 = df_2.loc[:, ['Player', 'G', 'PTS', 'TRB', 'AST',
                     'STL', 'BLK', 'TOV', 'FGA', 'FG', 'FTA', 'FT', '3PA', '3P']]
per_2.loc[:, 'PER'] = (
    (per_2['PTS']
     + per_2['TRB']
     + per_2['AST']
     + per_2['STL']
     + per_2['BLK']
     - (per_2['FGA'] - per_2['FG'])
     - (per_2['FTA'] - per_2['FT'])
     - per_2['TOV'])
    / per_2['G']
)

per_2['PER'] = per_2['PER'].round(2)

per_2.to_csv('pure_efficiency_stats_21_22.csv', index=False)

df_3 = pd.read_csv('NBA player 2022-2023.csv')

per_3 = df_3.loc[:, ['Player', 'G', 'PTS', 'TRB', 'AST',
                     'STL', 'BLK', 'TOV', 'FGA', 'FG', 'FTA', 'FT', '3PA', '3P']]
per_3.loc[:, 'PER'] = (
    (per_3['PTS']
     + per_3['TRB']
     + per_3['AST']
     + per_3['STL']
     + per_3['BLK']
     - (per_3['FGA'] - per_3['FG'])
     - (per_3['FTA'] - per_3['FT'])
     - per_3['TOV'])
    / per_3['G']
)

per_3['PER'] = per_3['PER'].round(2)

per_3.to_csv('pure_efficiency_stats_22_23.csv', index=False)

train_data_1 = pd.read_csv('pure_efficiency_stats_20_21.csv')
train_data_2 = pd.read_csv('pure_efficiency_stats_21_22.csv')

train_data = pd.concat([train_data_1, train_data_2], ignore_index=True)

test_data = pd.read_csv('pure_efficiency_stats_22_23.csv')

train_data = train_data.drop('Player', axis=1)
test_data = test_data.drop('Player', axis=1)

X_train = train_data.drop('PER', axis=1)
y_train = train_data['PER']

X_test = test_data.drop('PER', axis=1)
y_test = test_data['PER']

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

comparison = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
print(comparison)

comparison.to_csv('final_results.csv', index=False)


with open('final_results.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)
    differences = [float(row[1]) - float(row[0]) for row in reader]

modified_differences = [diff + 1.0 for diff in differences]

with open('pure_efficiency_stats_22_23.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    header = next(reader)
    data = list(reader)

    g_column_index = header.index('G')

    for i, row in enumerate(data):
        for j in range(len(row)):
            if j != g_column_index and j != 0:
                row[j] = round(float(row[j]) * modified_differences[i], 2)

with open('updated_per_stats_22_23.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(data)
