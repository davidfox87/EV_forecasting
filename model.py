
import pandas as pd
from prophet import Prophet


def is_stay_at_home(ds):
    date = pd.to_datetime(ds)
    return (date >= pd.Timestamp(2020,3,25) and date < pd.Timestamp(2020,4,26))


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
    