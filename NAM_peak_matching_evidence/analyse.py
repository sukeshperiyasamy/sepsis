import pandas as pd, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
A="/sessions/dreamy-funny-johnson/mnt/NAM_Raman_Archive"
modes=pd.read_csv(f"{A}/02_DFT_Calculation/NAM_calculated_modes_all_111.csv")
exp=pd.read_csv(f"{A}/03_Processed_Results/Experimental_peak_list.csv")
ref=pd.read_csv(f"{A}/03_Processed_Results/Experimental_reference_spectrum.csv")
cmp_=pd.read_csv(f"{A}/03_Processed_Results/Experimental_vs_DFT_comparison.csv")
W=modes[(modes.freq_scaled>=400)&(modes.freq_scaled<=1800)].copy()
E=exp.peak_cm1.values; calc=np.sort(W.freq_scaled.values)
rng=np.random.default_rng(7)
def hits(tol,c,pts=E):
    c=np.sort(c); return sum(1 for e in pts if np.min(np.abs(c-e))<=tol)
tols=np.arange(2,21,1); real=[]; mu=[]; lo=[]; hi=[]
for t in tols:
    real.append(hits(t,calc))
    s=np.array([hits(t,rng.uniform(400,1800,len(W))) for _ in range(1500)])
    mu.append(s.mean()); lo.append(np.percentile(s,5)); hi.append(np.percentile(s,95))
real=np.array(real);mu=np.array(mu)

fig,ax=plt.subplots(figsize=(8.6,5.2))
ax.fill_between(tols,lo,hi,color="0.85",label="Chance range (5–95%), random mode positions")
ax.plot(tols,mu,'--',color="0.45",lw=1.6,label="Chance mean")
ax.plot(tols,real,'o-',color="#B03030",lw=2.2,ms=6,label="Actual DFT modes")
ax.axvline(18,color="#1F4E79",ls=':',lw=1.6)
ax.text(17.6,26,"tolerance used\nin the archive\n(±18 cm⁻¹)",fontsize=8.5,color="#1F4E79",va="top",ha="right")
ax.set_xlabel("Matching tolerance (± cm⁻¹)");ax.set_ylabel("Experimental peaks matched (of 41)")
ax.set_title("NAM peak matching vs. what chance alone would give\n67 calculated modes in 400–1800 cm⁻¹ · mean spacing 20.9 cm⁻¹",fontsize=10.5)
ax.legend(fontsize=8.5,loc="upper left");ax.grid(alpha=.3);ax.set_xticks(range(2,21,2))
plt.tight_layout();plt.savefig("fig_A_tolerance_vs_chance.png",dpi=170);plt.close()

# Gold-standard overlay
gold=[(458.0,460.5),(585.0,582.1),(646.0,640.1),(872.0,873.0),(930.0,926.7),
      (1157.0,1156.2),(1190.0,1192.1),(1346.0,1345.7)]
x=ref["raman_shift_cm-1"].values;y=ref["mean_intensity"].values
y=(y-y.min())/(y.max()-y.min())
fig,ax=plt.subplots(figsize=(11,5.4))
ax.plot(x,y,color="#1F4E79",lw=1.3,label="Experimental NAM reference (mean of 22 replicates)")
for f,a in zip(W.freq_scaled,W.raman):
    ax.vlines(f,0,-0.055-0.06*(a/W.raman.max()),color="0.7",lw=1)
ax.hlines(0,400,1800,color="0.4",lw=.8)
for i,(e,c) in enumerate(gold):
    ax.vlines(c,0,-0.115,color="#B03030",lw=2)
    ax.annotate("",xy=(e,0.02),xytext=(c,-0.115),
                arrowprops=dict(arrowstyle="-",color="#B03030",lw=1,alpha=.85))
    ax.text(e,1.03,f"{e:.0f}",rotation=90,fontsize=7.5,ha="center",va="bottom",color="#B03030")
ax.text(410,-0.155,"grey ticks = all 67 calculated modes (height ∝ Raman activity)   |   red = the 8 unambiguous assignments",
        fontsize=8.5,color="0.3")
ax.set_ylim(-0.2,1.30);ax.set_xlim(400,1800)
ax.set_xlabel("Raman shift (cm⁻¹)");ax.set_ylabel("Normalised intensity")
ax.set_title("Why the overlay is hard to read: calculated mode density vs. the defensible assignments",fontsize=11)
ax.legend(fontsize=9,loc="upper right",framealpha=1).set_zorder(20);plt.tight_layout()
plt.savefig("fig_B_mode_density_overlay.png",dpi=170);plt.close()
print("figures written")

# tables
cmp_.to_csv("table_full_41_peaks.csv",index=False)
rows=[]
for _,rw in cmp_.iterrows():
    e=rw['exp']; near=W[np.abs(W.freq_scaled-e)<=10]
    rows.append(dict(exp_cm1=e,n_modes_within_10=len(near),
        best_calc=round(near.iloc[(near.freq_scaled-e).abs().argmin()].freq_scaled,1) if len(near) else None,
        delta=round(near.iloc[(near.freq_scaled-e).abs().argmin()].freq_scaled-e,1) if len(near) else None,
        unambiguous=(len(near)==1),confidence=rw['q'],rel_int=rw['rel_int']))
pd.DataFrame(rows).to_csv("table_unambiguity_audit.csv",index=False)
print("tables written")
