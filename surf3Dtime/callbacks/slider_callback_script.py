SLIDER_CALLBACK_SCRIPT = """
var data = source.data;
var kdata = line_plot_source.data;
var data_info = data_info.data['variables'];

var time = time.value;
var button = surface_radio_group.active;

var time_periods = data_info[0];
var num_ages = data_info[1];
var num_abilities = data_info[2];
var plot_points = num_ages*num_abilities;

if (button == '0') {
    var bpath = bpath_source.data;

    window.surface_graph.setOptions({
        zLabel: 'indiv. savings-b',
        zMin: data_info[3],
        zMax: data_info[4]})

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

    window.surface_graph.setOptions({
        zLabel: 'indiv. consumption-c',
        zMin: data_info[5],
        zMax: data_info[6]})

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
        zMin: data_info[7],
        zMax: data_info[8],
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
var two_d_button = two_d_radio_group.active;
var two_d_object = two_d_object.data;

var b_path = two_d_all_source['b_path'];
var c_path = two_d_all_source['c_path'];
var n_path = two_d_all_source['n_path'];

if (two_d_button == '0') {
    two_d_object.title[0].attributes.text =
        'Age path for individual savings b';
    two_d_object.yaxis[0][0].attributes.axis_label = 'indiv. savings b';

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
    two_d_object.title[0].attributes.text =
        'Age path for individual consumption c';
    two_d_object.yaxis[0][0].attributes.axis_label = 'indiv. consumption c';

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
    two_d_object.title[0].attributes.text = 'Age path for labor supply n';
    two_d_object.yaxis[0][0].attributes.axis_label = 'labor supply n';

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
