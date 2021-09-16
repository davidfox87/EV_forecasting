import pandas as pd
import numpy as np
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Patch, HoverTool, CrosshairTool, BoxAnnotation
from bokeh.layouts import row, gridplot

import time
from datetime import datetime as dt

from bokeh.models import Span

def plot_forecast(data, df):
    df['ds'] = pd.to_datetime(df['ds'])

    source = ColumnDataSource(df)


    # absolute revenue plot
    p = figure(title='Visualizing revenue forecast through January 2025',
                x_axis_label='Date',
                y_axis_label='Revenue ($)',
                x_axis_type='datetime',
                sizing_mode="stretch_width", 
                height=600)

    forecast_future = df.loc[~df.ds.isin(data.index)]
    #forecast_future = df
    y1 = forecast_future['yhat_lower']
    y2 = forecast_future['yhat_upper'].iloc[::-1]
    x1 = forecast_future['ds']
    x2 = forecast_future['ds'].iloc[::-1]
    x = np.hstack((x1, x2))
    y = np.hstack((y1, y2))

    source2 = ColumnDataSource(dict(x=x, y=y))
    glyph = Patch(x="x", y="y", fill_color="aliceblue", fill_alpha=0.5)
    p.add_glyph(source2, glyph)

    p.line(x='ds', y='yhat', source=source, line_width=5, color="darkblue",
                    legend_label="Actual")
    p.line(x=forecast_future['ds'], y=forecast_future['yhat'], 
                    line_width=1, color="red", legend_label="Forecast")
    
    hover = HoverTool(tooltips=[('date', '@ds{%F}'), 
                                ('Value', '$y')],
            formatters={'@ds' : 'datetime'})
    p.add_tools(hover)
    p.add_tools(CrosshairTool())

    p.xaxis.major_label_text_font_size = "20pt"
    p.yaxis.major_label_text_font_size = "20pt"
    p.xaxis.axis_label_text_font_size = "20pt"
    p.yaxis.axis_label_text_font_size = "20pt"
    p.title.text_font_size = "25px" 

    # cumulative revenue
    p2 = figure(title='Visualizing cumulative revenue forecast through January 2025',
                x_axis_label='Date',
                x_axis_type='datetime',
                y_axis_label='Cumulative Revenue ($)',
                sizing_mode="stretch_width", 
                height=600)
    
    p2.line(x=forecast_future['ds'], y=forecast_future['yhat'].cumsum(), line_width=1, color="red")
    #p2.line(x='ds', y='cumsum_revenue_prediction', source=source, line_width=5, color="darkblue")
    p2.xaxis.major_label_text_font_size = "20pt"
    p2.yaxis.major_label_text_font_size = "20pt"
    p2.xaxis.axis_label_text_font_size = "20pt"
    p2.yaxis.axis_label_text_font_size = "20pt"
    p2.title.text_font_size = "25px"



    # plot patch for projected cumulative revenue
    cumsum_revenue_lower = forecast_future['yhat_lower'].cumsum()
    cumsum_revenue_upper = forecast_future['yhat_upper'].cumsum()
    y1 = cumsum_revenue_lower
    y2 = cumsum_revenue_upper.iloc[::-1]
    x1 = forecast_future['ds']
    x2 = forecast_future['ds'].iloc[::-1]
    x = np.hstack((x1, x2))
    y = np.hstack((y1, y2))


    source2 = ColumnDataSource(dict(x=x, y=y))
    glyph = Patch(x="x", y="y", fill_color="aliceblue", fill_alpha=0.5)
    p2.add_glyph(source2, glyph)

    high_box = BoxAnnotation(bottom=62077, fill_alpha=0.1, fill_color='green')
    p2.add_layout(high_box)

    start_date = time.mktime(dt(2025, 1, 1, 2, 0, 0).timetuple())*1000
    goal_date = Span(location=start_date,
                                dimension='height', line_color='green',
                                line_dash='dashed', line_width=3)
    p2.add_layout(goal_date)



    forecast_start_date = time.mktime(dt(2021, 7, 20, 2, 0, 0).timetuple())*1000
    forecast_start = Span(location=forecast_start_date,
                                dimension='height', line_color='black',
                                line_dash='dashed', line_width=3)
    p.add_layout(forecast_start)


    return row(p, p2)
