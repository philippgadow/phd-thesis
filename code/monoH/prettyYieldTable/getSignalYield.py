import ROOT


def getHistoYield1(h1):
    h = h1.Clone()
    e = ROOT.Double(0.)
    y = h.IntegralAndError(h.GetXaxis().GetFirst(), h.GetXaxis().GetLast(), e)
    return y, e


def getHistoYield2(h1, h2):
    h = h1.Clone()
    h.Add(h2)
    e = ROOT.Double(0.)
    y = h.IntegralAndError(h.GetXaxis().GetFirst(), h.GetXaxis().GetLast(), e)
    return y, e


def getHistoYield3(h1, h2, h3):
    h = h1.Clone()
    h.Add(h2)
    h.Add(h3)
    e = ROOT.Double(0.)
    y = h.IntegralAndError(h.GetXaxis().GetFirst(), h.GetXaxis().GetLast(), e)
    return y, e


def main():
    f = ROOT.TFile.Open("data/monoV_13TeV_0lep_mj_truthtag.root")

    signals = [("dmVWhadDM1MM200", "dmVZhadDM1MM200"), ("dmVWhadDM1MM600", "dmVZhadDM1MM600")]
    signals_VHinv = [["qqZqqHinv", "ggZqqHinv", "qqWqqHinv"], ["ggHinv"], ["VBFHinv"]]
    regions = ["_0tag1pfat0pjet_0ptv_0lep_SR_SubstrPassMassPass_MET",
               "_0tag1pfat0pjet_0ptv_0lep_SR_SubstrFailMassPass_MET",
               "_1tag1pfat0pjet_0ptv_0lep_SR_SubstrPassMassPass_MET",
               "_1tag1pfat0pjet_0ptv_0lep_SR_SubstrFailMassPass_MET",
               "_2tag1pfat0pjet_0ptv_0lep_SR_MassPass_MET",
               "_0tag0pfat0pjet_0ptv_0lep_SR_MassPass_MET",
               "_1tag0pfat0pjet_0ptv_0lep_SR_MassPass_MET",
               "_2tag0pfat0pjet_0ptv_0lep_SR_MassPass_MET",
               "_0tag1pfat0pjet_0ptv_0lep_SR_SubstrPassMassFailHigh_MET",
               "_0tag1pfat0pjet_0ptv_0lep_SR_SubstrFailMassFailHigh_MET",
               "_1tag1pfat0pjet_0ptv_0lep_SR_SubstrPassMassFailHigh_MET",
               "_1tag1pfat0pjet_0ptv_0lep_SR_SubstrFailMassFailHigh_MET",
               "_2tag1pfat0pjet_0ptv_0lep_SR_MassFailHigh_MET",
               "_0tag0pfat0pjet_0ptv_0lep_SR_MassFailHigh_MET",
               "_1tag0pfat0pjet_0ptv_0lep_SR_MassFailHigh_MET",
               "_2tag0pfat0pjet_0ptv_0lep_SR_MassFailHigh_MET"]

    for signal in signals:
        for region in regions:
            name_h1 = signal[0] + region
            name_h2 = signal[1] + region
            h1 = f.Get(name_h1)
            h2 = f.Get(name_h2)

            y, e = getHistoYield2(h1, h2)
            print("{signal} {region} {y:.2f} $\pm$ {e:.2f}".format(signal=signal[0].replace("Whad", "Vhad"), region=(("merged" if "1pfat" in region else "resolved") + region[1:5] + region.split('_')[-2]), y=y, e=e))

    for signal in signals_VHinv:
        for region in regions:
            name_h1 = signal[0] + region
            h1 = f.Get(name_h1)

            if len(signal) > 1:
                name_h2 = signal[0] + region
                h2 = f.Get(name_h2)

                name_h3 = signal[0] + region
                h3 = f.Get(name_h3)

                y, e = getHistoYield3(h1, h2, h3)
                print("{signal} {region} {y:.2f} $\pm$ {e:.2f}".format(signal=signal[0].replace("qqZqqHinv", "VH"), region=(("merged" if "1pfat" in region else "resolved") + region[1:5] + region.split('_')[-2]), y=y, e=e))
            else:
                y, e = getHistoYield1(h1)
                print("{signal} {region} {y:.2f} $\pm$ {e:.2f}".format(signal=signal[0].replace("ggHinv", "ggH"), region=(("merged" if "1pfat" in region else "resolved") + region[1:5] + region.split('_')[-2]), y=y, e=e))


if __name__ == "__main__":
    main()
