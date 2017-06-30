from __future__ import division

import numpy as np
import pickle

from bokeh.core.properties import Instance, String
from bokeh.models import ColumnDataSource, LayoutDOM, CustomJS, Slider
from bokeh.layouts import layout, widgetbox, gridplot
from bokeh.plotting import figure
from bokeh.io import show

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
  zMax: 4
  zMin: -1
  tooltip: false

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
tpi_args = pickle.load(open('HeteroAbil/OUTPUT/TPI/tpi_args.pkl', 'rb'))
tpi_vars = pickle.load(open('HeteroAbil/OUTPUT/TPI/tpi_vars.pkl', 'rb'))
ss_vars = pickle.load(open('HeteroAbil/OUTPUT/SS/ss_vars.pkl', 'rb'))

# 3D plot for bpath
S = tpi_args[1]
lambdas = tpi_args[4]

sgrid = np.arange(1, S + 1)
lamcumsum = lambdas.cumsum()
jmidgrid = 0.5 * lamcumsum + 0.5 * (lamcumsum - lambdas)
smat, jmat = np.meshgrid(sgrid, jmidgrid)
smat = smat.ravel()
jmat = jmat.ravel()
value = tpi_vars['bpath'].T[0]
value = value.ravel()
bpath_ravel = tpi_vars['bpath'].T.ravel()

source = ColumnDataSource(data=dict(x=smat, y=jmat, z=value,
                          color=value))
bpath_source = ColumnDataSource(data=dict(bpath=bpath_ravel))

surface = Surface3d(x="x", y="y", z="z", color="color", data_source=source)

# line graph for Kpath
kpath = tpi_vars['Kpath'][:69]
time = range(69)
circle_color = ['blue'] + ['white']*68
kplot_source = ColumnDataSource(data=dict(x=time, y=kpath,
                                circle_color=circle_color))

kplot = figure(title='Time path for aggregate capital stock K', plot_width=500,
               plot_height=300)
kplot.xaxis.axis_label = 'Period t'
kplot.yaxis.axis_label = 'Aggregate capital K'
kplot.line('x', 'y', line_width=2, source=kplot_source)
kplot.circle('x', 'y', fill_color='circle_color', size=8, source=kplot_source)

# line graph for Lpath
lpath = tpi_vars['Lpath'][:69]
lplot_source = ColumnDataSource(data=dict(x=time, y=lpath,
                                circle_color=circle_color))

lplot = figure(title='Time path for aggregate labor L', plot_width=500,
               plot_height=300)
lplot.xaxis.axis_label = 'Period t'
lplot.yaxis.axis_label = 'Aggregate labor L'
lplot.line('x', 'y', line_width=2, source=lplot_source)
lplot.circle('x', 'y', fill_color='circle_color', size=8, source=lplot_source)

# 2D plot for bpath
bpath = ss_vars['bpath']
# try ss output for b_ss
import pdb;pdb.set_trace()
bplot_source = ColumnDataSource(data=dict(x=sgrid, y=bpath))
bplot = figure(title='Individual Savings by Age', plot_width=500,
               plot_height=300)
bplot.xaxis.axis_label = 'age-s'
bplot.yaxis.axis_label = 'indiv. savings-b'
bplot.line('x', 'y', line_width=2, line_dash='dashed', source=bplot_source)
#bplot.line()
#bplot.line()

# callback for both graphs
callback = CustomJS(args=dict(source=source, bpath_source=bpath_source,
                    kplot_source=kplot_source, lplot_source=lplot_source),
                    code="""
    var data = source.data;
    var bdata = bpath_source.data;
    var kdata = kplot_source.data;
    var ldata = lplot_source.data;
    var time = time.value;
    x = data['x'];
    y = data['y'];
    z = data['z'];

    beg = time*80;
    end = (time+1)*80;
    b = bdata['bpath'].slice(beg,end);

    for (i = 0; i < z.length; i++) {
            z[i] = b[i];
    }

    kdata['circle_color'] = Array(69).fill('white');
    kdata['circle_color'][time] = 'blue';

    ldata['circle_color']= Array(69).fill('white');
    ldata['circle_color'][time] = 'blue';

    source.change.emit();
    kplot_source.change.emit();
    lplot_source.change.emit();
""")

# time slider
time_slider = Slider(start=0, end=68, value=0, step=1, title='Time period',
                     callback=callback)
callback.args['time'] = time_slider

# layout = layout([
#     [surface],
#     [kplot, lplot],
#     [widgetbox(time_slider)],
#     ])

layout = gridplot(
    children=[[surface], [kplot, lplot], [bplot], [widgetbox(time_slider)]],
    toolbar_location='right',
    # sizing_mode='stretch_both',
    toolbar_options=dict(logo='grey'),
)

show(layout)
