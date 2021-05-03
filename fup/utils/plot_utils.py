import numpy as np
from bokeh.plotting import figure
from bokeh.models import NumeralTickFormatter
from bokeh.models import Band, ColumnDataSource
from bokeh.models import Legend, LegendItem

def percentile(n):
    def percentile_(x):
        return np.percentile(x, n)
    percentile_.__name__ = 'percentile_%s' % n
    return percentile_

def create_plot(df, column, name, unit, color, legend_location="top_right"):
    dfg = df.groupby("year", as_index=False).agg({
        column: [percentile(5), percentile(25), percentile(50), percentile(75), percentile(95)],
    })
    source = ColumnDataSource(dfg)
    y_min = min(0, 1.1 * dfg[column]["percentile_5"].min())
    y_max = 1.1 * dfg[column]["percentile_95"].max()

    tools = "pan,wheel_zoom,box_zoom,reset,save"
    p = figure(plot_width=800, plot_height=400,
               y_range=(y_min, y_max),
               tools=tools)
    p.xaxis.axis_label = "Year"
    p.yaxis.axis_label = f"{name} [{unit}]"
    p.yaxis.formatter = NumeralTickFormatter(format="0,0")
    p.title.text = f"{name} over the years"
    p.xgrid[0].grid_line_color = None
    p.ygrid[0].grid_line_alpha = 0.5

    p.varea(x='year_', y1=f'{column}_percentile_5', y2=f'{column}_percentile_95', source=source,
            fill_alpha=0.3, fill_color=color, legend_label="90% range")

    p.varea(x='year_', y1=f'{column}_percentile_25', y2=f'{column}_percentile_75', source=source,
            fill_alpha=0.5, fill_color=color, legend_label="50% range")

    p.line(x=dfg["year"], y=dfg[column]["percentile_50"], line_width=3., line_color=color,
           legend_label="median"
           )

    p.legend.location = legend_location
    p.legend.click_policy = "hide"

    return p
