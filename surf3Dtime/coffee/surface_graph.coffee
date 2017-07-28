import * as p from "core/properties"
import {LayoutDOM, LayoutDOMView} from "models/layouts/layout_dom"

# This defines some default options for the Graph3d feature of vis.js
OPTIONS =
  width:  '600px'
  height: '390px'
  style: 'surface'
  showPerspective: true
  showGrid: true
  keepAspectRatio: false
  verticalRatio: 1.0
  showLegend: true
  cameraPosition:
    horizontal: -0.35
    vertical: 0.22
    distance: 2.6
  xLabel: 'age-s'
  yLabel: 'ability-j'
  zLabel: 'indiv. savings-b'
  zMin: -31.038196332661578
  zMax: 65.22289937437553

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

    window.surface_graph = @_graph

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
