'''
------------------------------------------------------------------------
This script reads in data generated from the OSPC Tax Calculator and
the 2009 IRS PUF and plots one year and age of data

This module defines the following functions:
    clean_data()
    gen_3Dscatter_hist()
------------------------------------------------------------------------
'''
# Import packages
import os
import pickle
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

'''
------------------------------------------------------------------------
Define Functions
------------------------------------------------------------------------
'''


def clean_data(microDataDict, beg_yr, end_yr):
    '''
    --------------------------------------------------------------------
    This function imports the micro data dictionary from Tax-Calculator
    and returns the data file necessary to make the 3D scatterplots for
    ETR, MTRx, and MTRy, and the associated 3D histogram.
    --------------------------------------------------------------------
    INPUTS:
    df         = (N1, 11) DataFrame, 11 variables with N observations
    s          = integer >= 21, age of individual
    t          = integer >= 2016, year of analysis
    output_dir = string, output directory for saving plot files

    OTHER FUNCTIONS AND FILES CALLED BY THIS FUNCTION: None

    OBJECTS CREATED WITHIN FUNCTION:

    FILES SAVED BY THIS FUNCTION:

    RETURNS: microDataDict_clean
    --------------------------------------------------------------------
    '''
    tpers = int(end_yr - beg_yr + 1)
    AvgInc = np.zeros(tpers)
    AvgETR = np.zeros(tpers)
    AvgMTRx = np.zeros(tpers)
    AvgMTRy = np.zeros(tpers)
    TotPop_yr = np.zeros(tpers)
    years_list = np.arange(beg_yr, end_yr + 1)
    microDataDict_clean = {}
    for t in years_list:
        '''
        ----------------------------------------------------------------
        Clean up the data
        ----------------------------------------------------------------
        data_orig  = (N1, 11) DataFrame, original micro tax data from
                     Tax-Calculator for particular year
        data       = (N1, 8) DataFrame, new variables dataset
        data_trnc  = (N2, 8) DataFrame, truncated observations dataset
        min_age    = integer >= 1, minimum age in micro data that is
                     relevant to model
        max_age    = integer >= min_age, maximum age in micro data that
                     is relevant to model
        NoData_cnt = integer >= 0, number of consecutive ages with
                     insufficient data to estimate tax functions
        ----------------------------------------------------------------
        '''
        data_orig = microDataDict[str(t)]
        data_orig['Total Labor Income'] = \
            (data_orig['Wage and Salaries'] +
             data_orig['Self-Employed Income'])
        data_orig['Effective Tax Rate'] = \
            (data_orig['Total Tax Liability'] /
             data_orig["Adjusted Total income"])
        data_orig["Total Capital Income"] = \
            (data_orig['Adjusted Total income'] -
             data_orig['Total Labor Income'])
        # use weighted avg for MTR labor - abs value because
        # SE income may be negative
        data_orig['MTR Labor Income'] = \
            (data_orig['MTR wage'] * (data_orig['Wage and Salaries'] /
             (data_orig['Wage and Salaries'].abs() +
             data_orig['Self-Employed Income'].abs())) +
             data_orig['MTR self-employed Wage'] *
             (data_orig['Self-Employed Income'].abs() /
             (data_orig['Wage and Salaries'].abs() +
              data_orig['Self-Employed Income'].abs())))
        data = data_orig[['Age', 'MTR Labor Income', 'MTR capital income',
                          'Total Labor Income', 'Total Capital Income',
                          'Adjusted Total income', 'Effective Tax Rate',
                          'Weights']]

        # Calculate average total income in each year
        AvgInc[t - beg_yr] = \
            (((data['Adjusted Total income'] * data['Weights']).sum()) /
             data['Weights'].sum())

        # Calculate average ETR and MTRs (weight by population weights
        #    and income) for each year
        AvgETR[t - beg_yr] = \
            (((data['Effective Tax Rate'] *
             data['Adjusted Total income'] * data['Weights']).sum()) /
             (data['Adjusted Total income'] * data['Weights']).sum())

        AvgMTRx[t - beg_yr] = \
            (((data['MTR Labor Income'] * data['Adjusted Total income'] *
             data['Weights']).sum()) /
             (data['Adjusted Total income'] * data['Weights']).sum())

        AvgMTRy[t - beg_yr] = \
            (((data['MTR capital income'] *
             data['Adjusted Total income'] * data['Weights']).sum()) /
             (data['Adjusted Total income'] * data['Weights']).sum())

        # Calculate total population in each year
        TotPop_yr[t - beg_yr] = data['Weights'].sum()

        # Clean up the data by dropping outliers
        # drop all obs with ETR > 0.65
        data_trnc = \
            data.drop(data[data['Effective Tax Rate'] > 0.65].index)
        # drop all obs with ETR < -0.15
        data_trnc = \
            data_trnc.drop(data_trnc[data_trnc['Effective Tax Rate'] <
                                     -0.15].index)
        # drop all obs with ATI, TLI, TCI < $5
        data_trnc = \
            data_trnc[(data_trnc['Adjusted Total income'] >= 5) &
                      (data_trnc['Total Labor Income'] >= 5) &
                      (data_trnc['Total Capital Income'] >= 5)]

        # drop all obs with MTR on capital income > 10.99
        data_trnc = \
            data_trnc.drop(data_trnc[data_trnc['MTR capital income'] >
                           0.99].index)
        # drop all obs with MTR on capital income < -0.45
        data_trnc = \
            data_trnc.drop(data_trnc[data_trnc['MTR capital income'] <
                           -0.45].index)
        # drop all obs with MTR on labor income > 10.99
        data_trnc = data_trnc.drop(data_trnc[data_trnc['MTR Labor Income'] >
                                   0.99].index)
        # drop all obs with MTR on labor income < -0.45
        data_trnc = data_trnc.drop(data_trnc[data_trnc['MTR Labor Income'] <
                                   -0.45].index)

        microDataDict_clean[str(t)] = data_trnc

    return microDataDict_clean


def gen_3Dscatters_hist(df, s, t):
    '''
    --------------------------------------------------------------------
    Create 3-D scatterplots and corresponding 3D histogram of ETR, MTRx,
    and MTRy as functions of labor income and capital income with
    truncated data in the income dimension
    --------------------------------------------------------------------
    INPUTS:
    df         = (N1, 11) DataFrame, 11 variables with N observations
    s          = integer >= 21, age of individual
    t          = integer >= 2016, year of analysis

    OTHER FUNCTIONS AND FILES CALLED BY THIS FUNCTION: None

    OBJECTS CREATED WITHIN FUNCTION:
    cur_path    = string, path name of current directory
    output_fldr = string, folder in current path to save files
    output_dir  = string, total path of images directory
    df_trnc     = (N2 x 6) DataFrame, truncated data for 3D graph
    inc_lab     = (N2 x 1) vector, total labor income for 3D graph
    inc_cap     = (N2 x 1) vector, total capital income for 3D graph
    etr_data    = (N2 x 1) vector, effective tax rate data
    mtrx_data   = (N2 x 1) vector, marginal tax rate of labor income
                  data
    mtry_data   = (N2 x 1) vector, marginal tax rate of capital income
                  data
    filename    = string, name of image file
    fullpath    = string, full path of file
    bin_num     = integer >= 2, number of bins along each axis for 3D
                  histogram
    hist        = (bin_num, bin_num) matrix, bin percentages
    xedges      = (bin_num+1,) vector, bin edge values in x-dimension
    yedges      = (bin_num+1,) vector, bin edge values in y-dimension
    x_midp      = (bin_num,) vector, midpoints of bins in x-dimension
    y_midp      = (bin_num,) vector, midpoints of bins in y-dimension
    elements    = integer, total number of 3D histogram bins
    xpos        = (bin_num * bin_num) vector, x-coordinates of each bin
    ypos        = (bin_num * bin_num) vector, y-coordinates of each bin
    zpos        = (bin_num * bin_num) vector, zeros or z-coordinates of
                  origin of each bin
    dx          = (bin_num,) vector, x-width of each bin
    dy          = (bin_num,) vector, y-width of each bin
    dz          = (bin_num * bin_num) vector, height of each bin

    FILES SAVED BY THIS FUNCTION:
        output_dir/ETR_Age_[age]_Year_[year]_data.png
        output_dir/MTRx_Age_[age]_Year_[year]_data.png
        output_dir/MTRy_Age_[age]_Year_[year]_data.png
        output_dir/Hist_Age_[age]_Year_[year].png

    RETURNS: None
    --------------------------------------------------------------------
    '''
    # Create directory if images directory does not already exist
    cur_path = os.path.split(os.path.abspath(__file__))[0]
    output_fldr = 'images'
    output_dir = os.path.join(cur_path, output_fldr)
    if not os.access(output_dir, os.F_OK):
        os.makedirs(output_dir)

    # Truncate the data
    df_trnc = df[(df['Total Labor Income'] > 5) &
                 (df['Total Labor Income'] < 500000) &
                 (df['Total Capital Income'] > 5) &
                 (df['Total Capital Income'] < 500000)]
    inc_lab = df_trnc['Total Labor Income']
    inc_cap = df_trnc['Total Capital Income']
    etr_data = df_trnc['Effective Tax Rate']
    mtrx_data = df_trnc['MTR Labor Income']
    mtry_data = df_trnc['MTR capital income']

    # Plot 3D scatterplot of ETR data
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(inc_lab, inc_cap, etr_data, c='r', marker='o')
    ax.set_xlabel('Total Labor Income')
    ax.set_ylabel('Total Capital Income')
    ax.set_zlabel('Effective Tax Rate')
    plt.title('ETR, Lab. Inc., and Cap. Inc., Age=' + str(s) +
              ', Year=' + str(t))
    filename = ('ETR_Age_' + str(s) + '_Year_' + str(t) + '_data.png')
    fullpath = os.path.join(output_dir, filename)
    fig.savefig(fullpath, bbox_inches='tight')
    plt.close()

    # Plot 3D histogram for all data
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    bin_num = int(30)
    hist, xedges, yedges = np.histogram2d(inc_lab, inc_cap,
                                          bins=bin_num)
    hist = hist / hist.sum()
    x_midp = xedges[:-1] + 0.5 * (xedges[1] - xedges[0])
    y_midp = yedges[:-1] + 0.5 * (yedges[1] - yedges[0])
    elements = (len(xedges) - 1) * (len(yedges) - 1)
    ypos, xpos = np.meshgrid(y_midp, x_midp)
    xpos = xpos.flatten()
    ypos = ypos.flatten()
    zpos = np.zeros(elements)
    dx = (xedges[1] - xedges[0]) * np.ones_like(bin_num)
    dy = (yedges[1] - yedges[0]) * np.ones_like(bin_num)
    dz = hist.flatten()
    ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color='b', zsort='average')
    ax.set_xlabel('Total Labor Income')
    ax.set_ylabel('Total Capital Income')
    ax.set_zlabel('Percent of obs.')
    plt.title('Histogram by lab. inc., and cap. inc., Age=' + str(s) +
              ', Year=' + str(t))
    filename = ('Hist_Age_' + str(s) + '_Year_' + str(t) + '.png')
    fullpath = os.path.join(output_dir, filename)
    fig.savefig(fullpath, bbox_inches='tight')
    plt.close()

    # Plot 3D scatterplot of MTRx data
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(inc_lab, inc_cap, mtrx_data, c='r', marker='o')
    ax.set_xlabel('Total Labor Income')
    ax.set_ylabel('Total Capital Income')
    ax.set_zlabel('Marginal Tax Rate, Labor Inc.)')
    plt.title('MTR Labor Income, Lab. Inc., and Cap. Inc., Age=' +
              str(s) + ", Year=" + str(t))
    filename = ('MTRx_Age_' + str(s) + '_Year_' + str(t) + '_data.png')
    fullpath = os.path.join(output_dir, filename)
    fig.savefig(fullpath, bbox_inches='tight')
    plt.close()

    # Plot 3D scatterplot of MTRy data
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(inc_lab, inc_cap, mtry_data, c='r', marker='o')
    ax.set_xlabel('Total Labor Income')
    ax.set_ylabel('Total Capital Income')
    ax.set_zlabel('Marginal Tax Rate (Capital Inc.)')
    plt.title('MTR Capital Income, Cap. Inc., and Cap. Inc., Age=' +
              str(s) + ', Year=' + str(t))
    filename = ('MTRy_Age_' + str(s) + '_Year_' + str(t) + '_data.png')
    fullpath = os.path.join(output_dir, filename)
    fig.savefig(fullpath, bbox_inches='tight')
    plt.close()


# Read in the data and clean it
start_yr = 2017
end_yr = 2026
micro_dict_base = pickle.load(open('data/micro_dict_base.pkl', 'rb'))
micro_dict_pol = pickle.load(open('data/micro_dict_pol.pkl', 'rb'))
microDataDict_base_clean = clean_data(micro_dict_base, start_yr, end_yr)
microDataDict_pol_clean = clean_data(micro_dict_pol, start_yr, end_yr)

# How to generate three 3D scatter plots (ETR, MTRx, MTRy) and one
# population histogram for a given year and age
year = int(2017)
age = 42
df = microDataDict_base_clean[str(year)]
df = df[df['Age'] == age]
gen_3Dscatters_hist(df, age, year)
