'''
------------------------------------------------------------------------
This module contains the functions used to solve the steady state of
the model with S-period lived agents, endogenous labor supply, and
heterogeneous ability from Chapter 8 of the OG textbook.

This Python module imports the following module(s):
    households.py
    firms.py
    aggregates.py
    utilities.py

This Python module defines the following function(s):
    get_SS_bsct()
------------------------------------------------------------------------
'''
# Import packages
import time
import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import os
import households as hh
import firms
import aggregates as aggr
import utilities as utils

'''
------------------------------------------------------------------------
    Functions
------------------------------------------------------------------------
'''


def get_SS_bsct(init_vals, args, graphs=False):
    '''
    --------------------------------------------------------------------
    Solve for the steady-state solution of the S-period-lived agent OG
    model with endogenous labor supply using the bisection method for
    the outer loop
    --------------------------------------------------------------------
    INPUTS:
    init_vals = length 3 tuple, (Kss_init, Lss_init, c1_init)
    args      = length 15 tuple, (J, S, lambdas, emat, beta, sigma,
                l_tilde, b_ellip, upsilon, chi_n_vec, A, alpha, delta,
                SS_tol, EulDiff)
    graphs    = boolean, =True if output steady-state graphs

    OTHER FUNCTIONS AND FILES CALLED BY THIS FUNCTION:
        firms.get_r()
        firms.get_w()
        hh.bn_solve()
        hh.c1_bSp1err()
        hh.get_cnb_vecs()
        aggr.get_K()
        aggr.get_L()
        aggr.get_Y()
        aggr.get_C()
        hh.get_cons()
        hh.get_n_errors()
        hh.get_b_errors()
        utils.print_time()

    OBJECTS CREATED WITHIN FUNCTION:
    start_time   = scalar > 0, clock time at beginning of program
    Kss_init     = scalar > 0, initial guess for steady-state aggregate
                   capital stock
    Lss_init     = scalar > 0, initial guess for steady-state aggregate
                   labor
    rss_init     = scalar > 0, initial guess for steady-state interest
                   rate
    wss_init     = scalar > 0, initial guess for steady-state wage
    c1_init      = scalar > 0, initial guess for first period consumpt'n
    S            = integer in [3, 80], number of periods an individual
                   lives
    beta         = scalar in (0,1), discount factor for each model per
    sigma        = scalar > 0, coefficient of relative risk aversion
    l_tilde      = scalar > 0, time endowment for each agent each period
    b_ellip      = scalar > 0, fitted value of b for elliptical
                   disutility of labor
    upsilon      = scalar > 1, fitted value of upsilon for elliptical
                   disutility of labor
    chi_n_vec    = (S,) vector, values for chi^n_s
    A            = scalar > 0, total factor productivity parameter in
                   firms' production function
    alpha        = scalar in (0,1), capital share of income
    delta        = scalar in [0,1], model-period depreciation rate of
                   capital
    SS_tol       = scalar > 0, tolerance level for steady-state fsolve
    EulDiff      = Boolean, =True if want difference version of Euler
                   errors beta*(1+r)*u'(c2) - u'(c1), =False if want
                   ratio version [beta*(1+r)*u'(c2)]/[u'(c1)] - 1
    hh_fsolve    = boolean, =True if solve inner-loop household problem
                   by choosing c_1 to set final period savings b_{S+1}=0
    KL_outer     = boolean, =True if guess K and L in outer loop
                   Otherwise, guess r and w in outer loop
    maxiter_SS   = integer >= 1, maximum number of iterations in outer
                   loop bisection method
    iter_SS      = integer >= 0, index of iteration number
    mindist_SS   = scalar > 0, minimum distance tolerance for
                   convergence
    dist_SS      = scalar > 0, distance metric for current iteration
    xi_SS        = scalar in (0,1], updating parameter
    KL_init      = (2,) vector, (K_init, L_init)
    c1_options   = length 1 dict, options to pass into
                   opt.root(c1_bSp1err,...)
    cnb_args     = length 8 tuple, args to pass into get_cnb_vecs()
    r_params     = length 3 tuple, args to pass into get_r()
    w_params     = length 2 tuple, args to pass into get_w()
    K_init       = scalar, initial value of aggregate capital stock
    L_init       = scalar, initial value of aggregate labor
    r_init       = scalar, initial value for interest rate
    w_init       = scalar, initial value for wage
    rpath        = (S,) vector, lifetime path of interest rates
    wpath        = (S,) vector, lifetime path of wages
    c1_args      = length 10 tuple, args to pass into c1_bSp1err()
    results_c1   = results object, root finder results from
                   opt.root(c1_bSp1err,...)
    c1_new       = scalar, updated value of optimal c1 given r_init and
                   w_init
    cvec_new     = (S,) vector, updated values for lifetime consumption
    nvec_new     = (S,) vector, updated values for lifetime labor supply
    bvec_new     = (S,) vector, updated values for lifetime savings
                   (b1, b2,...bS)
    b_Sp1_new    = scalar, updated value for savings in last period,
                   should be arbitrarily close to zero
    K_new        = scalar, updated K given bvec_new
    K_cnstr      = boolean, =True if K_new <= 0
    L_new        = scalar, updated L given nvec_new
    KL_new       = (2,) vector, updated K and L given bvec_new, nvec_new
    K_ss         = scalar > 0, steady-state aggregate capital stock
    L_ss         = scalar > 0, steady-state aggregate labor
    r_ss         = scalar > 0, steady-state interest rate
    w_ss         = scalar > 0, steady-state wage
    c1_ss        = scalar > 0, steady-state consumption in first period
    c_ss         = (S,) vector, steady-state lifetime consumption
    n_ss         = (S,) vector, steady-state lifetime labor supply
    b_ss         = (S,) vector, steady-state lifetime savings
                   (b1_ss, b2_ss, ...bS_ss) where b1_ss=0
    b_Sp1_ss     = scalar, steady-state savings for period after last
                   period of life. b_Sp1_ss approx. 0 in equilibrium
    Y_params     = length 2 tuple, (A, alpha)
    Y_ss         = scalar > 0, steady-state aggregate output (GDP)
    C_ss         = scalar > 0, steady-state aggregate consumption
    n_err_params = length 5 tuple, args to pass into get_n_errors()
    n_err_ss     = (S,) vector, lifetime labor supply Euler errors
    b_err_params = length 2 tuple, args to pass into get_b_errors()
    b_err_ss     = (S-1) vector, lifetime savings Euler errors
    RCerr_ss     = scalar, resource constraint error
    ss_time      = scalar, seconds elapsed to run steady-state comput'n
    ss_output    = length 14 dict, steady-state objects {n_ss, b_ss,
                   c_ss, b_Sp1_ss, w_ss, r_ss, K_ss, L_ss, Y_ss, C_ss,
                   n_err_ss, b_err_ss, RCerr_ss, ss_time}

    FILES CREATED BY THIS FUNCTION:
        SS_bc.png
        SS_n.png

    RETURNS: ss_output
    --------------------------------------------------------------------
    '''
    start_time = time.clock()
    Kss_init, Lss_init, c1_init = init_vals
    (J, S, lambdas, emat, beta, sigma, l_tilde, b_ellip, upsilon,
        chi_n_vec, A, alpha, delta, SS_tol, EulDiff) = args
    maxiter_SS = 200
    iter_SS = 0
    mindist_SS = 1e-12
    dist_SS = 10
    xi_SS = 0.2
    KL_init = np.array([Kss_init, Lss_init])
    c1_options = {'maxiter': 500}
    r_params = (A, alpha, delta)
    w_params = (A, alpha)
    while (iter_SS < maxiter_SS) and (dist_SS >= mindist_SS):
        iter_SS += 1
        K_init, L_init = KL_init
        r_init = firms.get_r(r_params, K_init, L_init)
        w_init = firms.get_w(w_params, K_init, L_init)
        rpath = r_init * np.ones(S)
        wpath = w_init * np.ones(S)
        cmat = np.zeros((S, J))
        nmat = np.zeros((S, J))
        bmat = np.zeros((S, J))
        b_Sp1_vec = np.zeros(J)
        for j in range(J):
            c1_args = (0.0, emat[:, j], beta, sigma, l_tilde, b_ellip,
                       upsilon, chi_n_vec, rpath, wpath, EulDiff)
            results_c1 = \
                opt.root(hh.c1_bSp1err, c1_init, args=(c1_args),
                         method='lm', tol=SS_tol, options=(c1_options))
            c1 = results_c1.x
            cnb_args = (0.0, emat[:, j], beta, sigma, l_tilde, b_ellip,
                        upsilon, chi_n_vec, EulDiff)
            cmat[:, j], nmat[:, j], bmat[:, j], b_Sp1_vec[j] = \
                hh.get_cnb_vecs(c1, rpath, wpath, cnb_args)
        K_new, K_cnstr = aggr.get_K(bmat, lambdas)
        L_new = aggr.get_L(nmat, emat, lambdas)
        KL_new = np.array([K_new, L_new])
        dist_SS = ((KL_new - KL_init) ** 2).sum()
        KL_init = xi_SS * KL_new + (1 - xi_SS) * KL_init
        print('SS Iteration=', iter_SS, ', SS Distance=',
              '%10.4e' % (dist_SS), ',K:', '%10.4e' % (K_new),
              'L:', '%10.4e' % (L_new))

    K_ss, L_ss = KL_init
    r_ss = firms.get_r(r_params, K_ss, L_ss)
    w_ss = firms.get_w(w_params, K_ss, L_ss)
    c_ss = cmat
    n_ss = nmat
    b_ss = bmat
    b_Sp1_ss = b_Sp1_vec
    Y_params = (A, alpha)
    Y_ss = aggr.get_Y(Y_params, K_ss, L_ss)
    C_ss = aggr.get_C(c_ss, lambdas)
    n_err_ss = np.zeros((S, J))
    b_err_ss = np.zeros((S - 1, J))
    for j in range(J):
        n_err_params = (emat[:, j], sigma, l_tilde, chi_n_vec, b_ellip,
                        upsilon)
        n_err_ss[:, j] = hh.get_n_errors(n_err_params, w_ss, c_ss[:, j],
                                         n_ss[:, j], EulDiff)
        b_err_params = (beta, sigma)
        b_err_ss[:, j] = hh.get_b_errors(b_err_params, r_ss, c_ss[:, j],
                                         EulDiff)
    RCerr_ss = Y_ss - C_ss - delta * K_ss

    ss_time = time.clock() - start_time

    ss_output = {
        'n_ss': n_ss, 'b_ss': b_ss, 'c_ss': c_ss, 'b_Sp1_ss': b_Sp1_ss,
        'w_ss': w_ss, 'r_ss': r_ss, 'K_ss': K_ss, 'L_ss': L_ss,
        'Y_ss': Y_ss, 'C_ss': C_ss, 'n_err_ss': n_err_ss,
        'b_err_ss': b_err_ss, 'RCerr_ss': RCerr_ss, 'ss_time': ss_time}
    print('K_ss=', K_ss, ', L_ss=', L_ss)
    print('r_ss=', r_ss, ', w_ss=', w_ss)
    print('Maximum abs. labor supply Euler error is: ',
          np.absolute(n_err_ss).max())
    print('Maximum abs. savings Euler error is: ',
          np.absolute(b_err_ss).max())
    print('Resource constraint error is: ', RCerr_ss)
    print('Max. absolute SS residual savings b_Sp1_j is: ',
          np.absolute(b_Sp1_ss).max())

    # Print SS computation time
    utils.print_time(ss_time, 'SS')

    if graphs:
        '''
        ----------------------------------------------------------------
        cur_path    = string, path name of current directory
        output_fldr = string, folder in current path to save files
        output_dir  = string, total path of images folder
        output_path = string, path of file name of figure to be saved
        sgrid       = (S,) vector, ages from 1 to S
        lamcumsum   = (J,) vector, cumulative sum of lambdas vector
        jmidgrid    = (J,) vector, midpoints of ability percentile bins
        smat        = (J, S) matrix, sgrid copied down J rows
        jmat        = (J, S) matrix, jmidgrid copied across S columns
        ----------------------------------------------------------------
        '''
        # Create directory if images directory does not already exist
        cur_path = os.path.split(os.path.abspath(__file__))[0]
        output_fldr = 'images'
        output_dir = os.path.join(cur_path, output_fldr)
        if not os.access(output_dir, os.F_OK):
            os.makedirs(output_dir)

        # Plot 3D steady-state consumption distribution
        sgrid = np.arange(1, S + 1)
        lamcumsum = lambdas.cumsum()
        jmidgrid = 0.5 * lamcumsum + 0.5 * (lamcumsum - lambdas)
        smat, jmat = np.meshgrid(sgrid, jmidgrid)
        cmap_c = cm.get_cmap('summer')
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.set_xlabel(r'age-$s$')
        ax.set_ylabel(r'ability-$j$')
        ax.set_zlabel(r'indiv. consumption $c_{j,s}$')
        ax.plot_surface(smat, jmat, c_ss.T, rstride=1,
                        cstride=6, cmap=cmap_c)
        output_path = os.path.join(output_dir, 'c_ss_3D')
        plt.savefig(output_path)
        # plt.show()
        plt.close()

        # Plot 2D steady-state consumption distribution
        minorLocator = MultipleLocator(1)
        fig, ax = plt.subplots()
        linestyles = np.array(["-", "--", "-.", ":"])
        markers = np.array(["x", "v", "o", "d", ">", "|"])
        pct_lb = 0
        for j in range(J):
            this_label = (str(int(np.rint(pct_lb))) + " - " +
                          str(int(np.rint(pct_lb + 100 * lambdas[j]))) +
                          "%")
            pct_lb += 100 * lambdas[j]
            if j <= 3:
                ax.plot(sgrid, c_ss[:, j], label=this_label,
                        linestyle=linestyles[j], color='black')
            elif j > 3:
                ax.plot(sgrid, c_ss[:, j], label=this_label,
                        marker=markers[j - 4], color='black')
        ax.xaxis.set_minor_locator(minorLocator)
        plt.grid(b=True, which='major', color='0.65', linestyle='-')
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        ax.set_xlabel(r'age-$s$')
        ax.set_ylabel(r'indiv. consumption $c_{j,s}$')
        output_path = os.path.join(output_dir, 'c_ss_2D')
        plt.savefig(output_path)
        # plt.show()
        plt.close()


        # Plot 3D steady-state labor supply distribution
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.set_xlabel(r'age-$s$')
        ax.set_ylabel(r'ability-$j$')
        ax.set_zlabel(r'labor supply $n_{j,s}$')
        ax.plot_surface(smat, jmat, n_ss.T, rstride=1,
                        cstride=6, cmap=cmap_c)
        output_path = os.path.join(output_dir, 'n_ss_3D')
        plt.savefig(output_path)
        # plt.show()
        plt.close()

        # Plot 2D steady-state labor supply distribution
        minorLocator = MultipleLocator(1)
        fig, ax = plt.subplots()
        linestyles = np.array(["-", "--", "-.", ":"])
        markers = np.array(["x", "v", "o", "d", ">", "|"])
        pct_lb = 0
        for j in range(J):
            this_label = (str(int(np.rint(pct_lb))) + " - " +
                          str(int(np.rint(pct_lb + 100 * lambdas[j]))) +
                          "%")
            pct_lb += 100 * lambdas[j]
            if j <= 3:
                ax.plot(sgrid, n_ss[:, j], label=this_label,
                        linestyle=linestyles[j], color='black')
            elif j > 3:
                ax.plot(sgrid, n_ss[:, j], label=this_label,
                        marker=markers[j - 4], color='black')
        ax.xaxis.set_minor_locator(minorLocator)
        plt.grid(b=True, which='major', color='0.65', linestyle='-')
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        ax.set_xlabel(r'age-$s$')
        ax.set_ylabel(r'labor supply $n_{j,s}$')
        output_path = os.path.join(output_dir, 'n_ss_2D')
        plt.savefig(output_path)
        # plt.show()
        plt.close()


        # Plot 3D steady-state savings/wealth distribution
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.set_xlabel(r'age-$s$')
        ax.set_ylabel(r'ability-$j$')
        ax.set_zlabel(r'indiv. savings $b_{j,s}$')
        ax.plot_surface(smat, jmat, b_ss.T, rstride=1,
                        cstride=6, cmap=cmap_c)
        output_path = os.path.join(output_dir, 'b_ss_3D')
        plt.savefig(output_path)
        # plt.show()
        plt.close()

        # Plot 2D steady-state savings/wealth distribution
        fig, ax = plt.subplots()
        linestyles = np.array(["-", "--", "-.", ":"])
        markers = np.array(["x", "v", "o", "d", ">", "|"])
        pct_lb = 0
        for j in range(J):
            this_label = (str(int(np.rint(pct_lb))) + " - " +
                          str(int(np.rint(pct_lb + 100 * lambdas[j]))) +
                          "%")
            pct_lb += 100 * lambdas[j]
            if j <= 3:
                ax.plot(sgrid, b_ss[:, j], label=this_label,
                        linestyle=linestyles[j], color='black')
            elif j > 3:
                ax.plot(sgrid, b_ss[:, j], label=this_label,
                        marker=markers[j - 4], color='black')
        ax.xaxis.set_minor_locator(minorLocator)
        plt.grid(b=True, which='major', color='0.65', linestyle='-')
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        ax.set_xlabel(r'age-$s$')
        ax.set_ylabel(r'indiv. savings $b_{j,s}$')
        output_path = os.path.join(output_dir, 'b_ss_2D')
        plt.savefig(output_path)
        # plt.show()
        plt.close()

    return ss_output
