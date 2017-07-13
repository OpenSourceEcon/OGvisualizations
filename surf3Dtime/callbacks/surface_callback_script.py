SURFACE_CALLBACK_SCRIPT = """
var button = surface_radio_group.active;

if (button == '0') {
var source_data = source.data;
var data = bsource.data;
var bdata = data['z']

window.surface_graph.setOptions({zLabel: 'indiv. savings-b', zMin: -20,
zMax: 50})

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

window.surface_graph.setOptions({zLabel: 'indiv. consumption-c',
zMin: 0, zMax: 6})

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

window.surface_graph.setOptions({zLabel: 'labor supply-n', zMin: 0,
zMax: 1})

x = source_data['x'];
y = source_data['y'];
z = source_data['z'];

for (i = 0; i < z.length; i++) {
z[i] = ndata[i];
}
source.change.emit();
}
"""
