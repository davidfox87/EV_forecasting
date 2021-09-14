import pandas as pd
import numpy as np
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Patch, HoverTool, CrosshairTool

def plot_forecast(df):
    df['ds'] = pd.to_datetime(df['ds'])

    source = ColumnDataSource(df)

    p = figure(title='EV Forecasting Tool',
                x_axis_label='Date',
                x_axis_type='datetime',
                sizing_mode="stretch_width", 
                height=600)

    forecast_future = df.loc[~df.ds.isin(df.ds)]
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

    return p
