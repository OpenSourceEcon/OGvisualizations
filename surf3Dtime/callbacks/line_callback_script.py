LINE_CALLBACK_SCRIPT = """
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
"""
