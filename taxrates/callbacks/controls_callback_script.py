CONTROLS_CALLBACK_SCRIPT = """
var year = year_slider.value;
var tax = tax_buttons.active;
var state = state_buttons.active;
var age_range = age_slider.range;
var x_range = x_slider.range;
var y_range = y_slider.range;

window.scatter_graph.setOptions({
    xMin: x_range[0],
    xMax: x_range[1],
    yMin: y_range[0],
    yMax: y_range[1]
});

// For some reason, setting things to null isn't working. So we
// need to make some other signifier that a value should be excluded.
var EXCLUDE = -9999;

var scatter_source_dict = scatter_source.data;
var bar_source_dict = bar_source.data;

var xdata, ydata, age_data, etr_zdata, mtrx_zdata, mtry_zdata;

// Helper functions to assign from different data sets
function assignFromPrefixedData(prefix) {
    xdata = eval(prefix + year.toString()).data['Total Labor Income'].slice();
    ydata = eval(prefix + year.toString()).data['Total Capital Income'].slice();
    age_data = eval(prefix + year.toString()).data['Age'].slice();
    etr_zdata = eval(prefix + year.toString()).data['Effective Tax Rate'].slice();
    mtrx_zdata = eval(prefix + year.toString()).data['MTR Labor Income'].slice();
    mtry_zdata = eval(prefix + year.toString()).data['MTR capital income'].slice();
}

switch(state) {
    case 0:
        assignFromPrefixedData('base_');
        break;
    case 1:
        assignFromPrefixedData('pol_');
        break;
    case 2:
        assignFromPrefixedData('pol_');
        break;
    default: throw new Error('Could not get data set for "state" == ' + state);
}

function getIndexesToRemove(dataSet, upperBound, lowerBound) {
    return dataSet.reduce(function(currentIndexes, value, index) {
        if (value >= upperBound || value < lowerBound) {
            currentIndexes.push(index);
        }
        return currentIndexes;
    }, []);
}
var indexesToRemoveAge = getIndexesToRemove(age_data, age_range[1], age_range[0]);
var indexesToRemoveXaxis = getIndexesToRemove(xdata, x_range[1], x_range[0]);
var indexesToRemoveYaxis = getIndexesToRemove(ydata, y_range[1], y_range[0]);

var base_etr_zdata, base_mtrx_zdata;
var base_mtry_zdata, pol_etr_zdata, pol_mtrx_zdata, pol_mtry_zdata;

if (state == '0' || state == '1') {
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

function updateScatterSource(label, dataSet) {
    window.scatter_graph.setOptions({
        zLabel: label,
    });

    scatter_source_dict['x'] = [];
    scatter_source_dict['y'] = [];
    scatter_source_dict['z'] = [];
    for (var i = 0; i < dataSet.length; i++) {
        if (xdata[i] !== EXCLUDE && ydata[i] !== EXCLUDE && dataSet[i] !== EXCLUDE) {
            scatter_source_dict['x'].push(xdata[i]);
            scatter_source_dict['y'].push(ydata[i]);
            scatter_source_dict['z'].push(dataSet[i]);
        }
    }

    scatter_source.change.emit();
}

if (tax == '0') {
    updateScatterSource('Effective Tax Rate', etr_zdata);
} else if (tax == '1') {
    updateScatterSource('Marginal Tax Rate (labor inc.)', mtrx_zdata);
} else if (tax == '2') {
    updateScatterSource('Marginal Tax Rate (capital inc.)', mtry_zdata);
}
"""
