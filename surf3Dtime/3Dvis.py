from __future__ import division

import numpy as np
import pickle

from bokeh.core.properties import Instance, String
from bokeh.models import ColumnDataSource, LayoutDOM, CustomJS, Slider
from bokeh.layouts import layout, widgetbox, gridplot
from bokeh.models.widgets import RadioButtonGroup
from bokeh.plotting import figure, curdoc

JS_CODE = """
import * as p from "core/properties"
import {LayoutDOM, LayoutDOMView} from "models/layouts/layout_dom"

# This defines some default options for the Graph3d feature of vis.js
# See: http://visjs.org/graph3d_examples.html for more details.
OPTIONS =
  width:  '450px'
  height: '450px'
  style: 'surface'
  showPerspective: true
  showGrid: true
  keepAspectRatio: false
  verticalRatio: 1.0
  showLegend: true
  cameraPosition:
    horizontal: -0.35
    vertical: 0.22
    distance: 1.8
  xLabel: 'age-s'
  yLabel: 'ability-j'
  zLabel: 'indiv. savings-b'
  zMin: -20
  zMax: 50

export class Surface3dView extends LayoutDOMView

  initialize: (options) ->
    super(options)

    url = "https://cdnjs.cloudflare.com/ajax/libs/vis/4.16.1/vis.min.js"

    script = document.createElement('script')
    script.src = url
    script.async = false
    script.onreadystatechange = script.onload = () => @_init()
    document.querySelector("head").appendChild(script)

  _init: () ->
    @_graph = new vis.Graph3d(@el, @get_data(), OPTIONS)

    @connect(@model.data_source.change, () =>
        @_graph.setData(@get_data())
    )

  get_data: () ->
    data = new vis.DataSet()
    source = @model.data_source
    for i in [0...source.get_length()]
      data.add({
        x:     source.get_column(@model.x)[i]
        y:     source.get_column(@model.y)[i]
        z:     source.get_column(@model.z)[i]
        style: source.get_column(@model.color)[i]
      })
    return data

export class Surface3d extends LayoutDOM

  default_view: Surface3dView

  type: "Surface3d"

  @define {
    x:           [ p.String           ]
    y:           [ p.String           ]
    z:           [ p.String           ]
    color:       [ p.String           ]
    data_source: [ p.Instance         ]
  }
"""


class Surface3d(LayoutDOM):
    __implementation__ = JS_CODE

    data_source = Instance(ColumnDataSource)

    x = String
    y = String
    z = String
    color = String


# read in data
tpi_args = pickle.load(open('HeteroAbil/s80j7/OUTPUT/TPI/tpi_args.pkl', 'rb'))
tpi_vars = pickle.load(open('HeteroAbil/s80j7/OUTPUT/TPI/tpi_vars.pkl', 'rb'))
# ss_vars = pickle.load(open('HeteroAbil/OUTPUT/SS/ss_vars.pkl', 'rb'))

# 3D plot for bpath
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

source = ColumnDataSource(data=dict(x=smat, y=jmat, z=bvalue, color=bvalue))
bsource = ColumnDataSource(data=dict(x=smat, y=jmat, z=bvalue, color=bvalue))
csource = ColumnDataSource(data=dict(x=smat, y=jmat, z=cvalue, color=cvalue))
nsource = ColumnDataSource(data=dict(x=smat, y=jmat, z=nvalue, color=nvalue))

bpath_source = ColumnDataSource(data=dict(bpath=bpath_ravel))
cpath_source = ColumnDataSource(data=dict(cpath=cpath_ravel))
npath_source = ColumnDataSource(data=dict(npath=npath_ravel))

surface = Surface3d(x="x", y="y", z="z", color="color", data_source=source)

# radio buttons and callback for 3D surfaces
surface_callback = CustomJS(args=dict(source=source, bsource=bsource,
                            csource=csource, nsource=nsource), code="""
    var button = surface_radio_group.active;

    if (button == '0') {
        var source_data = source.data;
        var data = bsource.data;
        var bdata = data['z']

        x = source_data['x'];
        y = source_data['y'];
        z = source_data['z'];

        for (i = 0; i < z.length; i++) {
                z[i] = bdata[i];
        }
        source.change.emit();
    }

    if (button == '1') {
        var source_data = source.data;
        var data = csource.data;
        var cdata = data['z'];

        x = source_data['x'];
        y = source_data['y'];
        z = source_data['z'];

        for (i = 0; i < z.length; i++) {
                z[i] = cdata[i];
        }
        source.change.emit();
    }

    if (button == '2') {
        var source_data = source.data;
        var data = nsource.data;
        var ndata = data['z'];

        x = source_data['x'];
        y = source_data['y'];
        z = source_data['z'];

        for (i = 0; i < z.length; i++) {
                z[i] = ndata[i];
        }
        source.change.emit();
    }
""")
surface_radio_group = RadioButtonGroup(labels=['B', 'C', 'N'], active=0,
                                       callback=surface_callback)
surface_callback.args['surface_radio_group'] = surface_radio_group

# line graph for Kpath
kpath = tpi_vars['Kpath'][:80]
time = range(80)
circle_color = ['blue'] + ['white']*79
kplot_source = ColumnDataSource(data=dict(x=time, y=kpath,
                                circle_color=circle_color))

kplot = figure(title='Time path for aggregate capital stock K', plot_width=500,
               plot_height=300)
kplot.xaxis.axis_label = 'Period t'
kplot.yaxis.axis_label = 'Aggregate capital K'
kplot.line('x', 'y', line_width=2, source=kplot_source)
kplot.circle('x', 'y', fill_color='circle_color', size=8, source=kplot_source)

# the other path data for the other line plots
rpath = ColumnDataSource(data=dict(x=time, y=tpi_vars['rpath'][:80],
                                   circle_color=circle_color))
wpath = ColumnDataSource(data=dict(x=time, y=tpi_vars['wpath'][:80],
                                   circle_color=circle_color))
kpath = ColumnDataSource(data=dict(x=time, y=tpi_vars['Kpath'][:80],
                                   circle_color=circle_color))
lpath = ColumnDataSource(data=dict(x=time, y=tpi_vars['Lpath'][:80],
                                   circle_color=circle_color))
ypath = ColumnDataSource(data=dict(x=time, y=tpi_vars['Ypath'][:80],
                                   circle_color=circle_color))
cpath = ColumnDataSource(data=dict(x=time, y=tpi_vars['Cpath'][:80],
                                   circle_color=circle_color))


# radio buttons and callback for line graph
line_callback = CustomJS(args=dict(kplot_source=kplot_source, rpath=rpath,
                                   wpath=wpath, kpath=kpath, lpath=lpath,
                                   ypath=ypath, cpath=cpath), code="""
    var button = line_radio_group.active;

    if (button == '0') {
        var source = kplot_source.data;
        var path_data = rpath.data;

        x = source['x'];
        y = source['y'];

        for (i = 0; i < y.length; i++) {
                y[i] = path_data['y'][i];
        }
        kplot_source.change.emit();
    }

    if (button == '1') {
        var source = kplot_source.data;
        var path_data = wpath.data;

        x = source['x'];
        y = source['y'];

        for (i = 0; i < y.length; i++) {
                y[i] = path_data['y'][i];
        }
        kplot_source.change.emit();
    }

    if (button == '2') {
        var source = kplot_source.data;
        var path_data = kpath.data;

        x = source['x'];
        y = source['y'];

        for (i = 0; i < y.length; i++) {
                y[i] = path_data['y'][i];
        }
        kplot_source.change.emit();
    }

    if (button == '3') {
        var source = kplot_source.data;
        var path_data = lpath.data;

        x = source['x'];
        y = source['y'];

        for (i = 0; i < y.length; i++) {
                y[i] = path_data['y'][i];
        }
        kplot_source.change.emit();
    }

    if (button == '4') {
        var source = kplot_source.data;
        var path_data = ypath.data;

        x = source['x'];
        y = source['y'];

        for (i = 0; i < y.length; i++) {
                y[i] = path_data['y'][i];
        }
        kplot_source.change.emit();
    }

    if (button == '5') {
        var source = kplot_source.data;
        var path_data = cpath.data;

        x = source['x'];
        y = source['y'];

        for (i = 0; i < y.length; i++) {
                y[i] = path_data['y'][i];
        }
        kplot_source.change.emit();
    }
""")


def my_radio_handler(new):
    if new == 0:
        kplot.title.text = 'Time path for real interest rate r'
        kplot.yaxis.axis_label = 'Real interest rate r'
    elif new == 1:
        kplot.title.text = 'Time path for real wage w'
        kplot.yaxis.axis_label = 'Real wage w'
    elif new == 2:
        kplot.title.text = 'Time path for aggregate capital stock K'
        kplot.yaxis.axis_label = 'Aggregate capital K'
    elif new == 3:
        kplot.title.text = 'Time path for aggregate labor L'
        kplot.yaxis.axis_label = 'Aggregate labor L'
    elif new == 4:
        kplot.title.text = 'Time path for aggregate output (GDP) Y'
        kplot.yaxis.axis_label = 'Aggregate output Y'
    elif new == 5:
        kplot.title.text = 'Time path for aggregate consumption C'
        kplot.yaxis.axis_label = 'Aggregate consumption C'


line_radio_group = RadioButtonGroup(labels=['r', 'w', 'K', 'L', 'Y', 'C'],
                                    active=2, callback=line_callback)
line_callback.args['line_radio_group'] = line_radio_group
line_radio_group.on_click(my_radio_handler)

# callback for both graphs
slider_callback = CustomJS(args=dict(source=source, bpath_source=bpath_source,
                                     cpath_source=cpath_source,
                                     npath_source=npath_source,
                                     kplot_source=kplot_source),
                           code="""
    var data = source.data;
    var kdata = kplot_source.data;
    var time = time.value;
    var button = surface_radio_group.active;
    var plot_points = 560;

    if (button == '0') {
        var bpath = bpath_source.data;

        x = data['x'];
        y = data['y'];
        z = data['z'];

        beg = time*plot_points;
        end = (time+1)*plot_points;
        b = bpath['bpath'].slice(beg,end);

        for (i = 0; i < z.length; i++) {
                z[i] = b[i];
        }
        source.change.emit();
    }

    if (button == '1') {
        var cpath = cpath_source.data;

        x = data['x'];
        y = data['y'];
        z = data['z'];

        beg = time*plot_points;
        end = (time+1)*plot_points;
        c = cpath['cpath'].slice(beg,end);

        for (i = 0; i < z.length; i++) {
                z[i] = c[i];
        }
        source.change.emit();
    }

    if (button == '2') {
        var npath = npath_source.data;

        x = data['x'];
        y = data['y'];
        z = data['z'];

        beg = time*plot_points;
        end = (time+1)*plot_points;
        n = npath['npath'].slice(beg,end);

        for (i = 0; i < z.length; i++) {
                z[i] = n[i];
        }
        source.change.emit();
    }

    kdata['circle_color'] = Array(80).fill('white');
    kdata['circle_color'][time] = 'blue';

    kplot_source.change.emit();
""")

# time slider
time_slider = Slider(start=0, end=79, value=0, step=1, title='Time period',
                     callback=slider_callback)
slider_callback.args['time'] = time_slider
slider_callback.args['surface_radio_group'] = surface_radio_group

layout = gridplot(
    children=[[surface], [widgetbox(surface_radio_group)],
              [kplot, widgetbox(line_radio_group)], [widgetbox(time_slider)]],
    toolbar_location='right',
    # sizing_mode='stretch_both',
    toolbar_options=dict(logo='grey'),
)

# put the button and plot in a layout and add to the document
curdoc().add_root(layout)
