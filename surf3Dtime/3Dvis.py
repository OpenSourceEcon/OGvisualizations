import numpy as np
import pickle
import os

from bokeh.core.properties import Instance, String
from bokeh.models import ColumnDataSource, LayoutDOM, CustomJS, Slider, Legend
from bokeh.layouts import layout, widgetbox, gridplot
from bokeh.models.widgets import RadioButtonGroup
from bokeh.plotting import figure, curdoc

from callbacks.surface_callback_script import SURFACE_CALLBACK_SCRIPT
from callbacks.line_callback_script import LINE_CALLBACK_SCRIPT
from callbacks.slider_callback_script import SLIDER_CALLBACK_SCRIPT


class Surface3d(LayoutDOM):
    __implementation__ = "coffee/surface_graph.coffee"

    data_source = Instance(ColumnDataSource)

    x = String
    y = String
    z = String
    color = String


# DATA
tpi_args = pickle.load(open('surf3Dtime/HeteroAbil/s80j7/OUTPUT/TPI/tpi_args.pkl', 'rb'))
tpi_vars = pickle.load(open('surf3Dtime/HeteroAbil/s80j7/OUTPUT/TPI/tpi_vars.pkl', 'rb'))
ss_vars = pickle.load(open('surf3Dtime/HeteroAbil/s80j7/OUTPUT/SS/ss_vars.pkl', 'rb'))

S = tpi_args[1]
lambdas = tpi_args[4]

sgrid = np.arange(1, S + 1)
lamcumsum = lambdas.cumsum()
jmidgrid = 0.5 * lamcumsum + 0.5 * (lamcumsum - lambdas)
smat, jmat = np.meshgrid(sgrid, jmidgrid)
smat = smat.ravel()
jmat = jmat.ravel()

bvalue = tpi_vars['bpath'].T[0]
bvalue = bvalue.ravel()
bpath_ravel = tpi_vars['bpath'].T.ravel()

cvalue = tpi_vars['cpath'].T[0]
cvalue = cvalue.ravel()
cpath_ravel = tpi_vars['cpath'].T.ravel()

nvalue = tpi_vars['npath'].T[0]
nvalue = nvalue.ravel()
npath_ravel = tpi_vars['npath'].T.ravel()

# data for 2D plot
b_ss = ss_vars['b_ss']
c_ss = ss_vars['c_ss']
n_ss = ss_vars['n_ss']
two_d_all_sources = ColumnDataSource(data=dict(b_ss=b_ss, c_ss=c_ss,
                                     n_ss=n_ss))

# import pdb; pdb.set_trace()

source = ColumnDataSource(data=dict(x=smat, y=jmat, z=bvalue, color=bvalue))
bsource = ColumnDataSource(data=dict(x=smat, y=jmat, z=bvalue, color=bvalue))
csource = ColumnDataSource(data=dict(x=smat, y=jmat, z=cvalue, color=cvalue))
nsource = ColumnDataSource(data=dict(x=smat, y=jmat, z=nvalue, color=nvalue))

bpath_source = ColumnDataSource(data=dict(bpath=bpath_ravel))
cpath_source = ColumnDataSource(data=dict(cpath=cpath_ravel))
npath_source = ColumnDataSource(data=dict(npath=npath_ravel))

# 3D SURFACE
surface = Surface3d(x="x", y="y", z="z", color="color", data_source=source)

# callback for 3D surface
surface_callback = CustomJS(args=dict(source=source, bsource=bsource,
                            csource=csource, nsource=nsource,
                            surface=surface),
                            code=SURFACE_CALLBACK_SCRIPT)

# buttons for 3D surface
surface_radio_group = RadioButtonGroup(labels=['b(j,s,t)', 'c(j,s,t)',
                                               'n(j,s,t)'],
                                       active=0,
                                       callback=surface_callback)
surface_callback.args['surface_radio_group'] = surface_radio_group

# 2D PLOT
# create 2d plot buttons
two_d_radio_group = RadioButtonGroup(labels=['b(j,s,t)', 'c(j,s,t)',
                                             'n(j,s,t)'], active=0)


# listener and function for altering the 2D plot
def two_d_radio_handler(new):
    data = dict(x=sgrid)
    if new == 0:
        two_d_plot.yaxis.axis_label = 'indiv. savings b'
        for j in range(num_abilities):
            data['y_' + str(j)] = b_ss[:, j]

        two_d_plot_source.data = data
    if new == 1:
        two_d_plot.yaxis.axis_label = 'indiv. consumption c'
        for j in range(num_abilities):
            data['y_' + str(j)] = c_ss[:, j]

        two_d_plot_source.data = data
    if new == 2:
        two_d_plot.yaxis.axis_label = 'labor supply n'
        for j in range(num_abilities):
            data['y_' + str(j)] = n_ss[:, j]

        two_d_plot_source.data = data


two_d_radio_group.on_click(two_d_radio_handler)

# create 2d plot
num_abilities = 7
two_d_plot = figure(plot_width=600, plot_height=300)
two_d_plot_data = dict(x=sgrid)
for j in range(num_abilities):
    two_d_plot_data['y_' + str(j)] = b_ss[:, j]
two_d_plot_source = ColumnDataSource(two_d_plot_data)

two_d_plot.xaxis.axis_label = 'age s'
two_d_plot.yaxis.axis_label = 'indiv. savings b'

line_styles = ['solid', 'dashed', 'dotted', 'dotdash', 'dashdot']
line_colors = ['#3288bd', '#009900', '#552A86', '#fee08b', '#fc8d59']
glyph_list = []
for j in range(num_abilities):
    y = 'y_' + str(j)
    if j <= 4:
        glyph_list.append(two_d_plot.line('x', y, line_dash=line_styles[j],
                                          line_color=line_colors[j],
                                          line_width=2,
                                          source=two_d_plot_source))
    if j == 5:
        glyph_list.append(two_d_plot.square('x', y, fill_color=None,
                                            line_color=line_colors[j-5],
                                            source=two_d_plot_source))
        glyph_list.append(two_d_plot.line('x', y, line_color=line_colors[j-5],
                                          source=two_d_plot_source))
    if j == 6:
        glyph_list.append(two_d_plot.circle('x', y,
                                            fill_color=line_colors[j-5],
                                            line_color=line_colors[j-5],
                                            source=two_d_plot_source))
        glyph_list.append(two_d_plot.line('x', y, line_color=line_colors[j-5],
                                          source=two_d_plot_source))

legend = Legend(items=[
    ('0 - 25%', [glyph_list[0]]),
    ('25 - 50%', [glyph_list[1]]),
    ('50 - 70%', [glyph_list[2]]),
    ('70 - 80%', [glyph_list[3]]),
    ('80 - 90%', [glyph_list[4]]),
    ('90 - 99%', [glyph_list[5], glyph_list[6]]),
    ('99 - 100%', [glyph_list[7], glyph_list[8]]),
], location=(10, -30))

two_d_plot.add_layout(legend, 'right')

# LINE GRAPH
# line graph for Kpath initially
time_periods = 80
kpath = tpi_vars['Kpath'][:time_periods]
time = range(time_periods)
circle_color = ['#3288bd'] + ['white']*(time_periods-1)
line_plot_source = ColumnDataSource(data=dict(x=time, y=kpath,
                                    circle_color=circle_color))
line_plot = figure(title='Time path for aggregate capital stock K',
                   plot_width=500, plot_height=300)
line_plot.xaxis.axis_label = 'Period t'
line_plot.yaxis.axis_label = 'Aggregate capital K'
line_plot.line('x', 'y', line_width=2, source=line_plot_source)
line_plot.circle('x', 'y', fill_color='circle_color', size=8,
                 source=line_plot_source)

# the other path data for the other line plots
rpath = ColumnDataSource(data=dict(x=time, y=tpi_vars['rpath'][:time_periods],
                                   circle_color=circle_color))
wpath = ColumnDataSource(data=dict(x=time, y=tpi_vars['wpath'][:time_periods],
                                   circle_color=circle_color))
kpath = ColumnDataSource(data=dict(x=time, y=tpi_vars['Kpath'][:time_periods],
                                   circle_color=circle_color))
lpath = ColumnDataSource(data=dict(x=time, y=tpi_vars['Lpath'][:time_periods],
                                   circle_color=circle_color))
ypath = ColumnDataSource(data=dict(x=time, y=tpi_vars['Ypath'][:time_periods],
                                   circle_color=circle_color))
cpath = ColumnDataSource(data=dict(x=time, y=tpi_vars['Cpath'][:time_periods],
                                   circle_color=circle_color))

# callback for the line graph
line_callback = CustomJS(args=dict(line_plot_source=line_plot_source,
                                   rpath=rpath, wpath=wpath, kpath=kpath,
                                   lpath=lpath, ypath=ypath, cpath=cpath),
                         code=LINE_CALLBACK_SCRIPT)


# change the text for the line plot depending on data source
def line_radio_handler(new):
    if new == 0:
        line_plot.title.text = 'Time path for real interest rate r'
        line_plot.yaxis.axis_label = 'Real interest rate r'
    elif new == 1:
        line_plot.title.text = 'Time path for real wage w'
        line_plot.yaxis.axis_label = 'Real wage w'
    elif new == 2:
        line_plot.title.text = 'Time path for aggregate capital stock K'
        line_plot.yaxis.axis_label = 'Aggregate capital K'
    elif new == 3:
        line_plot.title.text = 'Time path for aggregate labor L'
        line_plot.yaxis.axis_label = 'Aggregate labor L'
    elif new == 4:
        line_plot.title.text = 'Time path for aggregate output (GDP) Y'
        line_plot.yaxis.axis_label = 'Aggregate output Y'
    elif new == 5:
        line_plot.title.text = 'Time path for aggregate consumption C'
        line_plot.yaxis.axis_label = 'Aggregate consumption C'


# create buttons for line graph
line_radio_group = RadioButtonGroup(labels=['r(t)', 'w(t)', 'K(t)', 'L(t)',
                                            'Y(t)', 'C(t)'],
                                    active=2, callback=line_callback)
line_callback.args['line_radio_group'] = line_radio_group
line_radio_group.on_click(line_radio_handler)

# SLIDER
# callback for both graphs from slider
slider_callback = CustomJS(args=dict(source=source, bpath_source=bpath_source,
                                     cpath_source=cpath_source,
                                     npath_source=npath_source,
                                     line_plot_source=line_plot_source,
                                     two_d_plot_source=two_d_plot_source,
                                     two_d_all_sources=two_d_all_sources),
                           code=SLIDER_CALLBACK_SCRIPT)

# time slider
time_slider = Slider(start=0, end=79, value=0, step=1, title='Time period',
                     callback=slider_callback)
slider_callback.args['time'] = time_slider
slider_callback.args['surface_radio_group'] = surface_radio_group

# create layout to place all items
layout = gridplot(
    children=[[surface], [widgetbox(surface_radio_group)],
              [line_plot, widgetbox(line_radio_group)],
              [two_d_plot, two_d_radio_group],
              [widgetbox(time_slider)]],
    toolbar_location=None
)

# add the layout to the document
curdoc().add_root(layout)
