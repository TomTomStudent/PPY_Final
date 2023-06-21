from matplotlib.widgets import RadioButtons
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt


def file_output_per(input_file, output_file):
    df = pd.read_csv(input_file)
    grouped_data = df.groupby('Player').sum()
    sorted_data = grouped_data.sort_values('Player').reset_index()
    rounded_data = sorted_data.round(2)

    per = rounded_data.loc[:,
                           ['Player', 'Age', 'G', 'GS', 'MP', 'PTS', 'TRB', 'AST', 'STL',
                            'BLK', 'TOV', 'FGA', 'FG', 'FTA', 'FT', '3PA', '3P', 'PF']]

    per['PER'] = ((per['PTS']
                   + per['TRB']
                   + per['AST']
                   + per['STL']
                   + per['BLK']
                   - (per['FGA'] - per['FG'])
                   - (per['FTA'] - per['FT'])
                   - per['TOV']) / per['G'])

    per['PER'] = per['PER'].round(2)
    per.to_csv(output_file, index=False)


file_output_per('NBA player 2020-2021.csv', 'pure_efficiency_stats_20_21.csv')
file_output_per('NBA player 2021-2022.csv', 'pure_efficiency_stats_21_22.csv')
file_output_per('NBA player 2022-2023.csv', 'pure_efficiency_stats_22_23.csv')


def player_filter(data_set_1_path, data_set_2_path, data_set_3_path):
    df_1 = pd.read_csv(data_set_1_path)
    df_2 = pd.read_csv(data_set_2_path)
    df_3 = pd.read_csv(data_set_3_path)

    common_players = set(df_1['Player']).intersection(
        df_2['Player']).intersection(df_3['Player'])

    filtered_df_1 = df_1[df_1['Player'].isin(common_players)]
    filtered_df_2 = df_2[df_2['Player'].isin(common_players)]
    filtered_df_3 = df_3[df_3['Player'].isin(common_players)]

    return filtered_df_1, filtered_df_2, filtered_df_3


filtered_data_1, filtered_data_2, filtered_data_3 = player_filter('pure_efficiency_stats_20_21.csv',
                                                                  'pure_efficiency_stats_21_22.csv', 'pure_efficiency_stats_22_23.csv')

filtered_data_1.to_csv('pure_efficiency_stats_20_21_filtered.csv', index=False)
filtered_data_2.to_csv('pure_efficiency_stats_21_22_filtered.csv', index=False)
filtered_data_3.to_csv('pure_efficiency_stats_22_23_filtered.csv', index=False)

data_1 = pd.read_csv('pure_efficiency_stats_20_21_filtered.csv')
X_train = data_1.iloc[:, 1:-1].values

data_2 = pd.read_csv('pure_efficiency_stats_21_22_filtered.csv')
X_test = data_2.iloc[:, 1:-1].values
y_train = data_2.iloc[:, 18].values

df = pd.DataFrame(X_train)
df['PER'] = y_train

correlation_matrix = df.corr()

# Fig 1
# plt.figure(figsize=(10, 8))
# sns.heatmap(correlation_matrix, annot=True, cmap='flare', linewidths=0.5)
# plt.title('Correlation Heatmap')
# plt.show()


def backward_elimination(X, y, significance_level=0.05):
    num_features = X.shape[1]
    selected_indices = np.arange(num_features)

    for i in range(num_features):
        model = sm.OLS(y, X).fit()
        max_p_value = max(model.pvalues)

        if max_p_value > significance_level:
            max_p_value_index = np.argmax(model.pvalues)
            X = np.delete(X, max_p_value_index, axis=1)
            selected_indices = np.delete(selected_indices, max_p_value_index)

        else:
            break
    return selected_indices


selected_variables = backward_elimination(X_train, y_train)

X_train_selected = X_train[:, selected_variables]
X_test_selected = X_test[:, selected_variables]

# print(X_test_selected)
# print()
# print(X_test_selected)


regressor_rf = RandomForestRegressor()

regressor_rf.fit(X_train_selected, y_train)

# setting an intercept for RF not std. approach
# introduces bias and changes behavior of RF
# regressor.estimators_[-1].tree_.value[0] = [[y_train.mean()]]

y_pred_m_1 = regressor_rf.predict(X_test_selected)

comp_data = pd.read_csv('pure_efficiency_stats_22_23_filtered.csv')
comp = comp_data['PER'].values

score_m_1 = r2_score(comp, y_pred_m_1) * 100
#print('R2 Score =', score_m_1.round(5), '%')

# Fig 2
# plt.scatter(y_pred_m_1, comp)
# plt.xlabel('Predicted PER')
# plt.ylabel('Actual PER')
# plt.title('Comparison of Predicted PER vs Actual PER')
# plt.show()


selected_variables_m_2 = backward_elimination(X_train, y_train)

X_train_selected_m_2 = X_train[:, selected_variables_m_2]
X_test_selected_m_2 = X_test[:, selected_variables_m_2]

regressor_lr = LinearRegression()

regressor_lr.fit(X_train_selected_m_2, y_train)

y_pred_m_2 = regressor_lr.predict(X_test_selected_m_2)

score_m_2 = r2_score(comp, y_pred_m_2) * 100
#print('R2 Score =', score_m_2.round(5), '%')

# Fig 3
# plt.scatter(y_pred_m_2, comp)
# plt.xlabel('Predicted PER')
# plt.ylabel('Actual PER')
# plt.title('Comparison of Predicted PER vs Actual PER')
# plt.show()


def backward_elimination_2(X, y, significance_level=0.1):
    num_features = X.shape[1]
    selected_indices = np.arange(num_features)

    for i in range(num_features):
        model = sm.OLS(y, X).fit()
        max_p_value = max(model.pvalues)

        if max_p_value > significance_level:
            max_p_value_index = np.argmax(model.pvalues)
            X = np.delete(X, max_p_value_index, axis=1)
            selected_indices = np.delete(selected_indices, max_p_value_index)

        else:
            break
    return selected_indices


selected_variables_m_3 = backward_elimination_2(X_train, y_train)

X_train_selected_m_3 = X_train[:, selected_variables_m_3]
X_test_selected_m_3 = X_test[:, selected_variables_m_3]

# print(X_test_selected_m_3)
# print()
# print(X_test_selected_m_3)

regressor_rf = RandomForestRegressor()

regressor_rf.fit(X_train_selected_m_3, y_train)

y_pred_m_3 = regressor_rf.predict(X_test_selected_m_3)

score_m_3 = r2_score(comp, y_pred_m_3) * 100
#print('R2 Score =', score_m_3.round(5), '%')

# Fig 4
# plt.scatter(y_pred_m_3, comp)
# plt.xlabel('Predicted PER')
# plt.ylabel('Actual PER')
# plt.title('Comparison of Predicted PER vs Actual PER')
# plt.show()

selected_variables_m_4 = backward_elimination_2(X_train, y_train)

X_train_selected_m_4 = X_train[:, selected_variables_m_4]
X_test_selected_m_4 = X_test[:, selected_variables_m_4]

regressor_lr = LinearRegression()

regressor_lr.fit(X_train_selected_m_4, y_train)

y_pred_m_4 = regressor_lr.predict(X_test_selected_m_4)

score_m_4 = r2_score(comp, y_pred_m_4) * 100
#print('R2 Score =', score_m_4.round(5), '%')

# Fig 5
# plt.scatter(y_pred_m_4, comp)
# plt.xlabel('Predicted PER')
# plt.ylabel('Actual PER')
# plt.title('Comparison of Predicted PER vs Actual PER')
# plt.show()


figure_labels = ['Model 1', 'Model 2', 'Model 3', 'Model 4']
current_figure_index = 0


def heatmap_display():
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True,
                cmap='flare', linewidths=0.5, ax=ax)
    ax.set_title('Correlation Heatmap')
    plt.show()


def models_display():
    global current_figure_index

    fig, ax = plt.subplots(figsize=(8, 6))
    y_preds = [y_pred_m_1, y_pred_m_2, y_pred_m_3, y_pred_m_4]
    label = figure_labels[current_figure_index]
    ax.scatter(y_preds[current_figure_index], comp)
    ax.set_xlabel('Predicted PER')
    ax.set_ylabel('Actual PER')
    ax.set_title(f'Comparison of Predicted PER vs Actual PER ({label})')

    def on_radio_button_clicked(label):
        global current_figure_index
        current_figure_index = figure_labels.index(label)
        ax.clear()
        label = figure_labels[current_figure_index]
        ax.scatter(y_preds[current_figure_index], comp)
        ax.set_xlabel('Predicted PER')
        ax.set_ylabel('Actual PER')
        ax.set_title(f'Comparison of Predicted PER vs Actual PER ({label})')
        plt.draw()

    ax_radio_buttons = plt.axes([0.1, 0.1, 0.7, 0.1])
    radio_buttons = RadioButtons(ax_radio_buttons, figure_labels)
    radio_buttons.on_clicked(on_radio_button_clicked)

    plt.subplots_adjust(bottom=0.2)
    plt.show()


def findTrue():
    df = pd.DataFrame(
        {'Actual PER': comp, 'Predicited PER': y_pred_m_2, 'Difference': (comp - y_pred_m_2)})
    df.to_csv('final_result_m_2.csv', index=False)


def createSus():
    df_1 = pd.read_csv('pure_efficiency_stats_22_23_filtered.csv', header=0)
    df_2 = pd.read_csv('final_result_m_2.csv', header=0)
    df_1.iloc[:, 4:] = df_1.iloc[:, 4:] + \
        df_1.iloc[:, 4:].multiply(df_2.iloc[:, -1], axis=0)
    df_1.iloc[:, 4:] = df_1.iloc[:, 4:].round(2)
    df_1.iloc[:, -1] = df_2.iloc[:, 1].round(2)
    df_1.to_csv('m_2_predicted_player_stats_22_23.csv', index=0)
