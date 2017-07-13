SLIDER_CALLBACK_SCRIPT = """
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
"""
