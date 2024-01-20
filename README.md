# KPI Grid Prediction

## Overview

This Python script predicts Key Performance Indicator (KPI) grids for a specified date and time using the RandomForestRegressor algorithm. The predictions are generated based on historical KPI data obtained from the `tbl_coroebus_kpi_measurement_grid` table. The script allows users to specify the hour, day, month, and year for which they want to predict KPI grids.

## Requirements

- Python 3.x
- pandas
- scikit-learn
- argparse
- joblib
- numpy

To install the required dependencies, you can use the provided `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## Usage

1. Run the script with the following command:

   ```bash
   python script_name.py csv_file hour day month year
   ```

   - `csv_file`: Path to the input CSV file containing historical KPI data.
   - `hour`: Hour for prediction.
   - `day`: Day for prediction.
   - `month`: Month for prediction.
   - `year`: Year for prediction.

   Example:

   ```bash
   python script.py data.csv 12 1 6 2023
   ```

2. The script will generate predictions and save the results in a file named `predictions.csv`.

## Input Data

The input data is expected to be in the format of the result obtained from the SQL query:

```sql
select c.*, b.kpi_name 
from tbl_coroebus_kpi as b, tbl_coroebus_kpi_measurement_grid as c
where c.id_coroebus_kpi = b.id_coroebus_kpi and c.id_coroebus_game = 228
```

You can specify any other game id in the query to obtain relevant historical KPI data.

## Output

The script generates predictions for each unique KPI present in the input data. The output file (`predictions.csv`) contains the following columns:

1. **id_coroebus_prediction**: Unique identifier for each prediction.
2. **id_coroebus_game**: Unique identifier for the game associated with the prediction.
3. **id_coroebus_kpi**: Unique identifier for the KPI associated with the prediction.
4. **datetime**: Date and time for which the prediction is made.
5. **kpi_name**: Name of the KPI.
6. **start_range**: Predicted starting range for the KPI grid.
7. **end_range**: Predicted ending range for the KPI grid.
8. **updated_date_time**: Timestamp of when the prediction was generated.

## Sample Predictions

A sample of predictions is available in the `predictions.csv` file, showcasing the predicted KPI grids for the specified date and time.

Feel free to customize the script or query to suit your specific requirements.
