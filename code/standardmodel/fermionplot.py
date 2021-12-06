import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import atlas_mpl_style as ampl

# PDG information
from particle import Particle


def getData():
	return {
		'd': Particle.from_pdgid(1),
		'u': Particle.from_pdgid(2),
		's': Particle.from_pdgid(3),
		'c': Particle.from_pdgid(4),
		'b': Particle.from_pdgid(5),
		't': Particle.from_pdgid(6),
		'e': Particle.from_pdgid(11),
		'nu_e': Particle.from_pdgid(12),
		'mu': Particle.from_pdgid(13),
		'nu_mu': Particle.from_pdgid(14),
		'tau': Particle.from_pdgid(15),
		'nu_tau': Particle.from_pdgid(16)
		}


def makePlot(d):
	fig, ax = plt.subplots(2, 1, sharex=True)


	# "empirically" determined scaling factor to lepton masses to make them fit on plot
	size_scalingfactor = 0.1

	# quarks
	quarks_colorscheme = 'blue'
	quarks = [d['d'], d['u'], d['s'], d['c'], d['b'], d['t']]
	quarks_name = ['down', 'up', 'strange', 'charm', 'bottom', 'top']
	quarks_generation = [1, 1, 2, 2, 3, 3]
	quarks_charge = [q.charge for q in quarks]
	quarks_mass = np.array([q.mass for q in quarks])
	quarks_mass *= size_scalingfactor
	ax[0].scatter(quarks_generation, quarks_charge, s=quarks_mass, c=quarks_colorscheme, alpha=0.5)
	quarks_offset = [(0.0, 0.18), (0.0, -0.18), (0.0, 0.18), (0.0, -0.18), (0., 0.18), (0.0, -0.18)]
	quarks_color = [quarks_colorscheme, quarks_colorscheme, quarks_colorscheme, quarks_colorscheme, quarks_colorscheme, 'w']
	for name, generation, charge, offset, color in zip(quarks_name, quarks_generation, quarks_charge, quarks_offset, quarks_color):
		ax[0].annotate(name, (generation + offset[0], charge + offset[1]), ha='center', color=color)
	# style
	ax[0].minorticks_off()
	# x-axis style in ax[1]
	ax[0].set_yticks([2./3., -1./3])
	ax[0].set_yticklabels(["2/3", "-1/3"])
	ax[0].set_ylabel('electric charge')
	ax[0].get_yaxis().labelpad = 8.2
	# text on right y-axis
	ax0_copy = ax[0].twinx()
	ax0_copy.get_yaxis().set_ticks([])
	ax0_copy.set_ylabel('quarks', color=quarks_colorscheme)


	# leptons
	lepton_colorscheme = 'red'
	leptons = [d['nu_e'], d['e'], d['nu_mu'], d['mu'], d['nu_tau'], d['tau']]
	leptons_name = ['$\\nu_{e}$', '$e^{-}$', '$\\nu_{\\mu}$', '$\\mu^{-}$', '$\\nu_{\\tau}$', '$\\tau^{-}$']
	leptons_generation = [1, 1, 2, 2, 3, 3]
	leptons_charge = [l.charge for l in leptons]
	leptons_mass = np.array([l.mass if l.mass else 0.001 for l in leptons ])
	leptons_mass *= size_scalingfactor
	ax[1].scatter(leptons_generation, leptons_charge, s=leptons_mass, c=lepton_colorscheme, alpha=0.5)
	leptons_offset = [(0.0, -0.2), (0.0, 0.2), (0.0, -0.2), (0.0, 0.2), (0.0, -0.2), (0., 0.2)]
	leptons_color = [lepton_colorscheme, lepton_colorscheme, lepton_colorscheme, lepton_colorscheme, lepton_colorscheme, lepton_colorscheme]
	for name, generation, charge, offset, color in zip(leptons_name, leptons_generation, leptons_charge, leptons_offset, leptons_color):
		ax[1].annotate(name, (generation + offset[0], charge + offset[1]), ha='center', color=color)
	# style
	ax[1].minorticks_off()
	ax[0].set_xlim([0.5, 3.5])
	ax[1].set_xticks([1, 2, 3])
	ax[1].set_xticklabels(["I.", "II.", "III."])
	ax[1].set_xlabel('generation')
	ax[1].set_yticks([-1, 0])
	ax[1].set_yticklabels(["-1", "0"])
	ax[1].set_ylabel('electric charge')
	ax[1].set_ylim([0.2, -1.3])
	ax[1].get_yaxis().labelpad = 20
	ax1_copy = ax[1].twinx()
	ax1_copy.get_yaxis().set_ticks([])
	ax1_copy.set_ylabel('leptons', color=lepton_colorscheme)
	ax[1].invert_yaxis()

	# save figure
	fig.savefig('sm_fermions.pdf')


def main():
	# set style
	ampl.use_atlas_style()
	ampl.set_color_cycle(pal='Paper', n=2)

	# get data
	data = getData()

	# make plot
	makePlot(data)


if __name__ == '__main__':
	main()
