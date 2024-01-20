import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import copy
import argparse
import joblib
import os


def parse_arguments():
    parser = argparse.ArgumentParser(description="Generate predictions for KPI data.")
    parser.add_argument('csv_file', type=str, help='Path to the input CSV file')
    parser.add_argument('hour', type=int, help='Hour for prediction')
    parser.add_argument('day', type=int, help='Day for prediction')
    parser.add_argument('month', type=int, help='Month for prediction')
    parser.add_argument('year', type=int, help='Year for prediction')
    return parser.parse_args()


def clean_data(data):
    # Drop unnecessary columns and manipulate datetime features
    data.drop(
        ['start_date', 'end_date', 'is_dynamic_grid', 'version', 'start_time', 'end_time', 'data_type', 'kpi_name',
         'status', 'id_coroebus_kpi_measurement_grid', 'id_coroebus_game', 'id_coroebus_kpi_measurement_setup',
         'id_coroebus_measurement', 'end_range'], axis=1, inplace=True)
    data['updated_date_time'] = pd.to_datetime(data['updated_date_time'])
    data.sort_values(by=['updated_date_time'], inplace=True)
    data['hour'] = data['updated_date_time'].dt.hour
    data['day'] = data['updated_date_time'].dt.day
    data['month'] = data['updated_date_time'].dt.month
    data['year'] = data['updated_date_time'].dt.year
    data.drop(['updated_date_time'], axis=1, inplace=True)
    return data


def get_kpi_data(data, kpi_id):
    df = copy.deepcopy(data[data['id_coroebus_kpi'] == kpi_id].drop(['id_coroebus_kpi'], axis=1))
    return df


def train_kpi_data(data):
    X = data.drop(['start_range'], axis=1)
    y = data['start_range']
    rfc = RandomForestRegressor()
    rfc.fit(X, y)
    return rfc


def predict_kpi_data(data, kpi_id, hour, day, month, year):
    df = get_kpi_data(data, kpi_id)
    model = train_kpi_data(df)

    # Create test dataframe with specified datetime features
    test_df = pd.DataFrame({'hour': [hour], 'day': [day], 'month': [month], 'year': [year]})
    value_weightage = df['value_weightage'].unique()
    value_weightage.sort()
    test_df = pd.concat([test_df] * len(value_weightage), ignore_index=True)
    test_df['value_weightage'] = value_weightage
    test_df = test_df[['value_weightage', 'hour', 'day', 'month', 'year']]

    # Make predictions and generate final dataframe
    test_df['start_range'] = model.predict(test_df)
    test_df['start_range'] = test_df['start_range'].round().astype(int)
    test_df['end_range'] = test_df['start_range'].shift(-1).fillna(999).astype(int)
    test_df['kpi_name'] = kpi_dict[kpi_id]
    test_df['id_coroebus_kpi'] = kpi_id
    return test_df


def main():
    args = parse_arguments()
    df = pd.read_csv(args.csv_file)

    global kpi_dict
    kpi_dict = {kpi_id: df[df['id_coroebus_kpi'] == kpi_id]['kpi_name'].unique()[0] for kpi_id in
                df['id_coroebus_kpi'].unique()}

    id_coroebus_game = df['id_coroebus_game'].unique()[0]
    all_kpi_predictions = []

    cleaned_data = clean_data(df)

    for kpi_id in df['id_coroebus_kpi'].unique():
        prediction_df = predict_kpi_data(cleaned_data, kpi_id, args.hour, args.day, args.month, args.year)
        all_kpi_predictions.append(prediction_df)

    final_df = pd.concat(all_kpi_predictions, ignore_index=True)
    final_df['datetime'] = pd.to_datetime(final_df[['year', 'month', 'day', 'hour']])
    final_df['id_coroebus_game'] = id_coroebus_game
    final_df['updated_date_time'] = pd.to_datetime('now').strftime('%Y-%m-%d %H:%M:%S')
    final_df['id_coroebus_prediction'] = np.arange(len(final_df))
    final_df = final_df[['id_coroebus_prediction', 'id_coroebus_game', 'id_coroebus_kpi', 'datetime', 'kpi_name',
                         'start_range', 'end_range', 'updated_date_time']]
    final_df.to_csv('predictions.csv', index=False)
    print('Predictions saved to predictions.csv')


if __name__ == "__main__":
    main()
