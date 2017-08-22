from bokeh.plotting import show
from bokeh.models import ColumnDataSource, LayoutDOM, CustomJS
from bokeh.core.properties import Instance, String
from bokeh.layouts import column, gridplot
from bokeh.models.widgets import RadioButtonGroup
from txrates import clean_data
from callbacks.scatter_button_callback_script import SCATTER_BUTTON_CALLBACK_SCRIPT
import pickle
import numpy as np
import pandas as pd


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
microDataDict_base_clean = pickle.load(open('data/micro_dict_base_clean.pkl', 'rb'))
microDataDict_pol_clean = pickle.load(open('data/micro_dict_pol_clean.pkl', 'rb'))

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
base_mtrx_data = base_df_trnc['MTR Labor Income'].reset_index(drop=True)
base_mtry_data = base_df_trnc['MTR capital income'].reset_index(drop=True)

# Truncate the data and prepare for pol scatter plot
pol_df = microDataDict_pol_clean[str(year)]
pol_df = pol_df[pol_df['Age'] == age]

pol_df_trnc = pol_df[(pol_df['Total Labor Income'] > 5) &
             (pol_df['Total Labor Income'] < 500000) &
             (pol_df['Total Capital Income'] > 5) &
             (pol_df['Total Capital Income'] < 500000)]
pol_etr_data = pol_df_trnc['Effective Tax Rate'].reset_index(drop=True)
pol_mtrx_data = pol_df_trnc['MTR Labor Income'].reset_index(drop=True)
pol_mtry_data = pol_df_trnc['MTR capital income'].reset_index(drop=True)

# prepare data for change scatter plot
change_etr_data = pol_etr_data - base_etr_data
change_mtrx_data = pol_mtrx_data - base_mtrx_data
change_mtry_data = pol_mtry_data - base_mtry_data


scatter_source = ColumnDataSource(data=dict(x=base_inc_lab, y=base_inc_cap,
                                            z=base_etr_data))
etr_source = ColumnDataSource(data=dict(z_base=base_etr_data, z_pol=pol_etr_data, z_change=change_etr_data))
mtrx_source = ColumnDataSource(data=dict(z_base=base_mtrx_data, z_pol=pol_mtrx_data, z_change=change_mtrx_data))
mtry_source = ColumnDataSource(data=dict(z_base=base_mtry_data, z_pol=pol_mtry_data, z_change=change_mtry_data))

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

# import pdb; pdb.set_trace()

# scatter 3D
scatter = Scatter3d(x="x", y="y", z="z", color="color",
                    data_source=scatter_source, width=800, height=370)

# bar 3D
bar = Bar3d(x="x", y="y", z="z", color="color", data_source=bar_source,
            width=800, height=370)

# create callback for tax type/state of scatter plot
scatter_button_callback = CustomJS(args=dict(scatter_source=scatter_source,
                                             etr_source=etr_source,
                                             mtrx_source=mtrx_source,
                                             mtry_source=mtry_source),
                                   code=SCATTER_BUTTON_CALLBACK_SCRIPT)
# tax type buttons
tax_buttons = RadioButtonGroup(labels=['ETR', 'MTR(x)', 'MTR(y)'],
                               active=0, callback=scatter_button_callback)
scatter_button_callback.args['tax_buttons'] = tax_buttons

# state buttons
state_buttons = RadioButtonGroup(labels=['Base', 'Policy', 'Change'],
                                 active=0, callback=scatter_button_callback)
scatter_button_callback.args['state_buttons'] = state_buttons

# create layout and show!
column_3d = column(scatter, bar)
column_controls = column(tax_buttons, state_buttons)
layout = gridplot(
    children=[[column_3d, column_controls]],
    toolbar_location=None
)
show(layout)
