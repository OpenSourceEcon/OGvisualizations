from bokeh.plotting import show
from bokeh.models import ColumnDataSource, LayoutDOM
from bokeh.core.properties import Instance, String
from bokeh.layouts import column, layout
from txrates import clean_data
import pickle
import numpy as np


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
start_yr = 2017
end_yr = 2026
micro_dict_base = pickle.load(open('data/micro_dict_base.pkl', 'rb'))
micro_dict_pol = pickle.load(open('data/micro_dict_pol.pkl', 'rb'))
microDataDict_base_clean = clean_data(micro_dict_base, start_yr, end_yr)
microDataDict_pol_clean = clean_data(micro_dict_pol, start_yr, end_yr)

# example of 3D plots with one year and one age
year = int(2017)
age = 42
df = microDataDict_base_clean[str(year)]
df = df[df['Age'] == age]

# Truncate the data
df_trnc = df[(df['Total Labor Income'] > 5) &
             (df['Total Labor Income'] < 500000) &
             (df['Total Capital Income'] > 5) &
             (df['Total Capital Income'] < 500000)]
inc_lab = df_trnc['Total Labor Income']
inc_cap = df_trnc['Total Capital Income']
etr_data = df_trnc['Effective Tax Rate']
mtrx_data = df_trnc['MTR Labor Income']
mtry_data = df_trnc['MTR capital income']

scatter_source = ColumnDataSource(data=dict(x=inc_lab, y=inc_cap, z=etr_data))

# Prepare data for histogram
bin_num = int(30)
hist, xedges, yedges = np.histogram2d(inc_lab, inc_cap,
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

column_3d = column(scatter, bar)
show(column_3d)
