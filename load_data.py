
import pandas as pd

import streamlit as st  # pylint: disable=import-error


@st.cache
def load_data():
    """Loads the dataset from a filepath."""

    df1 = pd.read_csv('data/Fort Collins Utilities EV Data June 2020 to June 2021.csv')
    df2 = pd.read_csv('data/Fort Collins Utilities EV Data June 25 2021 to July 20 2021.csv')
    df = ( pd.concat([df1, df2]).rename(
                                    columns={'Session/Reservation Start Date': 'Date'})
                                .dropna(how='all')
                                .assign(Date=lambda df: pd.to_datetime(df["Date"]))
                                .set_index('Date')
    )

    df2 = df[['Energy (kWh)', 'Net Revenue']].resample('1D').sum().reset_index()

    df2.set_index('Date', inplace=True)


    df2["Energy (kWh)_7D"] = df2['Energy (kWh)'].\
                            transform(lambda x: x.rolling(7, min_periods=7, closed='both', center=True).median())
    df2["Net Revenue_7D"] = df2['Net Revenue'].\
                            transform(lambda x: x.rolling(7, min_periods=7, closed='both', center=True).median())

    df2['Energy (kWh)_7D'] = df2['Energy (kWh)_7D'].interpolate(method='linear', limit_direction='both')
    df2['Net Revenue_7D'] = df2['Net Revenue_7D'].interpolate(method='linear', limit_direction='both')

    return df2



