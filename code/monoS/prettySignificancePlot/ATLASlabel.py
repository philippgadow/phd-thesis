import matplotlib as mpl


def drawATLASLabel(x, y, ax=None, status='final', simulation=False,
                   energy=None, lumi=None, desc=None):
    """
    Draw ATLAS label.

    Parameters
    ----------
    x : float
        x position
    y : float
        y position
    ax : mpl.axes.Axes, optional
        Axes to draw label in
    status : [ 'int' | 'wip' | 'prelim' | *'final'* ], optional
        Approval status
    simulation : bool (optional, default ``False``)
        Does the plot show only MC simulation results
    energy : str, optional
        Centre of mass energy, including units
    lumi : float, optional
        Integrated luminosity in /fb
    desc : str, optional
        Additional description
    """

    # set LaTeX text setting
    mpl.rc('text', usetex=True)
    mpl.rcParams['text.latex.preamble'] = r'\usepackage{helvet} \usepackage{sansmath} \setlength{\parindent}{0pt} \sansmath'

    if ax is None:
        ax = mpl.pyplot.gca()

    # simulation string
    sim_str = "Simulation " if simulation else ""

    # status string
    if status == 'final':
        status_str = ''
    elif status == 'int':
        status_str = 'Internal'
    elif status == 'wip':
        status_str = 'Work in Progress'
    elif status == 'prelim':
        status_str = 'Preliminary'
    else:
        status_str = 'Internal (please set the status)'

    # energy string
    show_e_nl = False
    if energy is not None:
        show_e_nl = True
        energy_str = '$\sqrt{{s}} = $ {energy},  '.format(energy=energy)
    else:
        energy_str = ''

    # luminosity string
    if lumi is not None:
        show_e_nl = True
        # lumi_str = '$\displaystyle\int \\textsf{{L}}\\,\\textsf{{d}}t = {lumi:4.1f}\\textsf{{fb}}^{{-1}}$'.format(lumi=lumi)
        lumi_str = '${lumi:4.1f}\\textsf{{fb}}^{{-1}}$'.format(lumi=lumi)
    else:
        lumi_str = ''

    # description string
    show_desc_nl = False
    if desc is not None:
        show_desc_nl = True
    else:
        desc = ""

    # final label
    nl = '\n'
    nl_e = nl if show_e_nl else ""
    nl_desc = nl if show_desc_nl else ""
    label = '$\\textbf{{\\textit{{ATLAS}}}}$ {sim} {status} {nl_e}{energy}{lumi} {nl_desc}{desc}'.format(sim=sim_str, status=status_str, nl_e=nl_e, energy=energy_str, lumi=lumi_str, nl_desc=nl_desc, desc=desc)

    ax.text(x, y, label,
            verticalalignment='top', horizontalalignment='left',
            transform=ax.transAxes, fontsize=16)

def drawThesisLabel(x, y, ax=None, energy=None, lumi=None, desc=None):

    # set LaTeX text setting
    mpl.rc('text', usetex=True)
    mpl.rcParams['text.latex.preamble'] = r'\usepackage{helvet} \usepackage{sansmath} \setlength{\parindent}{0pt} \sansmath'

    if ax is None:
        ax = mpl.pyplot.gca()


    # energy string
    show_e_nl = False
    if energy is not None:
        show_e_nl = True
        energy_str = '$\sqrt{{s}} = $ {energy},  '.format(energy=energy)
    else:
        energy_str = ''

    # luminosity string
    if lumi is not None:
        show_e_nl = True
        # lumi_str = '$\displaystyle\int \\textsf{{L}}\\,\\textsf{{d}}t = {lumi:4.1f}\\textsf{{fb}}^{{-1}}$'.format(lumi=lumi)
        lumi_str = '${lumi:4.1f}\\,\\textsf{{fb}}^{{-1}}$'.format(lumi=lumi)
    else:
        lumi_str = ''

    # description string
    show_desc_nl = False
    if desc is not None:
        show_desc_nl = True
    else:
        desc = ""

    # final label
    nl = '\n'
    nl_desc = nl if show_desc_nl else ""
    label = '{energy}{lumi} {nl_desc}{desc}'.format(energy=energy_str, lumi=lumi_str, nl_desc=nl_desc, desc=desc)

    ax.text(x, y, label,
            verticalalignment='top', horizontalalignment='left',
            transform=ax.transAxes, fontsize=16)
