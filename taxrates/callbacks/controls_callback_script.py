CONTROLS_CALLBACK_SCRIPT = """
var year = year_slider.value;
var tax = tax_buttons.active;
var state = state_buttons.active;
var age_range = age_slider.range;
var x_range = x_slider.range;
var y_range = y_slider.range;

var scatter_source_dict = scatter_source.data;
var bar_source_dict = bar_source.data;
var age_data = base_2017.data['Age'];
var xaxis_data = base_2017.data['Total Labor Income'];
var yaxis_data = base_2017.data['Total Capital Income'];

// For some reason, setting things to null isn't working. So we
// need to make some other signifier that a value should be excluded.
var EXCLUDE = -9999;

window.scatter_graph.setOptions({
    xMin: x_range[0],
    xMax: x_range[1],
    yMin: y_range[0],
    yMax: y_range[1]
})

var indexesToRemoveAge = age_data.reduce(function(currentIndexes, value, index) {
    if (value >= age_range[1] || value < age_range[0]) {
        currentIndexes.push(index);
    }

    return currentIndexes;
}, []);

var indexesToRemoveXaxis = xaxis_data.reduce(function(currentIndexes, value, index) {
    if (value >= x_range[1] || value < x_range[0]) {
        currentIndexes.push(index);
    }

    return currentIndexes;
}, []);

var indexesToRemoveYaxis = yaxis_data.reduce(function(currentIndexes, value, index) {
    if (value >= y_range[1] || value < y_range[0]) {
        currentIndexes.push(index);
    }

    return currentIndexes;
}, []);

var xdata, ydata, etr_zdata, mtrx_zdata, mtry_zdata, base_etr_zdata, base_mtrx_zdata, base_mtry_zdata, pol_etr_zdata, pol_mtrx_zdata, pol_mtry_zdata;

if (state == '0') {
    console.log('state 0')
    xdata = eval('base_' + year.toString()).data['Total Labor Income'].slice();
    ydata = eval('base_' + year.toString()).data['Total Capital Income'].slice();
    etr_zdata = eval('base_' + year.toString()).data['Effective Tax Rate'].slice();
    mtrx_zdata = eval('base_' + year.toString()).data['MTR Labor Income'].slice();
    mtry_zdata = eval('base_' + year.toString()).data['MTR capital income'].slice();

    indexesToRemoveAge.forEach(function(index) {
        xdata[index] = EXCLUDE;
        ydata[index] = EXCLUDE;
        etr_zdata[index] = EXCLUDE;
        mtrx_zdata[index] = EXCLUDE;
        mtry_zdata[index] = EXCLUDE;
    });

    indexesToRemoveXaxis.forEach(function(index) {
        xdata[index] = EXCLUDE;
        ydata[index] = EXCLUDE;
        etr_zdata[index] = EXCLUDE;
        mtrx_zdata[index] = EXCLUDE;
        mtry_zdata[index] = EXCLUDE;
    });

    indexesToRemoveYaxis.forEach(function(index) {
        xdata[index] = EXCLUDE;
        ydata[index] = EXCLUDE;
        etr_zdata[index] = EXCLUDE;
        mtrx_zdata[index] = EXCLUDE;
        mtry_zdata[index] = EXCLUDE;
    });
}
if (state == '1') {
    console.log('state 1')
    xdata = eval('pol_' + year.toString()).data['Total Labor Income'].slice();
    ydata = eval('pol_' + year.toString()).data['Total Capital Income'].slice();
    etr_zdata = eval('pol_' + year.toString()).data['Effective Tax Rate'].slice();
    mtrx_zdata = eval('pol_' + year.toString()).data['MTR Labor Income'].slice();
    mtry_zdata = eval('pol_' + year.toString()).data['MTR capital income'].slice();

    indexesToRemoveAge.forEach(function(index) {
        xdata[index] = EXCLUDE;
        ydata[index] = EXCLUDE;
        etr_zdata[index] = EXCLUDE;
        mtrx_zdata[index] = EXCLUDE;
        mtry_zdata[index] = EXCLUDE;
    });

    indexesToRemoveXaxis.forEach(function(index) {
        xdata[index] = EXCLUDE;
        ydata[index] = EXCLUDE;
        etr_zdata[index] = EXCLUDE;
        mtrx_zdata[index] = EXCLUDE;
        mtry_zdata[index] = EXCLUDE;
    });

    indexesToRemoveYaxis.forEach(function(index) {
        xdata[index] = EXCLUDE;
        ydata[index] = EXCLUDE;
        etr_zdata[index] = EXCLUDE;
        mtrx_zdata[index] = EXCLUDE;
        mtry_zdata[index] = EXCLUDE;
    });
}


if (state == '2') {
    xdata = eval('pol_' + year.toString()).data['Total Labor Income'].slice();
    ydata = eval('pol_' + year.toString()).data['Total Capital Income'].slice();
    base_etr_zdata = eval('base_' + year.toString()).data['Effective Tax Rate'].slice();
    base_mtrx_zdata = eval('base_' + year.toString()).data['MTR Labor Income'].slice();
    base_mtry_zdata = eval('base_' + year.toString()).data['MTR capital income'].slice();
    pol_etr_zdata = eval('pol_' + year.toString()).data['Effective Tax Rate'].slice();
    pol_mtrx_zdata = eval('pol_' + year.toString()).data['MTR Labor Income'].slice();
    pol_mtry_zdata = eval('pol_' + year.toString()).data['MTR capital income'].slice();

    indexesToRemoveAge.forEach(function(index) {
        xdata[index] = EXCLUDE;
        ydata[index] = EXCLUDE;
        base_etr_zdata[index] = EXCLUDE;
        base_mtrx_zdata[index] = EXCLUDE;
        base_mtry_zdata[index] = EXCLUDE;
        pol_etr_zdata[index] = EXCLUDE;
        pol_mtrx_zdata[index] = EXCLUDE;
        pol_mtry_zdata[index] = EXCLUDE;
    });

    indexesToRemoveXaxis.forEach(function(index) {
        xdata[index] = EXCLUDE;
        ydata[index] = EXCLUDE;
        base_etr_zdata[index] = EXCLUDE;
        base_mtrx_zdata[index] = EXCLUDE;
        base_mtry_zdata[index] = EXCLUDE;
        pol_etr_zdata[index] = EXCLUDE;
        pol_mtrx_zdata[index] = EXCLUDE;
        pol_mtry_zdata[index] = EXCLUDE;
    });

    indexesToRemoveYaxis.forEach(function(index) {
        xdata[index] = EXCLUDE;
        ydata[index] = EXCLUDE;
        base_etr_zdata[index] = EXCLUDE;
        base_mtrx_zdata[index] = EXCLUDE;
        base_mtry_zdata[index] = EXCLUDE;
        pol_etr_zdata[index] = EXCLUDE;
        pol_mtrx_zdata[index] = EXCLUDE;
        pol_mtry_zdata[index] = EXCLUDE;
    });

    etr_zdata = pol_etr_zdata.map(function (item, index) {
        return item - base_etr_zdata[index];
    })
    mtrx_zdata = pol_mtrx_zdata.map(function (item, index) {
        return item - base_mtrx_zdata[index];
    })
    mtry_zdata = pol_mtry_zdata.map(function (item, index) {
        return item - base_mtry_zdata[index];
    })
}

if (tax == '0') {
    window.scatter_graph.setOptions({
        zLabel: 'Effective Tax Rate'
    })

    scatter_source_dict['x'] = [];
    scatter_source_dict['y'] = [];
    scatter_source_dict['z'] = [];
    for (var i = 0; i < etr_zdata.length; i++) {
        if (xdata[i] !== EXCLUDE && ydata[i] !== EXCLUDE && etr_zdata[i] !== EXCLUDE) {
            scatter_source_dict['x'].push(xdata[i]);
            scatter_source_dict['y'].push(ydata[i]);
            scatter_source_dict['z'].push(etr_zdata[i]);
        }
    }

    scatter_source.change.emit();
}

if (tax == '1') {
    window.scatter_graph.setOptions({
        zLabel: 'Marginal Tax Rate (labor inc.)'
    })

    scatter_source_dict['x'] = [];
    scatter_source_dict['y'] = [];
    scatter_source_dict['z'] = [];
    for (var i = 0; i < etr_zdata.length; i++) {
        if (xdata[i] !== EXCLUDE && ydata[i] !== EXCLUDE && mtrx_zdata[i] !== EXCLUDE) {
            scatter_source_dict['x'].push(xdata[i]);
            scatter_source_dict['y'].push(ydata[i]);
            scatter_source_dict['z'].push(mtrx_zdata[i]);

            if (xdata[i] > 500000) {
                debugger
            }
        }
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
"""
