import numpy as np
import matplotlib.pyplot as plt
import atlas_mpl_style as ampl

# use ATLAS style
ampl.use_atlas_style()
ampl.set_color_cycle(pal='Paper', n=4)

def lowercut_w_mass(pt):
    #if pt > 2500:
    #    return  60.0593267161
    return np.sqrt(np.power((-8680.2717943)/pt-(-54.2916959506),2)+np.power((0.0142530985867)*pt+(-67.640437403),2))
def uppercut_w_mass(pt):
    #if pt > 2500:
    #    return 99.824544933
    return np.sqrt(np.power((79.4993903251)/pt-(-94.0432300643),2)+np.power((0.0201350277197)*pt+(-16.9485211641),2))
def uppercut_w_d2(pt):
    # if pt > 2500:
    #    return 2.01439576478
    return (0.827098899953)+(0.00117390855197)*pt+(-7.27657125295e-07)*np.power(pt,2.0)+(3.46942900597e-10)*np.power(pt,3.0)+(-6.7087367778e-14)*np.power(pt,4.0)

def lowercut_z_mass(pt):
    #if pt > 2500:
    #    return 69.4240299485
    return np.sqrt(np.power((-8911.32152025)/pt-(-72.3863305346),2)+np.power((0.0232216747865)*pt+(-67.1786329156),2))
def uppercut_z_mass(pt):
    #if pt > 2500:
    #    return 109.831901054
    return np.sqrt(np.power((428.215902774)/pt-(-105.538285882),2)+np.power((0.0192931557406)*pt+(-18.4246216168),2))

def uppercut_z_d2(pt):
    # if pt > 2500:
    #    return 1.90713763304
    return (0.86245030986)+(0.0010301169875)*pt+(-6.37151804335e-07)*np.power(pt,2.0)+(2.95602462111e-10)*np.power(pt,3.0)+(-5.54801878773e-14)*np.power(pt,4.0)


def main():
    pt = np.arange(200., 2700.)

    fig, ax = plt.subplots(2,2, sharex=True, figsize=(16,8))

    # W boson tagger mass
    ax[0][0].set_title('$W$ boson tagger')
    ax[0][0].plot(pt, uppercut_w_mass(pt), 'b--')
    ax[0][0].plot(pt, lowercut_w_mass(pt), 'b--')
    ax[0][0].fill_between(pt, uppercut_w_mass(pt), 110, color='orange', alpha=0.5)
    ax[0][0].fill_between(pt, 50, lowercut_w_mass(pt), color='orange', alpha=0.5)
    ax[0][0].set_ylim((50, 110))
    ampl.plot.set_ylabel('$m_{V}$ [GeV]', ax=ax[0][0])

    ax[0][0].text(0.6, 0.5, "W boson mass window",
        verticalalignment='center', horizontalalignment='center',
        transform=ax[0][0].transAxes, color='#999999', fontsize=16)

    ax[0][0].text(0.35, 0.88, "W boson mass side-band",
        verticalalignment='center', horizontalalignment='center',
        transform=ax[0][0].transAxes, color='#999999', fontsize=16)

    ax[0][0].text(0.2, 0.15, "rejected",
        verticalalignment='center', horizontalalignment='center',
        transform=ax[0][0].transAxes, color='#999999', fontsize=16)


    # W boson tagger D2
    ax[1][0].plot(pt, uppercut_w_d2(pt), 'r--')
    ax[1][0].fill_between(pt, uppercut_w_d2(pt), 2.35, color='red', alpha=0.5)
    ax[1][0].set_ylim((0., 2.35))
    ax[1][0].set_xlim((200., 2700.))
    ampl.plot.set_ylabel('$D_{2}^{\\beta=1}$', ax=ax[1][0])
    ampl.plot.set_xlabel('$p_{T}$ [GeV]', ax=ax[1][0])

    ax[1][0].text(0.6, 0.35, "W boson high purity selection",
        verticalalignment='center', horizontalalignment='center',
        transform=ax[1][0].transAxes, color='#999999', fontsize=16)

    ax[1][0].text(0.3, 0.85, "W boson low purity selection",
        verticalalignment='center', horizontalalignment='center',
        transform=ax[1][0].transAxes, color='#EEEEEE', fontsize=16)


    # Z boson tagger mass
    ax[0][1].set_title('$Z$ boson tagger')
    ax[0][1].plot(pt, uppercut_z_mass(pt), 'b--')
    ax[0][1].plot(pt, lowercut_z_mass(pt), 'b--')
    ax[0][1].fill_between(pt, uppercut_z_mass(pt), 120, color='orange', alpha=0.5)
    ax[0][1].fill_between(pt, 60, lowercut_z_mass(pt), color='orange', alpha=0.5)
    ax[0][1].set_ylim((60, 120))
    ampl.plot.set_ylabel('$m_{V}$ [GeV]', ax=ax[0][1])

    ax[0][1].text(0.6, 0.5, "Z boson mass window",
        verticalalignment='center', horizontalalignment='center',
        transform=ax[0][1].transAxes, color='#999999', fontsize=16)

    ax[0][1].text(0.4, 0.88, "Z boson mass side-band",
        verticalalignment='center', horizontalalignment='center',
        transform=ax[0][1].transAxes, color='#999999', fontsize=16)

    ax[0][1].text(0.2, 0.15, "rejected",
        verticalalignment='center', horizontalalignment='center',
        transform=ax[0][1].transAxes, color='#999999', fontsize=16)

    # Z boson tagger D2
    ax[1][1].plot(pt, uppercut_z_d2(pt), 'r--')
    ax[1][1].fill_between(pt, uppercut_z_d2(pt), 2.25, color='red', alpha=0.5)
    ampl.plot.set_ylabel('$D_{2}^{\\beta=1}$', ax=ax[1][1])
    ampl.plot.set_xlabel('$p_{T}$ [GeV]', ax=ax[1][1])
    ax[1][1].set_ylim((0., 2.25))
    ax[1][1].set_xlim((200., 2700.))

    ax[1][1].text(0.6, 0.35, "Z boson high purity selection",
        verticalalignment='center', horizontalalignment='center',
        transform=ax[1][1].transAxes, color='#999999', fontsize=16)

    ax[1][1].text(0.3, 0.85, "Z boson low purity selection",
        verticalalignment='center', horizontalalignment='center',
        transform=ax[1][1].transAxes, color='#EEEEEE', fontsize=16)

    fig.savefig('monoVtagger.png')

if __name__ == '__main__':
    main()
