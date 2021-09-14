# EV charging demand and revenue forecasting for budget planning.


Modeling EV usage and revenue
Forecasting electric vehicle (EV) usage and revenue across public charging stations in Fort Collins to aid in budget planning.

Consulting project for The Data Incubator Data Science with the City of Fort Collins Utilities and the EV coordination group.

## Project description

**Modeling:** This project applies machine learning to forecast charging station usage and revnue from EV charging stations in the city of Fort Collins. The dataset consists of daily charging sessions across 8 public charging stations. The outcome of interest is a forecasted value for each day in the next 1-3 months.
The following algorithms were compared using walk-forward validation and reporting their 1-month mean-absolute percentage error (MAPE):
- SARIMAX
- XGBoost
- fbProphet

fbProphet was used as the final model as this modeling framework can take into account changes in trend and seasonality due to COVID-related factors (mask mandates, lockdown, etc). The approach achieved a 1-month MAPE of 10%. 

**Web application:** The app deploys the ML model and provides forecasts of revenue and usage from 1-3 months aggregated over all 8 stations. This app serves as a prototype to guide financial planning and as a starting point to understand which stations should be prioritized if budget goals are not being met. Currently, it's deployed using streamlit's github sharing service.

**Please check out my app!**

[App](https://share.streamlit.io/davidfox87/ev_forecasting/main/app.py)


n**otebooks:** Jupyter notebooks to walk through data cleaning, EDA, and machine learning pipeline for model evaluation, selection, and tuning.

app: live_app.py contains the source code for Streamlit app, which deploys the machine learning model and provides forcasts on revenue and demand. Requirements.txt provides the required packages to deploy the streamlit app via their github sharing service.
