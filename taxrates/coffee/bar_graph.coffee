import * as p from "core/properties"
import {LayoutDOM, LayoutDOMView} from "models/layouts/layout_dom"

# This defines some default options for the Graph3d feature of vis.js
OPTIONS =
  width:  '600px'
  height: '390px'
  style: 'bar'
  showPerspective: true
  showGrid: true
  keepAspectRatio: false
  verticalRatio: 1.0
  showLegend: true
  cameraPosition:
    horizontal: -0.35
    vertical: 0.22
    distance: 2.6
  xLabel: 'Total Labor Income'
  yLabel: 'Total Capital Income'
  zLabel: 'Percent of Obs.'
  xBarWidth: 7500
  yBarWidth: 7500

export class Bar3dView extends LayoutDOMView

  initialize: (options) ->
    super(options)

    url = "https://cdnjs.cloudflare.com/ajax/libs/vis/4.16.1/vis.min.js"

    window.visjsInits ||= []
    window.visjsInits.push(() => @_init())

    visjsCdnTag = document.querySelector("script[src=\"#{url}\"]")

    unless visjsCdnTag?
      script = document.createElement('script')
      script.src = url
      script.async = false
      script.onreadystatechange = script.onload = () =>
        for initFunction in window.visjsInits
          initFunction()
      document.querySelector("head").appendChild(script)

  _init: () ->
    @_bar_graph = new vis.Graph3d(@el, @get_data(), OPTIONS)

    @connect(@model.data_source.change, () =>
        @_bar_graph.setData(@get_data())
    )

  get_data: () ->
    data = new vis.DataSet()
    source = @model.data_source
    for i in [0...source.get_length()]
      data.add({
        x:     source.get_column(@model.x)[i]
        y:     source.get_column(@model.y)[i]
        z:     source.get_column(@model.z)[i]
      })
    return data

export class Bar3d extends LayoutDOM

  default_view: Bar3dView

  type: "Bar3d"

  @define {
    x:           [ p.String           ]
    y:           [ p.String           ]
    z:           [ p.String           ]
    color:       [ p.String           ]
    data_source: [ p.Instance         ]
  }
