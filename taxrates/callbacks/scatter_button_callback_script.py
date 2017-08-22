SCATTER_BUTTON_CALLBACK_SCRIPT = """
var tax_button = tax_buttons.active;
var state_button = state_buttons.active;
var source = scatter_source.data;
var etr_data = etr_source.data;
var mtrx_data = mtrx_source.data;
var mtry_data = mtry_source.data;

if (state_button == '0') {
    var etr_zdata = etr_data['z_base']
    var mtrx_zdata = mtrx_data['z_base']
    var mtry_zdata = mtry_data['z_base']
}
if (state_button == '1') {
    var etr_zdata = etr_data['z_pol']
    var mtrx_zdata = mtrx_data['z_pol']
    var mtry_zdata = mtry_data['z_pol']
}
if (state_button == '2') {
    var etr_zdata = etr_data['z_change']
    var mtrx_zdata = mtrx_data['z_change']
    var mtry_zdata = mtry_data['z_change']
}

if (tax_button == '0') {
    window.scatter_graph.setOptions({
        zLabel: 'Effective Tax Rate'
    })

    for (i = 0; i < source['z'].length; i++) {
        source['z'][i] = etr_zdata[i];
    }
    scatter_source.change.emit();
}

if (tax_button == '1') {
    window.scatter_graph.setOptions({
        zLabel: 'Marginal Tax Rate (labor inc.)'
    })

    for (i = 0; i < source['z'].length; i++) {
        source['z'][i] = mtrx_zdata[i];
    }
    scatter_source.change.emit();
}

if (tax_button == '2') {
    window.scatter_graph.setOptions({
        zLabel: 'Marginal Tax Rate (capital inc.)'
    })

    for (i = 0; i < source['z'].length; i++) {
        source['z'][i] = mtry_zdata[i];
    }
    scatter_source.change.emit();
}
"""
