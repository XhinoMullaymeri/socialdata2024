from bokeh.io import show, curdoc
from bokeh.plotting import gmap
from bokeh.models import ColumnDataSource, GMapOptions, CustomJS, Spacer, RangeSlider, HoverTool
from bokeh.models.widgets import Slider, RadioButtonGroup, Div, CheckboxButtonGroup
from bokeh.layouts import layout,column, row
from bokeh.io import output_file
from bokeh.transform import factor_cmap
from bokeh.palettes import Bright6
from bokeh.models import TabPanel, Tabs, Tooltip
from bokeh.transform import dodge

# Sample DataFrame replacement for demonstration purposes
import pandas as pd
from datetime import datetime

from bokeh.plotting import figure
from bokeh.models import BoxZoomTool, PanTool, WheelZoomTool


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import re
import logging
import plotly.express as px
import json
# Set Matplotlib's logger to ignore warnings
logging.getLogger('matplotlib').setLevel(logging.ERROR)
plt.rcParams['font.family'] = 'Helvetica' 

google_api_key = ""


crash_df = pd.read_csv(r'D:\Projects\social_data_2024\socialdata2024\fatal_severe_crashes.csv')
dui_df = pd.read_csv(r'D:\Projects\socialdata2024\solutions\data\dui_data.csv')


days_mapping = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}

# select from dui_df where wday 0 month is January and years 2013 or 2017
source = ColumnDataSource(dui_df[(dui_df['wday'] == 1) & (dui_df['month'] == 1) & (dui_df['year'].isin([2013, 2017]))])
source_crash = ColumnDataSource(crash_df[(crash_df['wday'] == 1) & (crash_df['month'] == 1) & (crash_df['year'].isin([2013, 2017]))])
map_options = GMapOptions(lat=37.7649, lng=-122.4394, map_type="roadmap", zoom=12)
p = gmap(google_api_key, map_options, title="San Francisco Map", tools="pan,box_zoom,wheel_zoom,save,reset", width=730, height=550)

for t in p.tools:
    if isinstance(t, WheelZoomTool):
        p.toolbar.active_scroll = t
# titel color 
p.title.text_alpha = 1
p.title.text_font = "Helvetica"
p.title.text_font_style = "bold"
p.title.text_font_size = "15px"
p.title.align = "center"


p.scatter(x="lon", y="lat", size=7, fill_color="#96DEFD", fill_alpha=0.8, source=source, marker="circle", legend_label="DUI reports", line_color="#0071A2")
p.scatter(x="lon", y="lat", size=9, fill_color="red", fill_alpha=0.6, source=source_crash, marker="diamond", legend_label="Severe and Fatal crashes", line_color=None)


# Define a CheckboxButtonGroup dui checkboxes
days_cb_dui = CheckboxButtonGroup(labels=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], active=[0,1,2,3,4,5,6])
days_dui_div = Div(text="Select <b> Days </b>")

months_cb_dui = CheckboxButtonGroup(labels=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], active=[0,1,2,3,4,5,6,7,8,9,10,11])
months_dui_div= Div(text="Select <b> Months </b>")

years_cb_dui = CheckboxButtonGroup(labels=["2003","2004","2005","2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016","2017"], active=[14])
years_dui_div = Div(text="Select <b> Years </b>")

# add a callback to checkboxes
def update_days_dui_checkbox(attr, old, new):
    change_source_data(new, months_cb_dui.active  , years_cb_dui.active)
days_cb_dui.on_change('active', update_days_dui_checkbox)


def update_months_dui_checkbox(attr, old, new):
    change_source_data(days_cb_dui.active,  new, years_cb_dui.active)
months_cb_dui.on_change('active', update_months_dui_checkbox)

def update_years_dui_checkbox(attr, old, new):
    change_source_data(days_cb_dui.active, months_cb_dui.active, new)
years_cb_dui.on_change('active', update_years_dui_checkbox)


def change_source_data(day_filter, month_filter, year_filter):
    print("Input values:")
    print(day_filter, month_filter, year_filter)
    #selected_days = [i+1 for i in day_filter]
    selected_days = day_filter
    selected_months = [i+1 for i in month_filter]
    selected_years = [2003+i for i in year_filter]
    print("Transformed values:")
    print(selected_days, selected_months, selected_years)
    filtered_data = dui_df[(dui_df['wday'].isin(selected_days)) & (dui_df['month'].isin(selected_months)) & (dui_df['year'].isin(selected_years))]
    print(filtered_data.shape)
    source.data = filtered_data.to_dict(orient='list')
    total_duis = []
    for i in range(2003, 2018):
        total_duis.append(filtered_data[(filtered_data['year'] == i)].shape[0])
    source_bar.data['DUI'] = total_duis




# Layout
days_of_week_row = row(children=[days_dui_div,Spacer(width=52, height=10),days_cb_dui], sizing_mode='scale_both')
months_row = row(children=[months_dui_div,Spacer(width=39, height=10),months_cb_dui], sizing_mode='scale_both')
years_row = row(children=[years_dui_div,Spacer(width=50, height=10),years_cb_dui], sizing_mode='scale_both')


# Define a CheckboxButtonGroup crash checkboxes
days_cb_crash = CheckboxButtonGroup(labels=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], active=[0,1,2,3,4,5,6])
days_crash_div = Div(text="Select <b> Days </b>")
months_cb_crash = CheckboxButtonGroup(labels=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], active=[0,1,2,3,4,5,6,7,8,9,10,11])
months_crash_div= Div(text="Select <b> Months </b>")
years_cb_crash = CheckboxButtonGroup(labels=["2003","2004","2005","2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016","2017"], active=[14])
years_crash_div = Div(text="Select <b> Years </b>")


# add a callback to checkboxes
def update_days_crash_checkbox(attr, old, new):
    change_source_crash_data(new, months_cb_crash.active  , years_cb_crash.active)
days_cb_crash.on_change('active', update_days_crash_checkbox)


def update_months_crash_checkbox(attr, old, new):
    change_source_crash_data(days_cb_crash.active,  new, years_cb_crash.active)
months_cb_crash.on_change('active', update_months_crash_checkbox)

def update_years_crash_checkbox(attr, old, new):
    change_source_crash_data(days_cb_crash.active, months_cb_crash.active, new)
years_cb_crash.on_change('active', update_years_crash_checkbox)


def change_source_crash_data(day_filter, month_filter, year_filter):
    print("Input values:")
    print(day_filter, month_filter, year_filter)
    selected_days = day_filter
    selected_months = [i+1 for i in month_filter]
    selected_years = [2003+i for i in year_filter]
    print("Transformed values:")
    print(selected_days, selected_months, selected_years)
    filtered_data = crash_df[(crash_df['wday'].isin(selected_days)) & (crash_df['month'].isin(selected_months)) & (crash_df['year'].isin(selected_years))]
    print(filtered_data.shape)
    source_crash.data = filtered_data.to_dict(orient='list')


    # # update linechart
    # total_crashes = []
    # for i in range(2003, 2018):
    #     total_crashes.append(filtered_data[(filtered_data['year'] == i)].shape[0])

    # # remove all lines with legend_label="Sever and Fatal crashes"
    # # p_line.renderers = [r for r in p_line.renderers if r.glyph.line_color != "red"]
    # source_bar.data['Crashes'] = total_crashes



# radio btn with 4 options for colors in filter
color_filtered_crash = RadioButtonGroup(labels=["None", "Day", "Month", "Year"], active=0)
color_filter_crash_div = Div(text=f"<b> Filter </b> by: None")
def update_color_filter(attr, old, new):
    color_filter_crash_div.text = f"<b> Filter </b> by: {color_filtered_crash.labels[new]}"
color_filtered_crash.on_change('active', update_color_filter)


# Layout
days_dui_row = row(children=[days_dui_div,Spacer(width=52, height=10),days_cb_dui], sizing_mode='scale_both')
months_dui_row = row(children=[months_dui_div,Spacer(width=39, height=10),months_cb_dui], sizing_mode='scale_both')
years_dui_row = row(children=[years_dui_div,Spacer(width=50, height=10),years_cb_dui], sizing_mode='scale_both')

days_crash_row = row(children=[days_crash_div,Spacer(width=52, height=10),days_cb_crash], sizing_mode='scale_both')
months_crash_row = row(children=[months_crash_div,Spacer(width=39, height=10),months_cb_crash], sizing_mode='scale_both')
years_crash_row = row(children=[years_crash_div,Spacer(width=50, height=10),years_cb_crash], sizing_mode='scale_both')

def center_row(r,width_l=0, width_r=30):
    return row(Spacer(width=width_l), r, Spacer(width=width_r))

centered_days_dui_row = center_row(days_dui_row)
centered_months_dui_row = center_row(months_dui_row)
centered_years_dui_row = center_row(years_dui_row)

centered_days_crash_row = center_row(days_crash_row)
centered_months_crash_row = center_row(months_crash_row)
centered_years_crash_row = center_row(years_crash_row)


main_dui_filters = column(
    centered_days_dui_row,
    centered_months_dui_row,
    centered_years_dui_row
)

main_crash_filters = column(
    centered_days_crash_row,
    centered_months_crash_row,
    centered_years_crash_row
)


# line chart
x = [2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017]
y = [0, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 8000]
p_line = figure(title="Simple line example", x_axis_label='x', y_axis_label='y')

x = [2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017]

# # create a new plot with a title and axis labels
# # p_line = figure(title="Simple line example", x_axis_label='x', y_axis_label='y')
# p = figure(x_range=x, height=350, toolbar_location=None, title="Fruit Counts")
# p.xgrid.grid_line_color = None
# p.y_range.start = 0
# p.y_range.end = 150
# p.legend.orientation = "horizontal"
# p.legend.location = "top_center"



# p.vbar(x='fruits', top='counts', width=0.9, source=source, legend_field="fruits",
#     line_color='white', fill_color=factor_cmap('fruits', palette=Bright6, factors=x))

# p.vbar(x='fruits', top='counts', width=0.9, source=source, legend_field="fruits",
#     line_color='white', fill_color=factor_cmap('fruits', palette=Bright6, factors=x))


years = ['2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017']
categories = ['DUI', 'Crashes']

total_crashes = []
total_duis = []



data = {'years' : years,
        'DUI'   : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 268],
        'Crashes'   : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 79]}

source_bar = ColumnDataSource(data=data)
tools = "pan,box_zoom,wheel_zoom,save,reset"

p_bar = figure(x_range=years, y_range=(0, 6000), title="Total DUI reports & Fatal crashes (Filtered)",
              width=535, height=550, tools=tools)

for t in p_bar.tools:
    if isinstance(t, WheelZoomTool):
        p_bar.toolbar.active_scroll = t

dui_bars = p_bar.vbar(x=dodge('years', -0.25, range=p_bar.x_range), top='DUI', source=source_bar,
       width=0.25, color="#96DEFD", legend_label="DUI reports")

crashes_bars = p_bar.vbar(x=dodge('years',  0.15,  range=p_bar.x_range), top='Crashes', source=source_bar,
       width=0.25, color="red", fill_alpha=0.6, legend_label="Crashes")

# Add HoverTool for DUI reports
hover_tool_dui = HoverTool(renderers=[dui_bars], tooltips=[("Year", "@years"), ("DUI reports", "@DUI")])
p_bar.add_tools(hover_tool_dui)

# Add HoverTool for Crashes #make it red color
hover_tool_crashes = HoverTool(renderers=[crashes_bars], tooltips=[("Year", "@years"), ("Crashes", "@Crashes")])
p_bar.add_tools(hover_tool_crashes)

# rotate x labels
p_bar.xaxis.major_label_orientation = 1
# dynami y range
p_bar.y_range.start = -3
p_bar.y_range.end = 600
p_bar.yaxis.axis_label = "Number of incidents"
p_bar.xaxis.axis_label = "Years"
p_bar.title.text_font_size = "15px"
p_bar.title.align = "center"
p_bar.title.text_font = "Helvetica"
p_bar.title.text_font_style = "bold"
p_bar.title.text_alpha = 1
p_bar.title.text_baseline = "middle"
p_bar.title.text_align = "center"
p_bar.title.text_line_height = 1.2

# similar for x and y titles
p_bar.xaxis.axis_label_text_font_size = "12px"
p_bar.xaxis.axis_label_text_font_style = "bold"
p_bar.xaxis.axis_label_text_font = "Helvetica"
p_bar.xaxis.axis_label_text_alpha = 1
p_bar.xaxis.axis_label_text_baseline = "middle"
p_bar.xaxis.axis_label_text_align = "center"
p_bar.xaxis.axis_label_text_line_height = 1.2

p_bar.yaxis.axis_label_text_font_size = "12px"
p_bar.yaxis.axis_label_text_font_style = "bold"
p_bar.yaxis.axis_label_text_font = "Helvetica"
p_bar.yaxis.axis_label_text_alpha = 1
p_bar.yaxis.axis_label_text_baseline = "middle"
p_bar.yaxis.axis_label_text_align = "center"
p_bar.yaxis.axis_label_text_line_height = 1.2





p_bar.x_range.range_padding = 0.1
p_bar.xgrid.grid_line_color = None
p_bar.legend.location = "top_right"
p_bar.legend.orientation = "horizontal"
# set legend size
p_bar.legend.label_text_font_size = "10px"
p_bar.legend.label_text_font = "Helvetica"





tab1 = TabPanel(child=main_dui_filters, title="DUI reports")
tab2 = TabPanel(child=main_crash_filters, title="Crashes")
tabs = Tabs(tabs=[tab1, tab2])
# add background color to tabs


change_source_data([0, 1, 2, 3, 4, 5, 6], [1, 2, 11, 12, 3, 4, 5, 6, 7, 8, 9, 10], [14])
change_source_crash_data([0, 1, 2, 3, 4, 5, 6], [1, 2, 11, 12, 3, 4, 5, 6, 7, 8, 9, 10], [14])






# ==============================================================================================================================
# ==============================================================================================================================

from bokeh.models import CustomJS



change_source_data_js = CustomJS(args=dict(data_df=dui_df.to_dict(orient='list') ,source=source, source_bar=source_bar, days_cb_dui=days_cb_dui, months_cb_dui=months_cb_dui, years_cb_dui=years_cb_dui), code="""
    // JavaScript to update the data source based on selected days
    var selected_days = []; // Array to hold selected days indices
    for (var i = 0; i < days_cb_dui.active.length; i++) {
        selected_days.push(days_cb_dui.active[i]);
    }

                            
    var selected_months = []; // Array to hold selected months indices
    for (var i = 0; i < months_cb_dui.active.length; i++) {
        selected_months.push(months_cb_dui.active[i]+1);
    }

    var selected_years = []; // Array to hold selected years indices
    for (var i = 0; i < years_cb_dui.active.length; i++) {
        selected_years.push(years_cb_dui.active[i]+2003);
    }

    console.log(selected_days)
    console.log(selected_months)
    console.log(selected_years)
                                 


    // Assuming 'wday' column in your source.data is what you filter by
    // make data to be my df_dui
    var data = data_df;
                                 

    var lon = data['lon'];
    var lat = data['lat'];
    var wday = data['wday'];
    var month = data['month'];
                                
    var year = data['year'];
                                 
    // Create new arrays to hold filtered data
    var new_lon = [];
    var new_lat = [];
    var new_wday = [];
    var new_month = [];
    var new_year = [];
                                 
    // Filter data based on selected days
    for (var i = 0; i < wday.length; i++) {
        if (selected_days.includes(wday[i]) && selected_months.includes(month[i]) && selected_years.includes(year[i])) {
            new_lon.push(lon[i]);
            new_lat.push(lat[i]);
            new_wday.push(wday[i]);
            new_month.push(month[i]);
            new_year.push(year[i]);
        }
    }


                                 
    // Update the source with the filtered data
    source.data = {'lon': new_lon, 'lat': new_lat, 'wday': new_wday, 'month': new_month, 'year': new_year};

    // count source.data 
    var total_duis = [];
    for (var i = 2003; i < 2018; i++) {
        var count = 0;
        for (var j = 0; j < source.data['year'].length; j++) {
            if (source.data['year'][j] == i) {
                count++;
            }
        }
        total_duis.push(count);
    }
                                 console.log(total_duis);
    source_bar.data['DUI'] = total_duis;



    // Trigger update
    source.change.emit();
    source_bar.change.emit();
""")
# Attach the CustomJS callback to the CheckboxButtonGroup
days_cb_dui.js_on_change('active', change_source_data_js)
months_cb_dui.js_on_change('active', change_source_data_js)
years_cb_dui.js_on_change('active', change_source_data_js)






change_source_crash_data_js = CustomJS(args=dict(data_df=crash_df.to_dict(orient='list') ,source=source_crash, source_bar=source_bar, days_cb_crash=days_cb_crash, months_cb_crash=months_cb_crash, years_cb_crash=years_cb_crash), code="""
    // JavaScript to update the data source based on selected days
    var selected_days = []; // Array to hold selected days indices
    for (var i = 0; i < days_cb_crash.active.length; i++) {
        selected_days.push(days_cb_crash.active[i]);
    }

                            
    var selected_months = []; // Array to hold selected months indices
    for (var i = 0; i < months_cb_crash.active.length; i++) {
        selected_months.push(months_cb_crash.active[i]+1);
    }

    var selected_years = []; // Array to hold selected years indices
    for (var i = 0; i < years_cb_crash.active.length; i++) {
        selected_years.push(years_cb_crash.active[i]+2003);
    }

    console.log(selected_days)
    console.log(selected_months)
    console.log(selected_years)
                                 


    // Assuming 'wday' column in your source.data is what you filter by
    // make data to be my df_dui
    var data = data_df;
                                 

    var lon = data['lon'];
    var lat = data['lat'];
    var wday = data['wday'];
    var month = data['month'];
                                
    var year = data['year'];
                                 
    // Create new arrays to hold filtered data
    var new_lon = [];
    var new_lat = [];
    var new_wday = [];
    var new_month = [];
    var new_year = [];
                                 
    // Filter data based on selected days
    for (var i = 0; i < wday.length; i++) {
        if (selected_days.includes(wday[i]) && selected_months.includes(month[i]) && selected_years.includes(year[i])) {
            new_lon.push(lon[i]);
            new_lat.push(lat[i]);
            new_wday.push(wday[i]);
            new_month.push(month[i]);
            new_year.push(year[i]);
        }
    }

    // Update the source with the filtered data
    source.data = {'lon': new_lon, 'lat': new_lat, 'wday': new_wday, 'month': new_month, 'year': new_year};

    // count source.data 
    var total_crashes = [];
    for (var i = 2003; i < 2018; i++) {
        var count = 0;
        for (var j = 0; j < source.data['year'].length; j++) {
            if (source.data['year'][j] == i) {
                count++;
            }
        }
        total_crashes.push(count);
    }
    source_bar.data['Crashes'] = total_crashes;
                                                                   
    // Trigger update
    source.change.emit();
    source_bar.change.emit();
""")
# Attach the CustomJS callback to the CheckboxButtonGroup
days_cb_crash.js_on_change('active', change_source_crash_data_js)
months_cb_crash.js_on_change('active', change_source_crash_data_js)
years_cb_crash.js_on_change('active', change_source_crash_data_js)

# ==============================================================================================================================
# ==============================================================================================================================

main_p = row(p,Spacer(width=10),p_bar,sizing_mode='stretch_width')
# create text widget
text = Div(text="""
<style>
    .custom-div h4 {
        font-family: 'Helvetica', sans-serif;
        font-size: 15px;
        font-weight: bold;
        text-align: center;
        opacity: 0.6;
        line-height: 1.2;
        margin: 0; /* Adjust as needed */
        padding: 0; /* Adjust as needed */
    }
</style>
<div class="custom-div">
    <h4>Select filters
</div>
""")
lay_out = layout([main_p,[Spacer(width=160),column(text,Spacer(width=5),tabs)]])


curdoc().add_root(lay_out)




# store to html
print("Storing to html")
output_file("D:\Projects\social_data_2024\socialdata2024\assignments\map_bookeh2.html")
output_file("map_bookeh2.html")

# save plot to html
show(lay_out)