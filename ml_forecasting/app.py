from models.ModelRegistry import ModelRegistry

import json

TRENDS_LIST = ['gentle_drift_noise', 'gradual_steady_increase', 'profit_linked', 'proportional_to_sales',
          'rate_cycle_rise_ease', 'sales_seasonal_cycle', 'seasonal_with_short_hump']

TREND_TO_MODEL_MAP = {
    'gentle_drift_noise': 'sarimax',
    'gradual_steady_increase': 'autoets',
    'profit_linked': 'nbeats',
    'proportional_to_sales': 'lstm',
    'rate_cycle_rise_ease': 'autoets',
    'sales_seasonal_cycle': 'nbeats',
    'seasonal_with_short_hump': 'sarimax'
}

MODEL_TO_WEIGHT_EXTENSION_TYPE_MAP = {
    'sarimax': 'pkl',
    'autoets': 'json',
    'lstm': 'pt',
    'nbeats': 'ckpt'
}

for trend in TRENDS_LIST:
    # INSTANTIATE UNFITTED MODEL OBJECT
    model_type = TREND_TO_MODEL_MAP[trend]

    train_model = ModelRegistry.create(model_type)

    # PULL FROM DB
    def getPNLEntriesByTrend(trend):  # Substitute using json data for DB Retrieval
        try:
            with open('data/train/data.json', 'r') as file:
                data = json.load(file)
            print('JSON data loaded from file:')
            print(data)
            print(f'Type of loaded data: {type(data)}')
        except FileNotFoundError:
            print(f'Error: The file {data.json} was not found.')
        except json.JSONDecodeError:
            print('Error: Failed to decode JSON from the file. Check for malformed JSON.')
        return data

    training_data = getPNLEntriesByTrend(trend)

    # TRAIN MODEL
    train_model.train(data=training_data, input_size=12,
                      output_size=3, epochs=50)

    # SAVE WEIGHTS
    weight_extension_type = MODEL_TO_WEIGHT_EXTENSION_TYPE_MAP[model_type]
    train_model.save(f'weights/{trend}/weight.{weight_extension_type}')

    # FORECAST
    pred_model = ModelRegistry.load_model(
        model_type, f'weights/{trend}/weight.{weight_extension_type}')
    
    for pnl_data_row in training_data:
        if pnl_data_row == "date":
            continue
        context_data = training_data[pnl_data_row][-12:]  # Get last 12 data

        predictions = pred_model.predict(
            series_name=pnl_data_row,
            steps=3,
            last_values=context_data
        )

        # UPDATE DB
        push_preds_to_DB = "unfinished"
        print(f'Predictions for\nTrend: {trend}, Values: {predictions}')
