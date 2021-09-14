from bokeh.core.property.color import Color
import streamlit as st
import numpy as np
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Patch, HoverTool, CrosshairTool
from prophet import Prophet
import boto3
from dotenv import load_dotenv
load_dotenv()  


st.set_page_config(layout="wide")


# s3 = boto3.client("s3", 
#                   region_name='us-west-2', 
#                   aws_access_key_id='AKIA42BR2TSGT4RPROK7', 
#                   aws_secret_access_key='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')

# df_list = []
# response = s3.list_objects(Bucket='tdicapstone')
# request_files = response["Contents"]

# print(request_files)
# for file in request_files:
#      obj = s3.get_object(Bucket='tdicapstone', Key=file["Key"])
#      print(obj)
#      obj_df = pd.read_csv(obj["Body"])
#      df_list.append(obj_df)
# df = pd.concat(df_list)

df1 = pd.read_csv('data/Fort Collins Utilities EV Data June 2020 to June 2021.csv')
df2 = pd.read_csv('data/Fort Collins Utilities EV Data June 25 2021 to July 20 2021.csv')
df = pd.concat([df1, df2])

df.info()

df.rename(columns={'Session/Reservation Start Date': 'Date'}, inplace=True)
df = df.dropna(how='all')

df['Date'] = pd.to_datetime(df['Date'])
df.set_index(df['Date'], inplace=True)

df2 = df[['Energy (kWh)', 'Net Revenue']].resample('1D').sum().reset_index()

df2.set_index('Date', inplace=True)


df2["Energy (kWh)_7D"] = df2['Energy (kWh)'].\
                         transform(lambda x: x.rolling(7, min_periods=7, closed='both', center=True).median())
df2["Net Revenue_7D"] = df2['Net Revenue'].\
                         transform(lambda x: x.rolling(7, min_periods=7, closed='both', center=True).median())

df2['Energy (kWh)_7D'] = df2['Energy (kWh)_7D'].interpolate(method='linear', limit_direction='both')
df2['Net Revenue_7D'] = df2['Net Revenue_7D'].interpolate(method='linear', limit_direction='both')



def make_forecasting_df(dataframe, col):
    yy = "Energy (kWh)_7D" if col=="Demand" else "Net Revenue_7D"
        
    df = dataframe.rename(columns={yy:'y', 'Start Date':'ds'})
    df['ds'] = df.index
    
    return df


st.sidebar.subheader("Forecasting Options")

option = st.sidebar.selectbox(
    'What would you like to forecast?',
    ('Demand', 'Revenue'))



df_ = make_forecasting_df(df2, option)

def is_stay_at_home(ds):
    date = pd.to_datetime(ds)
    return (date >= pd.Timestamp(2020,3,25) and date < pd.Timestamp(2020,4,26))

df_['is_stay_at_home'] = df_['ds'].apply(is_stay_at_home)
df_['is_not_stay_at_home'] = ~df_['ds'].apply(is_stay_at_home)

def create_end_of_year_holidays_df():
    """Create holidays data frame for the end of the year season."""
    holidays = pd.DataFrame({
      'holiday': 'end_of_year',
      'ds': pd.to_datetime(
          ['2019-12-25', '2020-12-25']
      ),
      'lower_window': -7,
      'upper_window': 7,
    })
    return holidays


def build_model():
    """Define forecasting model."""
    # Create holidays data frame. 
    holidays = create_end_of_year_holidays_df()
    
    model = Prophet(
        yearly_seasonality=True,
        #weekly_seasonality=True,
        daily_seasonality=False, 
        holidays = holidays, 
        interval_width=0.95, 
    )

    model.add_seasonality(
        name='monthly', 
        period=30.5, 
        fourier_order=30
    )

    model.add_seasonality(
        name='stay_at_home', 
        period=7, 
        fourier_order=30, 
        condition_name='is_stay_at_home'
    )
    model.add_seasonality(
        name='no_stay_at_home', 
        period=7, 
        fourier_order=30, 
        condition_name='is_not_stay_at_home')
    
    return model
    
model = build_model()
model.fit(df_)


st.title("Fort Collins EV demand and revenue Forecasting App")



forecast_horizon = st.sidebar.number_input("Forecast_horizon (days)", \
                                            value=30, \
                                            min_value=30, \
                                            max_value=90, \
                                            step=1)




future = model.make_future_dataframe(periods=forecast_horizon)
future['is_stay_at_home'] = future['ds'].apply(is_stay_at_home)
future['is_not_stay_at_home'] = ~future['ds'].apply(is_stay_at_home)
forecast = model.predict(future)

forecast['ds'] = pd.to_datetime(forecast['ds'])

source = ColumnDataSource(forecast)

p = figure(title='EV Forecasting Tool',
            x_axis_label='Date',
            x_axis_type='datetime',
            sizing_mode="stretch_width", 
            height=600)

forecast_future = forecast.loc[~forecast.ds.isin(df_.ds)]
y1 = forecast_future['yhat_lower']
y2 = forecast_future['yhat_upper'].iloc[::-1]
x1 = forecast_future['ds']
x2 = forecast_future['ds'].iloc[::-1]
x = np.hstack((x1, x2))
y = np.hstack((y1, y2))

source2 = ColumnDataSource(dict(x=x, y=y))
glyph = Patch(x="x", y="y", fill_color="aliceblue", fill_alpha=0.5)
p.add_glyph(source2, glyph)

p.line(x='ds', y='yhat', source=source, line_width=5, color="darkblue")
p.line(x=forecast_future['ds'], y=forecast_future['yhat'], line_width=5, color="red")
hover = HoverTool(tooltips=[('date', '@ds{%F}'), 
                            ('Value', '$y')],
        formatters={'@ds' : 'datetime'})
p.add_tools(hover)
p.add_tools(CrosshairTool())

p.xaxis.major_label_text_font_size = "20pt"
p.yaxis.major_label_text_font_size = "20pt"
p.xaxis.axis_label_text_font_size = "20pt"
p.yaxis.axis_label_text_font_size = "20pt"

st.markdown(
    """
Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s,
 when an unknown printer took a galley of type and scrambled it to make a type specimen book. 
 It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. 
 It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, 
and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
## Try it out!
"""
)


st.bokeh_chart(p, use_container_width=True)


