# Dynamic 3D Scatter Plot Visualization of Tax Rates
This directory provides code for a dynamic 3D scatter plot visualization of three different tax rate measures--effective tax rate (ETR), marginal tax rate on labor income (MTRx), and marginal tax rate on capital income (MTRy)--as functions of labor income and capital income, respectively. The visualization also includes a 3D histogram of the population distribution by labor income and capital income respectively.

## Description of current code
This code runs with Python 3.6. The running the current code requires the Python script [`txrates.py`](https://github.com/OpenSourceMacro/OGvisualizations/blob/master/taxrates/txrates.py). It also requires that the following two Python pickle files (`micro_dict_base.pkl` and `micro_dict_pol.pkl`) be placed in a `/data/` directory at the level of the `txrates.py` script. These two pickle files are Python dictionaries, each element of which is a Pandas dataframe of tax rate data for a given year. The file `micro_dict_base.pkl` contains tax rate data for the current policy baseline. The file `micro_dict_pol.pkl` contains tax rate data for a policy reform.

**WARNING:** The two source data files `micro_dict_base.pkl` and `micro_dict_pol.pkl` cannot be made public yet because they are derived from the IRS Public Use File (PUF). We are currently working on a way to make these data public.
