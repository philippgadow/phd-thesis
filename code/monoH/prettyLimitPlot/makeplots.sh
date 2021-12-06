mkdir -p plots/limitplot
python prettyLimitPlot.py data/graphs/zp2hdm_Limits_rel21_79p8invFb_2t.root
mv monoHbb-95CLsLimitPlot.* plots/limitplot

mkdir -p plots/2tag/mA{300,400,500}
python prettyExpectedLimitPlot.py data/graphs/zp2hdm_Limits_rel21_79p8invFb_2t.root -e data/graphs/zp2hdm_expLimit_rel20p7_79p8invFb_2t.root
mv monoHbb-95CLsExpectedLimitPlot.* plots/2tag
python prettyMuLimitPlot_ratio.py data/mulimits/release21.79p8.2b/fixed_mA/data/mA500.dat data/mulimits/release20p8.79p8.2b/fixed_mA/data/mA500.dat
mv monoHbb-expmulimitratio.* plots/2tag/mA500/

mkdir -p plots/12tag/mA{300,400,500}
python prettyExpectedLimitPlot.py data/graphs/zp2hdm_Limits_rel21_79p8invFb_2t.root -e data/graphs/zp2hdm_expLimit_rel20p7_79p8invFb_12t.root --tag12
mv monoHbb-95CLsExpectedLimitPlot.* plots/12tag
python prettyMuLimitPlot_ratio.py data/mulimits/release21.79p8.2b/fixed_mA/data/mA500.dat data/mulimits/release20p8.79p8.12b/fixed_mA/data/mA500.dat --tag12
mv monoHbb-expmulimitratio.* plots/12tag/mA500/