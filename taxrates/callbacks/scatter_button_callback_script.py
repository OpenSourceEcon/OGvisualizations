SCATTER_BUTTON_CALLBACK_SCRIPT = """
var button = scatter_buttons.active;

if (button == '0') {
    var source = scatter_source.data;
    var zdata = etr_source.data;

    x = source['x'];
    y = source['y'];
    z = source['z'];

    for (i = 0; i < z.length; i++) {
        z[i] = zdata['z'][i];
    }
}

if (button == '1') {
    var source = scatter_source.data;
    var zdata = mtrx_source.data;

    x = source['x'];
    y = source['y'];
    z = source['z'];

    for (i = 0; i < z.length; i++) {
        z[i] = zdata['z'][i];
    }
}

if (button == '2') {
    var source = scatter_source.data;
    var zdata = mtry_source.data;

    x = source['x'];
    y = source['y'];
    z = source['z'];

    for (i = 0; i < z.length; i++) {
        z[i] = zdata['z'][i];
    }
}
"""
