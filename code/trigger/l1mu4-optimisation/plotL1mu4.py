from uproot.rootio import open
from argparse import ArgumentParser
from uncertainties import unumpy
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import atlas_mpl_style as ampl

# use ATLAS style
ampl.use_atlas_style()
ampl.set_color_cycle(pal='Paper', n=4)

def getArgParser():
    parser = ArgumentParser()
    parser.add_argument("data")
    return parser

def two_ratio_axes():
    "Splits axes for ratio plots. Returns fig, main_axes, ratio_axes."
    fig = plt.figure(figsize=(8, 8), dpi=600)
    gs = mpl.gridspec.GridSpec(6, 1, hspace=0.0, wspace=0.0)
    ax0 = fig.add_subplot(gs[0:4])
    ax0.tick_params(labelbottom=False)
    ax1 = fig.add_subplot(gs[4], sharex=ax0)
    ax1.tick_params(labelbottom=False)
    ax1.yaxis.set_major_locator(
        mpl.ticker.MaxNLocator(symmetric=True, prune="both", min_n_ticks=5, nbins=4)
    )
    ax2 = fig.add_subplot(gs[5], sharex=ax0)
    ax2.yaxis.set_major_locator(
        mpl.ticker.MaxNLocator(symmetric=True, prune="both", min_n_ticks=5, nbins=4)
    )
    ax2.autoscale(axis="x", tight=True)
    return fig, ax0, ax1, ax2


def makeRatePlot(data):
    # get histograms
    h_l1mu4 = data['hEta_L1MU4']
    h_l1mu4_matched = data['hMuonMatched']

    h_l1mu4_optimised = data['hEta_L1MU4new']
    h_l1mu4_matched_optimised = data['hMuonMatchedNew']

    # make canvas
    fig, ax0, ax1, ax2 = two_ratio_axes()

    # plot histograms
    ampl.plot.plot_1d("L1MU4", h_l1mu4.edges, h_l1mu4.values, ax=ax0)
    ampl.plot.plot_1d("L1MU4 (optimised)", h_l1mu4_optimised.edges, h_l1mu4_optimised.values, ax=ax0)
    ampl.plot.plot_1d("Matched with rec. $\mu$ ", h_l1mu4_optimised.edges, h_l1mu4_optimised.values, ax=ax0)
    ampl.plot.plot_1d("Matched with rec. $\mu$ (optimised)", h_l1mu4_matched_optimised.edges, h_l1mu4_matched_optimised.values, ax=ax0)

    ampl.plot.plot_ratio(h_l1mu4.edges, h_l1mu4_optimised.values, np.sqrt(h_l1mu4_optimised.variances),
                                        h_l1mu4.values, np.sqrt(h_l1mu4.variances),
                                        ratio_ax=ax1, max_ratio=1.05, plottype="raw")
    ampl.plot.plot_ratio(h_l1mu4_matched.edges, h_l1mu4_matched_optimised.values, np.sqrt(h_l1mu4_matched_optimised.variances),
                                        h_l1mu4_matched.values, np.sqrt(h_l1mu4_matched.variances),
                                        ratio_ax=ax2, max_ratio=1.05, plottype="raw")

    # label axes
    ampl.plot.set_xlabel("$\eta$")
    ampl.plot.set_ylabel("Events", ax=ax0)
    ampl.plot.set_ylabel("Ratio \n L1MU4", ax=ax1)
    ampl.plot.set_ylabel("Ratio matched \n with rec. $\mu$", ax=ax2)


    # set axis limits
    ax0.set_ylim((0.01, 85000))
    ax1.set_ylim((0.6, 1.1))
    ax1.set_yticks([0.7, 1.0])
    ax2.set_ylim((0.8, 1.2))
    ax2.set_yticks([0.9, 1.0, 1.1])

    # add legend
    ax0.legend(frameon=False, loc='upper left')

    # save plot
    fig.savefig('l1mu4_rate_eta.pdf')



def makeEfficiencyPlots(data):
    # get histograms
    h_l1mu4_all_pt_probe = data['hMuPt_0_0']
    h_l1mu4_all_pt_matched = data['hMuPt_1_0']
    h_l1mu4_all_pt_matched_optimised = data['hMuPt_0_1']

    h_l1mu4_forward_pt_probe = data['hMuPt_Forward_0_0']
    h_l1mu4_forward_pt_matched = data['hMuPt_Forward_1_0']
    h_l1mu4_forward_pt_matched_optimised = data['hMuPt_Forward_0_1']

    h_l1mu4_all_eta_probe = data['hMuEta_0_0']
    h_l1mu4_all_eta_matched = data['hMuEta_1_0']
    h_l1mu4_all_eta_matched_optimised = data['hMuEta_0_1']

    h_l1mu4_all_phi_probe = data['hMuPhi_0_0']
    h_l1mu4_all_phi_matched = data['hMuPhi_1_0']
    h_l1mu4_all_phi_matched_optimised = data['hMuPhi_0_1']


    # calculate efficiencies
    def getEfficiency(h_nom, h_denom):
        def clopper_pearson_interval(num, denom, coverage=None):
            """Compute Clopper-Pearson coverage interval for a binomial distribution
            Parameters
            ----------
                num : numpy.ndarray
                    Numerator, or number of successes, vectorized
                denom : numpy.ndarray
                    Denominator or number of trials, vectorized
                coverage : float, optional
                    Central coverage interval, defaults to 68%
            c.f. http://en.wikipedia.org/wiki/Binomial_proportion_confidence_interval
            """
            import scipy.stats
            _coverage1sd = scipy.stats.norm.cdf(1) - scipy.stats.norm.cdf(-1)
            if not coverage: coverage = _coverage1sd
            if np.any(num > denom):
                raise ValueError("Found numerator larger than denominator while calculating binomial uncertainty")
            lo = scipy.stats.beta.ppf((1 - coverage) / 2, num, denom - num + 1)
            hi = scipy.stats.beta.ppf((1 + coverage) / 2, num + 1, denom - num)
            interval = np.array([lo, hi])
            interval[:, num == 0.] = 0.
            interval[1, num == denom] = 1.
            return interval

        sumw_num = h_nom.values
        sumw_denom = h_denom.values
        rsumw = np.divide(h_nom.values, h_denom.values, out=np.zeros_like(h_nom.values), where=h_denom.values!=0)
        rsumw_err = np.abs(clopper_pearson_interval(sumw_num, sumw_denom) - rsumw)
        return rsumw, rsumw_err

    eff_all_pt, eff_all_pt_err = getEfficiency(h_l1mu4_all_pt_matched, h_l1mu4_all_pt_probe)
    eff_all_pt_optimised, eff_all_pt_optimised_err = getEfficiency(h_l1mu4_all_pt_matched_optimised, h_l1mu4_all_pt_probe)

    eff_forward_pt, eff_forward_pt_err = getEfficiency(h_l1mu4_forward_pt_matched, h_l1mu4_forward_pt_probe)
    eff_forward_pt_optimised, eff_forward_pt_optimised_err = getEfficiency(h_l1mu4_forward_pt_matched_optimised, h_l1mu4_forward_pt_probe)

    eff_all_eta, eff_all_eta_err = getEfficiency(h_l1mu4_all_eta_matched, h_l1mu4_all_eta_probe)
    eff_all_eta_optimised, eff_all_eta_optimised_err = getEfficiency(h_l1mu4_all_eta_matched_optimised, h_l1mu4_all_eta_probe)

    eff_all_phi, eff_all_phi_err = getEfficiency(h_l1mu4_all_phi_matched, h_l1mu4_all_phi_probe)
    eff_all_phi_optimised, eff_all_phi_optimised_err = getEfficiency(h_l1mu4_all_phi_matched_optimised, h_l1mu4_all_phi_probe)

    # make plots
    edges = [h_l1mu4_all_pt_probe.edges, h_l1mu4_forward_pt_probe.edges, h_l1mu4_all_eta_probe.edges, h_l1mu4_all_phi_probe.edges]
    h1 = [eff_all_pt_optimised, eff_forward_pt_optimised, eff_all_eta_optimised, eff_all_phi_optimised]
    h2 = [eff_all_pt, eff_forward_pt, eff_all_eta, eff_all_phi]
    e1 = [eff_all_pt_optimised_err, eff_forward_pt_optimised_err, eff_all_eta_optimised_err, eff_all_phi_optimised_err]
    e2 = [eff_all_pt_err, eff_forward_pt_err, eff_all_eta_err, eff_all_phi_optimised_err]
    xlabel = ["$p_{T}$ [GeV]", "$p_{T}$ [GeV]", "$\eta$", "$\phi$"]
    xlimits = [(2., 20.), (2., 20.), (-2.4, 2.4), (-3.2, 3.2)]
    outname = ['l1mu4_eff_pt_all.pdf', 'l1mu4_eff_pt_forward.pdf', 'l1mu4_eff_eta.pdf', 'l1mu4_eff_phi.pdf']

    for (e, hnom, hdenom, enom, edenom, x, xlim, o) in zip(edges, h1, h2, e1, e2, xlabel, xlimits, outname):
        # make canvas
        fig, ax0, ax1 = ampl.ratio_axes()

        # plot histograms
        ax0.errorbar(x=e[:-1], y=hnom, yerr=enom, color='blue', linestyle='none', fmt='.', label="L1MU4")
        ax0.errorbar(x=e[:-1], y=hdenom, yerr=edenom, color='orange', linestyle='none', fmt='.', label="L1MU4 (optimised)")

        def symm(err): return 0.5 * (err[0] + err[1])
        ampl.plot.plot_ratio(e,
            hnom, symm(enom),
            hdenom, symm(edenom),
            ratio_ax=ax1, max_ratio=1.05, plottype="raw")

        # label axes
        ampl.plot.set_xlabel(x)
        ampl.plot.set_ylabel("Efficiency", ax=ax0)
        ampl.plot.set_ylabel("Ratio", ax=ax1)

        # set axis range
        ax0.set_xlim(xlim)
        ax0.set_ylim((-0.01, 1.1))
        ax1.set_ylim((0.97, 1.03))
        ax1.set_yticks([0.98, 1.0, 1.02])

        # add legend
        ax0.legend(frameon=False, loc='lower right')

        # save plot
        fig.savefig(o)




def makeMuonPlots(data):
    # get histograms
    h_tap_pt_tag = data['hControl_3_MuTagPt']
    h_tap_pt_probe = data['hControl_3_MuProbePt']

    h_tap_eta_tag = data['hControl_3_MuTagEta']
    h_tap_eta_probe = data['hControl_3_MuProbeEta']

    h_tap_phi_tag = data['hControl_3_MuTagPhi']
    h_tap_phi_probe = data['hControl_3_MuProbePhi']

    # make plots
    htag = [h_tap_pt_tag, h_tap_eta_tag, h_tap_phi_tag]
    hprobe = [h_tap_pt_probe, h_tap_eta_probe, h_tap_phi_probe]
    xlabel = ['$p_{T}$ [GeV]', '$\eta$', '$\phi$']
    xlim = [(0, 20), (-2.5, 2.5), (-4, 4)]
    ylim = [(0, 14000), (0, 10000), (0, 14000)]

    filename = ['l1mu4_muon_pt.pdf', 'l1mu4_muon_eta.pdf', 'l1mu4_muon_phi.pdf']
    for (ht, hp, l, x, y, f) in zip(htag, hprobe, xlabel, xlim, ylim, filename):
        # make canvas
        fig = plt.figure(figsize=(6, 6), dpi=600)
        ax0 = fig.add_subplot()

        # plot histograms
        ampl.plot.plot_1d("Tag $\mu$", ht.edges, ht.values, ax=ax0, color='blue')
        ampl.plot.plot_1d("Probe $\mu$ ", hp.edges, hp.values, ax=ax0, color='orange')

        # label axes
        ampl.plot.set_xlabel(l)
        ampl.plot.set_ylabel("Events")

        # set axis range
        ax0.set_xlim(x)
        ax0.set_ylim(y)

        # legend
        ax0.legend(frameon=False, loc='upper left')

        # save plot
        fig.savefig(f)


def makeDiMuonMassPlot(data):
    # get histogram
    h_tap_mumu_mass = data['hControl_3_MuMuMass']

    # make canvas
    fig = plt.figure(figsize=(6, 6), dpi=600)
    ax0 = fig.add_subplot()

    # plot histograms
    ampl.plot.plot_1d("$\mu\mu$ mass", h_tap_mumu_mass.edges, h_tap_mumu_mass.values, ax=ax0, color='blue')

    # label axes
    ampl.plot.set_xlabel('$m_{\mu^{\pm}\mu^{\mp}}$ [GeV]')
    ampl.plot.set_ylabel("Events")

    # set axis range
    ax0.set_xlim((2.55, 3.65))

    # save plot
    fig.savefig('l1mu4_dimuon_mass.pdf')


def main():
    args = getArgParser().parse_args()

    data = open(args.data)
    makeRatePlot(data)
    makeMuonPlots(data)
    makeDiMuonMassPlot(data)
    makeEfficiencyPlots(data)

if __name__ == '__main__':
    main()
