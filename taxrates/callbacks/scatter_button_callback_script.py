SCATTER_BUTTON_CALLBACK_SCRIPT = """
var button = scatter_buttons.active;
var source = scatter_source.data;

if (button == '0') {
    var etr_data = etr_source.data;
    etr_zdata = etr_data['z']

    window.scatter_graph.setOptions({
        zLabel: 'Effective Tax Rate'
    })

    for (i = 0; i < source['z'].length; i++) {
        source['z'][i] = etr_zdata[i];
    }
    scatter_source.change.emit();
}

if (button == '1') {
    var mtrx_data = mtrx_source.data;
    mtrx_zdata = mtrx_data['z']

    window.scatter_graph.setOptions({
        zLabel: 'Marginal Tax Rate (labor inc.)'
    })

    for (i = 0; i < source['z'].length; i++) {
        source['z'][i] = mtrx_zdata[i];
    }
    scatter_source.change.emit();
}

if (button == '2') {
    var mtry_data = mtry_source.data;
    mtry_zdata = mtry_data['z']

    window.scatter_graph.setOptions({
        zLabel: 'Marginal Tax Rate (capital inc.)'
    })

    for (i = 0; i < source['z'].length; i++) {
        source['z'][i] = mtry_zdata[i];
    }
    scatter_source.change.emit();
}
"""
