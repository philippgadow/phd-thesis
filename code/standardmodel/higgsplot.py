import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import atlas_mpl_style as ampl


def higgsPotential(x, y, mh=125., v=246.):
    # Higgs potential parameters in dependency of Higgs mass and VEV
    mu = mh / np.sqrt(2)
    mu2 = - np.power(mh, 2) / 2
    lbd = np.abs(mu2) / (np.power(v,2))
    r = np.linalg.norm([x, y], axis=0)
    return np.add(mu2 * (np.power(r,2)), lbd * np.power(r, 4))


def higgsPotential1D(r, mh=125., v=246.):
    # Higgs potential parameters in dependency of Higgs mass and VEV
    mu = mh / np.sqrt(2)
    mu2 = - np.power(mh, 2) / 2
    lbd = np.abs(mu2) / (np.power(v,2))
    return np.add(mu2 * (np.power(r,2)), lbd * np.power(r, 4))


def makePlot():
    # Higgs boson potential (2D plot)
    x = y = np.arange(-250.0, 250.0, 1.)
    X, Y = np.meshgrid(x, y)
    Z = higgsPotential(X, Y)

    # set up figure and grid
    fig = plt.figure()
    gs = fig.add_gridspec(4, 4)
    ax_re = fig.add_subplot(gs[3, 1:4])
    ax_im = fig.add_subplot(gs[0:3, 0])
    ax = fig.add_subplot(gs[0:3, 1:4], sharex=ax_re, sharey=ax_im)

    # 1D projections of Higgs potential
    ax_re.plot(x, higgsPotential1D(x), color='blue', linestyle='-')
    mu2 = np.power(125., 2) / 2
    lbd = np.abs(mu2) / (np.power(246.,2))
    minimum = - np.power(mu2, 2) / (4*lbd)
    ax_re.plot([0., 246. / np.sqrt(2)], [minimum, minimum], color='orange', linestyle='-', linewidth=2)
    ax_im.plot(higgsPotential1D(y), y, color='blue', linestyle='-')

    # plot 2D Higgs potential
    im = ax.contourf(X, Y, Z, levels=100, cmap='plasma')
    # add line for real Higgs boson
    ax.plot([0., 246. / np.sqrt(2)], [0., 0.], color='orange', linestyle='-', linewidth=2)

    # create colour bar
    fig.subplots_adjust(bottom=0.1, top=0.9, left=0.1, right=0.8)
    cb_ax = fig.add_axes([0.83, 0.1, 0.02, 0.8])
    cbar = fig.colorbar(im, cax=cb_ax)
    cbar.ax.set_ylabel('$V(\phi)$', rotation=-90, va="center")

    # style
    plt.setp(ax.get_xticklabels(), visible=False)
    plt.setp(ax.get_yticklabels(), visible=False)
    ax_re.set_xlabel('Re$(\phi)$')
    ax_re.set_ylabel('$V(\phi)$')
    ax_re.set_xlim([-250, 250])
    ax_re.ticklabel_format(style='plain')
    plt.setp(ax_re.get_yticklabels(), visible=False)
    ax_im.set_xlabel('$V(\phi)$')
    ax_im.set_ylabel('Im$(\phi)$')
    ax_im.set_ylim([-250, 250])
    ax_im.ticklabel_format(style='plain')
    plt.setp(ax_im.get_xticklabels(), visible=False)
    plt.subplots_adjust(wspace=0., hspace=0.)

    # save figure
    fig.savefig('sm_higgs.pdf')


def main():
    # set style
    ampl.use_atlas_style()
    ampl.set_color_cycle(pal='Paper', n=2)

    # make plot
    makePlot()


if __name__ == '__main__':
    main()
