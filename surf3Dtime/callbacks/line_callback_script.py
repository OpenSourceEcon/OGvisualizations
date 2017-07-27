LINE_CALLBACK_SCRIPT = """
var button = line_radio_group.active;
var line_object = line_object.data;

if (button == '0') {
    var source = line_plot_source.data;
    var path_data = rpath.data;
    line_object.title[0].attributes.text =
        'Time path for real interest rate r';
    line_object.yaxis[0][0].attributes.axis_label = 'real interest rate r';

    x = source['x'];
    y = source['y'];

    for (i = 0; i < y.length; i++) {
        y[i] = path_data['y'][i];
        }
    line_plot_source.change.emit();
}

if (button == '1') {
    var source = line_plot_source.data;
    var path_data = wpath.data;
    line_object.title[0].attributes.text = 'Time path for real wage w';
    line_object.yaxis[0][0].attributes.axis_label = 'real wage w';

    x = source['x'];
    y = source['y'];

    for (i = 0; i < y.length; i++) {
        y[i] = path_data['y'][i];
    }
    line_plot_source.change.emit();
}

if (button == '2') {
    var source = line_plot_source.data;
    var path_data = kpath.data;
    line_object.title[0].attributes.text =
        'Time path for aggregate capital stock K';
    line_object.yaxis[0][0].attributes.axis_label = 'aggregate capital K';

    x = source['x'];
    y = source['y'];

    for (i = 0; i < y.length; i++) {
        y[i] = path_data['y'][i];
    }
    line_plot_source.change.emit();
}

if (button == '3') {
    var source = line_plot_source.data;
    var path_data = lpath.data;
    line_object.title[0].attributes.text = 'Time path for aggregate labor L';
    line_object.yaxis[0][0].attributes.axis_label = 'aggregate labor L';

    x = source['x'];
    y = source['y'];

    for (i = 0; i < y.length; i++) {
        y[i] = path_data['y'][i];
    }
    line_plot_source.change.emit();
}

if (button == '4') {
    var source = line_plot_source.data;
    var path_data = ypath.data;
    line_object.title[0].attributes.text =
        'Time path for aggregate output (GDP) Y';
    line_object.yaxis[0][0].attributes.axis_label = 'aggregate output Y';

    x = source['x'];
    y = source['y'];

    for (i = 0; i < y.length; i++) {
        y[i] = path_data['y'][i];
    }
    line_plot_source.change.emit();
}

if (button == '5') {
    var source = line_plot_source.data;
    var path_data = cpath.data;
    line_object.title[0].attributes.text =
        'Time path for aggregate consumption C';
    line_object.yaxis[0][0].attributes.axis_label = 'aggregate consumption C';

    x = source['x'];
    y = source['y'];

    for (i = 0; i < y.length; i++) {
        y[i] = path_data['y'][i];
    }
    line_plot_source.change.emit();
}
"""
