CONTROLS_CALLBACK_SCRIPT = """
var year = year_slider.value;
var tax = tax_buttons.active;
var state = state_buttons.active;
var age_range = age_slider.range;
var x_range = x_slider.range;
var y_range = y_slider.range;

var scatter_source_dict = scatter_source.data;
var bar_source_dict = bar_source.data;
var age_data = pol_2017.data['Age'];
var xaxis_data = pol_2017.data['Total Labor Income'];
var yaxis_data = pol_2017.data['Total Capital Income'];

window.scatter_graph.setOptions({
    xMin: x_range[0],
    xMax: x_range[1],
    yMin: y_range[0],
    yMax: y_range[1]
})

var indexesToRemoveAge = age_data.reduce(function(currentIndexes, value, index) {
    if (value > age_range[1] || value < age_range[0]) {
        currentIndexes.push(index);
    }

    return currentIndexes;
}, []);

var indexesToRemoveXaxis = xaxis_data.reduce(function(currentIndexes, value, index) {
    if (value > x_range[1] || value < x_range[0]) {
        currentIndexes.push(index);
    }

    return currentIndexes;
}, []);

var indexesToRemoveYaxis = yaxis_data.reduce(function(currentIndexes, value, index) {
    if (value > y_range[1] || value < y_range[0]) {
        currentIndexes.push(index);
    }

    return currentIndexes;
}, []);

if (state == '0') {
    var xdata = eval('base_' + year.toString()).data['Total Labor Income'].slice();
    var ydata = eval('base_' + year.toString()).data['Total Capital Income'].slice();
    var etr_zdata = eval('base_' + year.toString()).data['Effective Tax Rate'].slice();
    var mtrx_zdata = eval('base_' + year.toString()).data['MTR Labor Income'].slice();
    var mtry_zdata = eval('base_' + year.toString()).data['MTR capital income'].slice();

    indexesToRemoveAge.forEach(function(index) {
        xdata[index] = null;
        ydata[index] = null;
        etr_zdata[index] = null;
        mtrx_zdata[index] = null;
        mtry_zdata[index] = null;
    });

    indexesToRemoveXaxis.forEach(function(index) {
        xdata[index] = null;
        ydata[index] = null;
        etr_zdata[index] = null;
        mtrx_zdata[index] = null;
        mtry_zdata[index] = null;
    });

    indexesToRemoveYaxis.forEach(function(index) {
        xdata[index] = null;
        ydata[index] = null;
        etr_zdata[index] = null;
        mtrx_zdata[index] = null;
        mtry_zdata[index] = null;
    });
}
if (state == '1') {
    var xdata = eval('pol_' + year.toString()).data['Total Labor Income'].slice();
    var ydata = eval('pol_' + year.toString()).data['Total Capital Income'].slice();
    var etr_zdata = eval('pol_' + year.toString()).data['Effective Tax Rate'].slice();
    var mtrx_zdata = eval('pol_' + year.toString()).data['MTR Labor Income'].slice();
    var mtry_zdata = eval('pol_' + year.toString()).data['MTR capital income'].slice();

    indexesToRemoveAge.forEach(function(index) {
        xdata[index] = null;
        ydata[index] = null;
        etr_zdata[index] = null;
        mtrx_zdata[index] = null;
        mtry_zdata[index] = null;
    });

    indexesToRemoveXaxis.forEach(function(index) {
        xdata[index] = null;
        ydata[index] = null;
        etr_zdata[index] = null;
        mtrx_zdata[index] = null;
        mtry_zdata[index] = null;
    });

    indexesToRemoveYaxis.forEach(function(index) {
        xdata[index] = null;
        ydata[index] = null;
        etr_zdata[index] = null;
        mtrx_zdata[index] = null;
        mtry_zdata[index] = null;
    });
}
if (state == '2') {
    var xdata = eval('pol_' + year.toString()).data['Total Labor Income'].slice();
    var ydata = eval('pol_' + year.toString()).data['Total Capital Income'].slice();
    var base_etr_zdata = eval('base_' + year.toString()).data['Effective Tax Rate'].slice();
    var base_mtrx_zdata = eval('base_' + year.toString()).data['MTR Labor Income'].slice();
    var base_mtry_zdata = eval('base_' + year.toString()).data['MTR capital income'].slice();
    var pol_etr_zdata = eval('pol_' + year.toString()).data['Effective Tax Rate'].slice();
    var pol_mtrx_zdata = eval('pol_' + year.toString()).data['MTR Labor Income'].slice();
    var pol_mtry_zdata = eval('pol_' + year.toString()).data['MTR capital income'].slice();

    indexesToRemoveAge.forEach(function(index) {
        xdata[index] = null;
        ydata[index] = null;
        etr_zdata[index] = null;
        mtrx_zdata[index] = null;
        mtry_zdata[index] = null;
    });

    indexesToRemoveXaxis.forEach(function(index) {
        xdata[index] = null;
        ydata[index] = null;
        etr_zdata[index] = null;
        mtrx_zdata[index] = null;
        mtry_zdata[index] = null;
    });

    indexesToRemoveYaxis.forEach(function(index) {
        xdata[index] = null;
        ydata[index] = null;
        etr_zdata[index] = null;
        mtrx_zdata[index] = null;
        mtry_zdata[index] = null;
    });

    var etr_zdata = pol_etr_zdata.map( function (item, index) {
        return item - base_etr_zdata[index];
    })
    var mtrx_zdata = pol_mtrx_zdata.map( function (item, index) {
        return item - base_mtrx_zdata[index];
    })
    var mtry_zdata = pol_mtry_zdata.map( function (item, index) {
        return item - base_mtry_zdata[index];
    })
}

if (tax == '0') {
    window.scatter_graph.setOptions({
        zLabel: 'Effective Tax Rate'
    })

    for (i = 0; i < etr_zdata.length; i++) {
        scatter_source_dict['x'][i] = xdata[i];
        scatter_source_dict['y'][i] = ydata[i];
        scatter_source_dict['z'][i] = etr_zdata[i];
    }
    scatter_source.change.emit();
}

if (tax == '1') {
    window.scatter_graph.setOptions({
        zLabel: 'Marginal Tax Rate (labor inc.)'
    })

    for (i = 0; i < etr_zdata.length; i++) {
        scatter_source_dict['x'][i] = xdata[i];
        scatter_source_dict['y'][i] = ydata[i];
        scatter_source_dict['z'][i] = mtrx_zdata[i];
    }
    scatter_source.change.emit();
}

if (tax == '2') {
    window.scatter_graph.setOptions({
        zLabel: 'Marginal Tax Rate (capital inc.)'
    })

    for (i = 0; i < etr_zdata.length; i++) {
        scatter_source_dict['x'][i] = xdata[i];
        scatter_source_dict['y'][i] = ydata[i];
        scatter_source_dict['z'][i] = mtry_zdata[i];
    }
    scatter_source.change.emit();
}
debugger
"""
