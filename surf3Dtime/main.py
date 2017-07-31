import numpy as np
import pickle
import os
import sys

from bokeh.core.properties import Instance, String
from bokeh.models import ColumnDataSource, LayoutDOM, CustomJS, Slider, Legend
from bokeh.layouts import layout, widgetbox, gridplot, column
from bokeh.models.widgets import RadioButtonGroup, Div
from bokeh.plotting import figure, show
from bokeh.embed import components
from bokeh.resources import CDN

if 'show' in sys.argv:
    from callbacks.line_callback_script import LINE_CALLBACK_SCRIPT
    from callbacks.slider_callback_script import SLIDER_CALLBACK_SCRIPT
else:
    from surf3Dtime.callbacks.line_callback_script import LINE_CALLBACK_SCRIPT
    from surf3Dtime.callbacks.slider_callback_script import SLIDER_CALLBACK_SCRIPT


class Surface3d(LayoutDOM):
    __implementation__ = "coffee/surface_graph.coffee"

    data_source = Instance(ColumnDataSource)

    x = String
    y = String
    z = String
    color = String


# DATA
# read in data from pickle
tpi_args = pickle.load(open(
    'surf3Dtime/HeteroAbil/s80j7/OUTPUT/TPI/tpi_args.pkl', 'rb'))
tpi_vars = pickle.load(open(
    'surf3Dtime/HeteroAbil/s80j7/OUTPUT/TPI/tpi_vars.pkl', 'rb'))

# create smat and jmat
S = tpi_args[1]
lambdas = tpi_args[4]
sgrid = np.arange(1, S + 1)
lamcumsum = lambdas.cumsum()
jmidgrid = 0.5 * lamcumsum + 0.5 * (lamcumsum - lambdas)
smat, jmat = np.meshgrid(sgrid, jmidgrid)
smat = smat.ravel()
jmat = jmat.ravel()

# create bpath data objects
b_path = tpi_vars['bpath'].T
bvalue = b_path[0]
bvalue = bvalue.ravel()
source = ColumnDataSource(data=dict(x=smat, y=jmat, z=bvalue, color=bvalue))
bsource = ColumnDataSource(data=dict(x=smat, y=jmat, z=bvalue, color=bvalue))
bpath_ravel = b_path.ravel()
bpath_source = ColumnDataSource(data=dict(bpath=bpath_ravel))

# create cpath data objects
c_path = tpi_vars['cpath'].T
cvalue = c_path[0]
cvalue = cvalue.ravel()
csource = ColumnDataSource(data=dict(x=smat, y=jmat, z=cvalue, color=cvalue))
cpath_ravel = c_path.ravel()
cpath_source = ColumnDataSource(data=dict(cpath=cpath_ravel))

# create npath data objects
n_path = tpi_vars['npath'].T
nvalue = n_path[0]
nvalue = nvalue.ravel()
nsource = ColumnDataSource(data=dict(x=smat, y=jmat, z=nvalue, color=nvalue))
npath_ravel = n_path.ravel()
npath_source = ColumnDataSource(data=dict(npath=npath_ravel))

# information about data for slider
time_periods = b_path.shape[0]

rpath_value = tpi_vars['rpath']
wpath_value = tpi_vars['wpath']
kpath_value = tpi_vars['Kpath']
lpath_value = tpi_vars['Lpath']
ypath_value = tpi_vars['Ypath']
cpath_value = tpi_vars['Cpath']
line_paths = [rpath_value, wpath_value, kpath_value, lpath_value, ypath_value,
              cpath_value]

# dynamically choose the number of time periods
for path in line_paths:
    for i in range(len(path)-1):
        if abs((path[i+1]-path[i])/path[i+1]) < 0.000001:
            if path[0] == rpath_value[0]:
                time_periods = i
            elif time_periods < i:
                time_periods = i
            break

# find upper and lower bounds for plots and create source for plotting
num_abilities = len(lambdas)
variables = [time_periods, S, num_abilities]
paths = [b_path.ravel(), c_path.ravel(), n_path.ravel()]
for path in paths:
    # lower bound for surface plot
    lb = min(path) - 0.1*(max(path)-min(path))
    variables.append(lb)
    # upper bound for surface plot
    ub = max(path) + 0.1*(max(path)-min(path))
    variables.append(ub)
data_info = ColumnDataSource(data=dict(variables=variables))

# 3D SURFACE
surface = Surface3d(x="x", y="y", z="z", color="color", data_source=source,
                    width=800, height=370)

# 2D PLOT
# create 2d plot
two_d_plot = figure(plot_width=600, plot_height=300,
                    title='Age path for individual savings b')
two_d_plot_data = dict(x=sgrid)
for j in range(num_abilities):
    two_d_plot_data['y_' + str(j)] = b_path[:, j][0]
two_d_plot_source = ColumnDataSource(two_d_plot_data)

two_d_plot.xaxis.axis_label = 'age s'
two_d_plot.yaxis.axis_label = 'indiv. savings b'

# create the legend
legend_labels = []
labels = np.append(0, lamcumsum)
for i in range(num_abilities):
    legend_labels.append(str(100*labels[i]) + ' - ' +
                         str(100*labels[i+1]) + '%')

line_styles = ['solid', 'dashed', 'dotted']
line_colors = ['#3288bd', '#009900', '#D49C0E', '#8418C7', '#fc8d59']
line_shapes = ['circle', 'square', 'triangle']
glyphs = []
for j in range(num_abilities):
    y = 'y_' + str(j)

    if j % 4 == 0:
        shape = []
        if line_shapes[j % 3] == 'square':
            shape.append(two_d_plot.square('x', y, fill_color=None,
                                           line_color=line_colors[j % 5],
                                           source=two_d_plot_source))
        elif line_shapes[j % 3] == 'circle':
            shape.append(two_d_plot.circle('x', y,
                                           fill_color=line_colors[j % 5],
                                           line_color=line_colors[j % 5],
                                           source=two_d_plot_source))
        elif line_shapes[j % 3] == 'triangle':
            shape.append(two_d_plot.triangle('x', y,
                                             fill_color=line_colors[j % 5],
                                             line_color=line_colors[j % 5],
                                             source=two_d_plot_source))
        shape.append(two_d_plot.line('x', y, line_color=line_colors[j % 5],
                                     source=two_d_plot_source))
        glyphs.append(shape)

    else:
        glyphs.append([two_d_plot.line('x', y,
                                       line_dash=line_styles[(j % 4)-1],
                                       line_color=line_colors[j % 5],
                                       line_width=2,
                                       source=two_d_plot_source)])

legend_items = []
for i in range(len(legend_labels)):
    legend_items.append((legend_labels[i], glyphs[i]))

legend = Legend(items=legend_items, location=(10, -30))
two_d_plot.add_layout(legend, 'right')

# two d plot sources
two_d_all_source = ColumnDataSource(data=dict(b_path=b_path, c_path=c_path,
                                    n_path=n_path))
two_d_object = ColumnDataSource(data=dict(yaxis=[two_d_plot.yaxis],
                                          title=[two_d_plot.title],
                                          plot=[two_d_plot]))

# LINE GRAPH
# line graph for rpath initially
rpath_value = rpath_value[:time_periods]
time = range(time_periods)
circle_color = ['#3288bd'] + ['white']*(time_periods-1)
line_plot_source = ColumnDataSource(data=dict(x=time, y=rpath_value,
                                    circle_color=circle_color))
line_plot = figure(title='Time path for real interest rate r',
                   plot_width=600, plot_height=300)
line_plot.xaxis.axis_label = 'Period t'
line_plot.yaxis.axis_label = 'real interest rate r'
line_plot.line('x', 'y', line_width=2, source=line_plot_source)
line_plot.circle('x', 'y', fill_color='circle_color', size=8,
                 source=line_plot_source)

# the other path data for the other line plots
rpath = ColumnDataSource(data=dict(x=time, y=rpath_value[:time_periods],
                                   circle_color=circle_color))
wpath = ColumnDataSource(data=dict(x=time, y=wpath_value[:time_periods],
                                   circle_color=circle_color))
kpath = ColumnDataSource(data=dict(x=time, y=kpath_value[:time_periods],
                                   circle_color=circle_color))
lpath = ColumnDataSource(data=dict(x=time, y=lpath_value[:time_periods],
                                   circle_color=circle_color))
ypath = ColumnDataSource(data=dict(x=time, y=ypath_value[:time_periods],
                                   circle_color=circle_color))
cpath = ColumnDataSource(data=dict(x=time, y=cpath_value[:time_periods],
                                   circle_color=circle_color))

line_object = ColumnDataSource(data=dict(yaxis=[line_plot.yaxis],
                                         title=[line_plot.title]))

# callback for the line graph
line_callback = CustomJS(args=dict(line_plot_source=line_plot_source,
                                   rpath=rpath, wpath=wpath, kpath=kpath,
                                   lpath=lpath, ypath=ypath, cpath=cpath,
                                   line_object=line_object),
                         code=LINE_CALLBACK_SCRIPT)

# create buttons for line graph
line_radio_group = RadioButtonGroup(labels=['r(t)', 'w(t)', 'K(t)', 'L(t)',
                                            'Y(t)', 'C(t)'],
                                    active=0, callback=line_callback)
line_callback.args['line_radio_group'] = line_radio_group
# line_radio_group.on_click(line_radio_handler)

# SLIDER
# callback for both graphs from slider
slider_callback = CustomJS(args=dict(source=source, data_info=data_info,
                                     bpath_source=bpath_source,
                                     cpath_source=cpath_source,
                                     npath_source=npath_source,
                                     line_plot_source=line_plot_source,
                                     two_d_plot_source=two_d_plot_source,
                                     two_d_all_source=two_d_all_source,
                                     two_d_object=two_d_object),
                           code=SLIDER_CALLBACK_SCRIPT)

# time slider
time_slider = Slider(start=0, end=time_periods-1, value=0, step=1,
                     title='Time period', callback=slider_callback, width=400)
slider_callback.args['time'] = time_slider

# create 2d plot buttons
two_d_radio_group = RadioButtonGroup(labels=['b(j,s,t)', 'c(j,s,t)',
                                             'n(j,s,t)'], active=0,
                                     callback=slider_callback)
slider_callback.args['two_d_radio_group'] = two_d_radio_group

# buttons for 3D surface
surface_radio_group = RadioButtonGroup(labels=['b(j,s,t)', 'c(j,s,t)',
                                               'n(j,s,t)'],
                                       active=0, callback=slider_callback)
slider_callback.args['surface_radio_group'] = surface_radio_group

# paragraph for explanation
p = Div(text="""<b>The 3D surface shows the relationship between age,
ability, and either inidividual savings, consumption, or labor supply over
time.</b>""", width=400, height=100)

# create layout to place all items
surface_column = column(surface, surface_radio_group)
two_d_column = column(two_d_plot, two_d_radio_group)
line_column = column(line_plot, line_radio_group)
slider_column = column(p, time_slider)
layout = gridplot(
    children=[[surface_column, slider_column],
              [line_column, two_d_column]],
    toolbar_location=None
)

js, div = components(layout)
cdn_js = CDN.js_files[0]
cdn_css = CDN.css_files[0]

if 'show' in sys.argv:
    show(layout)
