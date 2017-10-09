# importing some libraries
import pandas as pd
from os import path
from math import pi
import sys

# importing Bokeh libraries
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, CustomJS, Slider, LabelSet
from bokeh.layouts import column, layout
from bokeh.io import output_file, show
from bokeh.models import FuncTickFormatter, FactorRange
from bokeh.embed import components
from bokeh.resources import CDN
pd.options.mode.chained_assignment = None

# define the years of interest
years = [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026]

# load data as DataFrame and process data in an appropriate format
sources = {}
sources_df = {}

# prepare data
for year in years:
    if 'show' is sys.argv:
        path = 'data/14814_'+str(year)+'_difference_combined_bins.csv'
    else:
        path = 'increase_decrease/data/14814_'+str(year)+'_difference_combined_bins.csv'

    sources = pd.DataFrame(pd.read_csv(path, decimal=",", encoding='utf-8-sig', header=1))
    sources = sources.rename(columns={'Unnamed: 0': 'Intervals'})
    # drop the first and the last row (first row contains units and last one source)
    sources_dropped = sources.drop(sources.index[[0,len(sources['Tax Units with Tax Cut'])-1]])
    # extract the columns that we are interested in
    df_data = sources_dropped[['Intervals', 'Tax Units with Tax Cut', 'Tax Units with Tax Increase', 'Average Tax Change']]
    # assign the name "Intervals" to the first column
    intervals = df_data['Intervals']
    # change the format of the data to be float
    # and make the tax-cut data to be negative
    df_data['Tax Units with Tax Cut'] = [x.replace(',', '.') for x in df_data['Tax Units with Tax Cut']]
    df_data['Tax Units with Tax Cut'] = (-1)*df_data['Tax Units with Tax Cut'].astype(float)
    df_data['Tax Units with Tax Increase'] = [x.replace(',', '.') for x in df_data['Tax Units with Tax Increase']]
    df_data['Tax Units with Tax Increase'] = df_data['Tax Units with Tax Increase'].astype(float)
    # transform ColumnDataFrame to ColumnDataSource and assign the year
    sources_df['_' + str(year)] = ColumnDataSource(df_data)

# we can also create a corresponding dictionary_of_sources object, where the
# keys are integers and the values are the references to our ColumnDataSources from above:
dictionary_of_sources = dict(zip([x for x in years], ['_%s' % x for x in years]))
js_source_array = str(dictionary_of_sources).replace("'", "")

# we start from the first year of data, which is our initial source
renderer_source = ColumnDataSource(data=sources_df['_%s' % years[0]].data.copy())
# renderer_source.data = sources_df['_%s' % years[0]].data.copy()

label_source = ColumnDataSource({'text': [str(years[0])]})
label = LabelSet(x=0.5, y=600, text='text', level='glyph', source=label_source,
                 render_mode='canvas', text_font_size='50pt', text_color='#0569CE')

# add the Bar graph
p = figure(plot_width=600, plot_height=500, y_range=[-1000, 1000],
           x_range=FactorRange(*renderer_source.data['Intervals']),
           tools="box_zoom, reset, save")
p.toolbar.logo = None

p.vbar(top='Tax Units with Tax Increase', x='Intervals', width=0.4,
       color='orange', source=renderer_source)
p.vbar(top='Tax Units with Tax Cut', x='Intervals', width=0.4, color='silver',
       source=renderer_source)
p.xaxis.axis_label = 'Income [$ thousands]'
p.xaxis.major_label_orientation = pi/4
p.yaxis.axis_label = 'Tax Units with Tax Cut            Tax Units with Tax Increase'
p.yaxis.major_label_orientation = "vertical"

# add the text as a glyph
p.add_layout(label)

# Create the "Average tax" figure
s1 = figure(plot_width=600, plot_height=250, y_range=[-800, 300],
            x_range=FactorRange(*renderer_source.data['Intervals']),
            title='Average Tax Change', tools="box_zoom, reset, save")
s1.toolbar.logo = None
s1.title.text_color = '#0569CE'
s1.xaxis.major_label_orientation = pi/4

s1.line('Intervals', 'Average Tax Change', line_color='#0569CE', line_width=2,
        source=renderer_source)
s1.circle('Intervals', 'Average Tax Change', fill_color="white", size=8,
          source=renderer_source)

# Add the slider
code = """
    var sources = %s;
    var year = slider.value;
    var new_source_data = sources[year].data;
    var data = renderer_source.data;

    for (i = 0; i < data['index'].length; i++){
        debugger;
        renderer_source.data['Average Tax Change'][i] = new_source_data['Average Tax Change'][i];
        data['Intervals'][i] = new_source_data['Intervals'][i];
        data['Tax Units with Tax Cut'][i] = new_source_data['Tax Units with Tax Cut'][i];
        data['Tax Units with Tax Increase'][i] = new_source_data['Tax Units with Tax Increase'][i];
    }

    for (i=0; i < label_source.data['text'].length; i++){
        label_source.data['text'][i] = String(year);
    }

    label_source.change.emit();
    renderer_source.change.emit();
""" % js_source_array

callback = CustomJS(args=sources_df, code=code)
slider = Slider(start=years[0], end=years[-1], value=years[0], step=1,
                title="Year", callback=callback)
callback.args["renderer_source"] = renderer_source
callback.args["slider"] = slider
callback.args["label_source"] = label_source

p_l = column(s1, p)
lay_out = layout([[p_l], [slider]])

if 'show' in sys.argv:
    show(lay_out)

js, div = components(lay_out)
cdn_js = CDN.js_files[0]
cdn_css = CDN.css_files[0]
widget_js = CDN.js_files[1]
widget_css = CDN.css_files[1]
