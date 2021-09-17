# EV charging demand and revenue forecasting for budget planning.


Modeling EV usage and revenue
Forecasting electric vehicle (EV) usage and revenue across public charging stations in Fort Collins to aid in budget planning.

Consulting project for The Data Incubator (TDI) Data Science with the City of Fort Collins Utilities and the EV coordination group.

## Project description

### CONTEXT
I took the initiative to personally reach out to the city of Fort Collins in Colorado because I was particularly interested in how small cities are managing their electic vehicle charging infrastructure during covid. I worked with them to build a data science solution to address their business problem.

Fort Collins received a support grant from the state but has to cover partial costs for maintenance. They wanted me to find out if they are making enough money from the stations to recover expenditures.

### ACTION
I built a solution to forecast Electric Vehicle (EV) revenue across their 8 charging stations and forecast revenue each quarter up to 2025 (grant renewal date).
  
### RESULT
Eventually this app will help in two ways:
- determine if the city is meeting their financial target at the grant renewal date. The forecasting model will be evaluated at each quarter and potentially retrained with new data.
- if not, the application will make a recommendation to change the hourly-rate for charging sessions so that Fort Collins reach their revenue goal by Jan 1, 2025.


**Modeling:** This project applies machine learning to forecast charging station usage and revnue from EV charging stations in the city of Fort Collins. The dataset consists of daily charging sessions across 8 public charging stations. The outcome of interest is a forecasted value for each day in the next 1-3 months.
The following algorithms were compared using walk-forward validation and reporting their 1-month mean-absolute percentage error (MAPE):
- SARIMAX
- XGBoost
- fbProphet


fbProphet was used as the final model as this modeling framework can take into account changes in trend and seasonality due to COVID-related factors (mask mandates, lockdown, etc). The approach achieved a 1-month MAPE of 10%. 


**Web application:** The app deploys the ML model and provides forecasts of revenue and usage from 1-3 months aggregated over all 8 stations. This app serves as a prototype to guide financial planning and as a starting point to understand which stations should be prioritized if budget goals are not being met. Currently, it's deployed using streamlit's github sharing service.

**Please check out my app!**

[App](https://share.streamlit.io/davidfox87/ev_forecasting/main/app.py)


**notebooks:** Jupyter notebooks to walk through data cleaning, EDA, and machine learning pipeline for model evaluation, selection, (and tuning to come). The notebook titled EDA_ML.ipynb shows how i constructed an XGBoost model to forecast 1-30 day revenue and evaluate its MAPE performance on a held-out test set. I also compare the MAPE of XGBoost to fbProphet. On this held-out test set fbprophet performed 3% better. I plan to perform walk-forward validation to get a better sense of the forecast performance of these models. Pricing strategy notebook fits a forecasting model and projects if Fort Collins will meet their financial target before the project grant is up for renewal. It determines if they will have enough money to renew and if not recommends an hourly rate increase for charging sessions.

app: live_app.py contains the source code for Streamlit app, which deploys the machine learning model and provides forcasts on revenue and demand. Requirements.txt provides the required packages to deploy the streamlit app via their github sharing service.
