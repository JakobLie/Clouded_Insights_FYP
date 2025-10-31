# Configurations
DICT_OF_TREND_TO_MODEL = {
    "trend_1": "SARIMA",
    "trend_2": "N-BEATS",
    "trend_7": "Holt-Winters"
}

LIST_OF_BU = ["BB1", "BB2", "HQ", "..."]

LIST_OF_PNL_CATEGORIES = "API CALL TO BACKEND"

# Functions
"""
retrieve all PNL entry data from DB
"""
def retrieve_data():
    return

"""
get data fronm the retrieved_data relevant to input trend_name (trend_1, ..., trend_7, static)
"""
def sort_data(trend_name):
    return

"""
generate model weight and write to respective "weights" folder
"""   
def train_model():
    return

"""
push input data into db using backend REST APIs
"""
def push_to_db(forecast_data):
    return

"""
forecasts values then pushes forecast data into DB
"""
def run_model():
    push_to_db(data)
    return

"""
caclualte KPIs from forecasted data and push to DB
"""
def kpi_calc():
    push_to_db(data)
    return

# Retrieve DB data (sqlalchemy)

all_data = retrieve_data()

trend_1_data = sort_data(all_data, "trend_1", "BU(?)")
trend_2_data = sort_data(all_data, "trend_2")
trend_7_data = sort_data(all_data, "trend_7")

# Train and write weights to respective trend folders
weight1 = train_model(DICT_OF_TREND_TO_MODEL["trend1"], "trend_1", trend_1_data)
weight2 = train_model(DICT_OF_TREND_TO_MODEL["trend2"], "trend_2", trend_2_data)
weight7 = train_model(DICT_OF_TREND_TO_MODEL["trend7"], "trend_7", trend_7_data)

# Run and push data into DB

trend_1_57_mth_historical = "SORT ALL_DATA" # Can reuse sort_data function or make another function
trend_2_57_mth_historical = "SORT ALL_DATA"
trend_7_57_mth_historical = "SORT ALL_DATA"

run_trend_1 = run_model(DICT_OF_TREND_TO_MODEL["trend1"], "trend_1", trend_1_57_mth_historical)
run_trend_2 = run_model(DICT_OF_TREND_TO_MODEL["trend1"], "trend_2", trend_2_57_mth_historical)
run_trend_7 = run_model(DICT_OF_TREND_TO_MODEL["trend1"], "trend_7", trend_7_57_mth_historical)

# Calculate KPIs
# Use load data KPI calculation function from backend

# Notification threshols
# based on KPI calculations determine whether to create notiofication ro not
# send email/whatzxapp here??