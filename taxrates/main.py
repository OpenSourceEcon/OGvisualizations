from bokeh.plotting import show
from bokeh.models import ColumnDataSource, LayoutDOM, CustomJS, Slider, RangeSlider
from bokeh.core.properties import Instance, String
from bokeh.layouts import column, gridplot
from bokeh.models.widgets import RadioButtonGroup, Div
from bokeh.embed import components
from bokeh.resources import CDN

import pickle
import numpy as np
import pandas as pd
import sys

if 'show' in sys.argv:
    from callbacks.controls_callback_script import CONTROLS_CALLBACK_SCRIPT
    from txrates import clean_data
else:
    from taxrates.callbacks.controls_callback_script import CONTROLS_CALLBACK_SCRIPT
    from taxrates.txrates import clean_data


class Scatter3d(LayoutDOM):
    __implementation__ = "coffee/scatter_graph.coffee"

    data_source = Instance(ColumnDataSource)

    x = String
    y = String
    z = String
    color = String


class Bar3d(LayoutDOM):
    __implementation__ = "coffee/bar_graph.coffee"

    data_source = Instance(ColumnDataSource)

    x = String
    y = String
    z = String
    color = String


# DATA
# Read in the data and clean it
if 'show' in sys.argv:
    microDataDict_base_clean = pickle.load(open('data/micro_dict_base_clean.pkl', 'rb'))
    microDataDict_pol_clean = pickle.load(open('data/micro_dict_pol_clean.pkl', 'rb'))
else:
    microDataDict_base_clean = pickle.load(open('taxrates/data/micro_dict_base_clean.pkl', 'rb'))
    microDataDict_pol_clean = pickle.load(open('taxrates/data/micro_dict_pol_clean.pkl', 'rb'))

# CREATE INITIAL PLOTS
# example of 3D plots with one year and one age
year = int(2017)
age = 42
base_df = microDataDict_base_clean[str(year)]
base_df = base_df[base_df['Age'] == age]

# Truncate the data and prepare for base scatter plot
base_df_trnc = base_df[(base_df['Total Labor Income'] > 5) &
                       (base_df['Total Labor Income'] < 500000) &
                       (base_df['Total Capital Income'] > 5) &
                       (base_df['Total Capital Income'] < 500000)]
base_inc_lab = base_df_trnc['Total Labor Income'].reset_index(drop=True)
base_inc_cap = base_df_trnc['Total Capital Income'].reset_index(drop=True)
base_etr_data = base_df_trnc['Effective Tax Rate'].reset_index(drop=True)

scatter_source = ColumnDataSource(data=dict(x=base_inc_lab, y=base_inc_cap,
                                            z=base_etr_data))

# Prepare data for bar plot
bin_num = int(30)
hist, xedges, yedges = np.histogram2d(base_inc_lab, base_inc_cap,
                                      bins=bin_num)
hist = hist / hist.sum()
x_midp = xedges[:-1] + 0.5 * (xedges[1] - xedges[0])
y_midp = yedges[:-1] + 0.5 * (yedges[1] - yedges[0])
ypos, xpos = np.meshgrid(y_midp, x_midp)
xpos = xpos.flatten()
ypos = ypos.flatten()
dz = hist.flatten()

bar_source = ColumnDataSource(data=dict(x=xpos, y=ypos, z=dz))

# scatter 3D
scatter = Scatter3d(x="x", y="y", z="z", color="color",
                    data_source=scatter_source, width=800, height=370)

# bar 3D
bar = Bar3d(x="x", y="y", z="z", color="color", data_source=bar_source,
            width=800, height=370)

source_dict = {}
for i in range(2017, 2027):
    source_dict['base_'+str(i)] = ColumnDataSource(data=microDataDict_base_clean[str(i)])
    source_dict['pol_'+str(i)] = ColumnDataSource(data=microDataDict_pol_clean[str(i)])

# create callback for all controls
controls_callback = CustomJS(args=dict(base_2017=source_dict['base_2017'],
                                       pol_2017=source_dict['pol_2017'],
                                       base_2018=source_dict['base_2017'],
                                       pol_2018=source_dict['base_2017'],
                                       base_2019=source_dict['base_2017'],
                                       pol_2019=source_dict['base_2017'],
                                       base_2020=source_dict['base_2017'],
                                       pol_2020=source_dict['base_2017'],
                                       base_2021=source_dict['base_2017'],
                                       pol_2021=source_dict['base_2017'],
                                       base_2022=source_dict['base_2017'],
                                       pol_2022=source_dict['base_2017'],
                                       base_2023=source_dict['base_2017'],
                                       pol_2023=source_dict['base_2017'],
                                       base_2024=source_dict['base_2017'],
                                       pol_2024=source_dict['base_2017'],
                                       base_2025=source_dict['base_2017'],
                                       pol_2025=source_dict['base_2017'],
                                       base_2026=source_dict['base_2017'],
                                       pol_2026=source_dict['base_2017'],
                                       scatter_source=scatter_source,
                                       bar_source=bar_source),
                             code=CONTROLS_CALLBACK_SCRIPT)

# tax type buttons
tax_buttons = RadioButtonGroup(labels=['ETR', 'MTR(x)', 'MTR(y)'],
                               active=0, callback=controls_callback)
controls_callback.args['tax_buttons'] = tax_buttons

# state buttons
state_buttons = RadioButtonGroup(labels=['Base', 'Reform', 'Change'],
                                 active=0, callback=controls_callback)
controls_callback.args['state_buttons'] = state_buttons

# year slider
year_slider = Slider(start=2017, end=2026, value=2017, step=1, title="Year",
                     callback=controls_callback,
                     callback_policy="mouseup")
controls_callback.args['year_slider'] = year_slider

# range slider x
x_slider = RangeSlider(start=0, end=60000000, range=[5, 500000], step=10000,
                       title='X-axis Range', callback=controls_callback,
                       callback_policy="mouseup")
controls_callback.args['x_slider'] = x_slider

# range slider y
y_slider = RangeSlider(start=0, end=60000000, range=[5, 500000], step=10000,
                       title='Y-axis Range', callback=controls_callback,
                       callback_policy="mouseup")
controls_callback.args['y_slider'] = y_slider

# range slider age
age_slider = RangeSlider(start=10, end=85, range=[age, age+1], step=1,
                         title='Age Range', callback=controls_callback,
                         callback_policy="mouseup")
controls_callback.args['age_slider'] = age_slider

space_div = Div(width=400, height=150)

scatter_title = Div(text="""<center><b>Tax Rate Scatter Plot</b></center>""",
                    width=600)

bar_title = Div(text="""<center><b>Population Histogram</b></center>""",
                width=600)


# create layout and show!
column_3d = column(scatter_title, scatter, bar_title, bar)
column_controls = column(tax_buttons, state_buttons, space_div,
                         year_slider, age_slider, x_slider, y_slider)
layout = gridplot(
    children=[[column_3d, column_controls]],
    toolbar_location=None
)

js, div = components(layout)
cdn_js = CDN.js_files[0]
cdn_css = CDN.css_files[0]

if 'show' in sys.argv:
    show(layout)
