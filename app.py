from datetime import datetime
from plot import plot_forecast
from bokeh.core.property.color import Color
import streamlit as st
import numpy as np
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Patch, HoverTool, CrosshairTool
from prophet import Prophet
from load_data import load_data
from model import build_model, is_stay_at_home
from plot import plot_forecast


st.set_page_config(layout="wide")

df, model = load_data()

@st.cache(allow_output_mutation=True)
def make_forecast():
    """Takes a name from the selection and makes a forecast plot with specified forecast horizon."""

    future = model.make_future_dataframe(periods=1500)
    future['is_stay_at_home'] = future['ds'].apply(is_stay_at_home)
    future['is_not_stay_at_home'] = ~future['ds'].apply(is_stay_at_home)
    forecast = model.predict(future)

    forecast['cumsum_revenue_prediction'] = forecast['yhat'].cumsum()

    forecast_quarter = (forecast 
                            .set_index('ds') 
                            .resample('3M').asfreq().pad()['cumsum_revenue_prediction'][:"2025-04-01"] 
                            .reset_index() 
    )

    forecast_quarter = (forecast_quarter
                                    .assign(ds=lambda df: pd.to_datetime(df["ds"]))
                                    .assign(ds=lambda df: df["ds"].dt.strftime('%Y-%m-%d'))
                                    .set_index('ds')
                        ).T

    # print(forecast.tail())
    time_to_target = forecast[forecast['cumsum_revenue_prediction'] >=  62077]['ds']
    rel_target_date =  time_to_target - datetime(2025, 1, 1)
    # print(rel_target_date.iloc[0])
    return forecast_quarter, plot_forecast(df, forecast), rel_target_date.iloc[0].days



st.title("Forecasting Revenue from Electric Vehicle Charging Stations")
st.markdown("# For the City of Fort Collins, CO")
st.markdown("#")

def header(url):
     st.markdown(f'<p style="color:#FF0000;font-size:24px;">{url}</p>', unsafe_allow_html=True)

forecast_quarter_df, fig_, time_to_target = make_forecast()
st.markdown("""An effort to expand public electric vehicle (EV) charging 
infrastructure was made by Fort Collins, CO.
As such 8 stations were commisioned in late June 2020. 
This project was partially funded by the state with a 5-year Charge Ahead Colorado grant. 
The upfront costs to Fort Collins utilities for this grant period, which covers payment processing 
and maintenance totals $21,077. Furthermore, it is estimated that the cost to renew the grant in 2025 
would be $41,000
""")

st.markdown("""By Jan 1st, 2025 the revenue generated by the charging stations should be at least
$62, 077
""")
header(f"Target financial goal of $62, 077 on January 1, 2025 will not be met")
header(f"{time_to_target} days past due and on January 1, 2025 you will be $3502.71 away from the target")
st.markdown("## **Recommendation: to achieve the target goal, the minimum hourly rate charge increase should be $0.11 **")
st.write("### By making this pricing change, at the end of grant period projected cumulative revenue will exceed the target by $5420.33")
st.write("#")

st.markdown("### Forecasted cumulative revenue")
st.markdown("""The following table gives you a real-time breakdown
               of how much you should expect to make each quarter.""")
st.dataframe(forecast_quarter_df.rename(columns={'cumsum_revenue_prediction': 'cumulative revenue'})) # will display the dataframe
#st.table(forecast_quarter_df)# will display the table

st.write("#")

st.bokeh_chart(fig_, use_container_width=True)









