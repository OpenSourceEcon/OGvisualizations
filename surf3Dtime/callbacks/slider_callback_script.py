SLIDER_CALLBACK_SCRIPT = """
var data = source.data;
var kdata = line_plot_source.data;

var time = time.value;
var button = surface_radio_group.active;
var two_d_button = two_d_radio_group.active;

var time_periods = 359;
var num_ages = 80;
var num_abilities = 7;
var plot_points = num_ages*num_abilities;

if (button == '0') {
    var bpath = bpath_source.data;

    window.surface_graph.setOptions({zLabel: 'indiv. savings-b', zMin: -20,
    zMax: 60})

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

    window.surface_graph.setOptions({zLabel: 'indiv. consumption-c', zMin: 0,
    zMax: 6})

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

    window.surface_graph.setOptions({
        zLabel: 'labor supply-n',
        zMin: 0,
        zMax: 1,
    });

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

var two_d_data = two_d_plot_source.data
var two_d_all_source = two_d_all_source.data;

var b_path = two_d_all_source['b_path'];
var c_path = two_d_all_source['c_path'];
var n_path = two_d_all_source['n_path'];

if (two_d_button == '0') {
    for (j = 0; j < num_abilities; j++) {
        beg = num_ages*j + num_ages*num_abilities*time;
        end = num_ages*(j+1) + num_ages*num_abilities*time;
        current_b_path = b_path.slice(beg,end);

        for (i = 0; i < num_ages; i++) {
            two_d_data['y_' + j][i] = current_b_path[i];
        }
    }

    two_d_plot_source.change.emit();
}

if (two_d_button == '1') {
    for (j = 0; j < num_abilities; j++) {
        beg = num_ages*j + num_ages*num_abilities*time;
        end = num_ages*(j+1) + num_ages*num_abilities*time;
        current_c_path = c_path.slice(beg,end);

        for (i = 0; i < num_ages; i++) {
            two_d_data['y_' + j][i] = current_c_path[i];
        }
    }

    two_d_plot_source.change.emit();
}

if (two_d_button == '2') {
    for (j = 0; j < num_abilities; j++) {
        beg = num_ages*j + num_ages*num_abilities*time;
        end = num_ages*(j+1) + num_ages*num_abilities*time;
        current_n_path = n_path.slice(beg,end);

        for (i = 0; i < num_ages; i++) {
            two_d_data['y_' + j][i] = current_n_path[i];
        }
    }

    two_d_plot_source.change.emit();
}

kdata['circle_color'] = Array(time_periods).fill('white');
kdata['circle_color'][time] = '#3288bd';

line_plot_source.change.emit();
"""
