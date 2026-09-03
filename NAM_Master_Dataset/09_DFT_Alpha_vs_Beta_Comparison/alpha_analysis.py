import re, csv, numpy as np

LOG="/sessions/dazzling-modest-faraday/mnt/uploads/nam-alpha.LOG"
ARCH="/sessions/dazzling-modest-faraday/mnt/mtp/NAM_Raman_Archive/"

# ---------- parse frequencies, raman activities, displacement vectors ----------
def parse(log):
    t=open(log,errors="ignore").read()
    freqs=[float(x) for l in re.findall(r"Frequencies --(.*)",t) for x in l.split()]
    raman=[float(x) for l in re.findall(r"Raman Activ --(.*)",t) for x in l.split()]
    # displacement vectors: blocks after "Atom  AN      X      Y      Z ..."
    disp=[[] for _ in freqs]
    blocks=re.split(r"Frequencies --",t)[1:]
    k=0
    for b in blocks:
        lines=b.splitlines()
        # find the coordinate rows
        rows=[]
        started=False
        for l in lines:
            if re.match(r"\s+Atom\s+AN\s+X",l): started=True; continue
            if started:
                m=re.match(r"\s*\d+\s+\d+((?:\s+-?\d+\.\d+){3,9})\s*$",l)
                if m: rows.append([float(x) for x in m.group(1).split()])
                else: break
        ncol=len(rows[0])//3 if rows else 0
        for c in range(ncol):
            if k+c < len(freqs):
                disp[k+c]=np.array([[r[3*c],r[3*c+1],r[3*c+2]] for r in rows])
        k+=ncol
    return np.array(freqs), np.array(raman), disp

fa, ra, da = parse(LOG)
fb, rb, db = parse(ARCH+"02_DFT_Calculation/NAM_beta_Gaussian16_B3LYP-D3BJ_6-311++Gdp.log")
print(f"alpha: {len(fa)} modes, {len(ra)} raman, disp shape {da[0].shape}")
print(f"beta : {len(fb)} modes, {len(rb)} raman, disp shape {db[0].shape}")

# ---------- scaling + Placzek intensity ----------
def scale(f): return np.where(f<1800, f*0.980, f*0.967)
LAM=785.0; NU0=1e7/LAM
def placzek(f,S,T=298.15):
    f=np.maximum(f,1e-6)
    B=1-np.exp(-1.4388*f/T)
    return S*(NU0-f)**4/(f*B)

fas, fbs = scale(fa), scale(fb)
Ia = placzek(fa,ra); Ia = Ia/Ia.max()*100
Ib = placzek(fb,rb); Ib = Ib/Ib.max()*100

# ---------- ring / atom decomposition ----------
MASS={"H":1.008,"C":12.011,"N":14.007,"O":15.999}
def geom(log):
    t=open(log,errors="ignore").read().replace("\r","")
    parts=t.split("Standard orientation:")
    if len(parts)<2: parts=t.split("Input orientation:")
    Z={1:"H",6:"C",7:"N",8:"O"}
    els=[];xyz=[]
    for l in parts[-1].splitlines()[1:]:
        r=l.split()
        if len(r)==6 and r[0].isdigit() and r[1].isdigit():
            els.append(Z[int(r[1])]); xyz.append([float(r[3]),float(r[4]),float(r[5])])
        elif els and set(l.strip())<=set("- "):
            if len(els)>0: break
    return els,np.array(xyz)
ea,xa=geom(LOG); eb2,xb2=geom(ARCH+"02_DFT_Calculation/NAM_beta_Gaussian16_B3LYP-D3BJ_6-311++Gdp.log")
print("alpha geom:",len(ea),"atoms   beta geom:",len(eb2),"atoms")

RING_A=[0,9,10,11,12,13]   # verified identical indexing earlier
def frac(d,idx,els):
    w=np.array([MASS[e] for e in els])
    m=(d**2).sum(1)*w
    return m[idx].sum()/m.sum(), m/m.sum()

# ---------- experimental peaks ----------
comp=list(csv.DictReader(open(ARCH+"03_Processed_Results/Experimental_vs_DFT_comparison.csv")))
exp=[(float(r["exp"]), r["calc"], r["rel_int"], r["q"]) for r in comp]
unmatched=[e[0] for e in exp if e[1].strip()==""]
print(f"\nexperimental bands: {len(exp)}   unmatched by beta: {len(unmatched)}")
print("unmatched:", unmatched)

# ---------- match unmatched bands against alpha ----------
TOL=18.0
print(f"\n{'='*84}")
print(f"UNMATCHED-BY-BETA BANDS TESTED AGAINST ALPHA  (tolerance +/-{TOL:.0f} cm-1)")
print(f"{'='*84}")
print(f"{'exp':>7} {'best alpha':>11} {'delta':>7} {'ramanAct':>9} {'rel_int%':>9}  {'nearest beta':>12} {'dbeta':>7}")
hits=[]
for e in unmatched:
    da_=np.abs(fas-e); ia=da_.argmin()
    db_=np.abs(fbs-e); ib=db_.argmin()
    ok = da_[ia]<=TOL
    flag=""
    if ok and db_[ib]>TOL: flag="  <== ALPHA ONLY"
    elif ok: flag="  (both near)"
    print(f"{e:7.1f} {fas[ia]:11.1f} {fas[ia]-e:+7.1f} {ra[ia]:9.2f} {Ia[ia]:9.2f}  {fbs[ib]:12.1f} {fbs[ib]-e:+7.1f}{flag}")
    if ok: hits.append((e,ia,fas[ia],ra[ia],Ia[ia],db_[ib]))

# ---------- decompose the hits ----------
print(f"\n{'='*84}\nDISPLACEMENT DECOMPOSITION OF ALPHA HITS\n{'='*84}")
for e,ia,fs,rr,ii,dbeta in hits:
    rf,per=frac(da[ia],RING_A,ea)
    top=np.argsort(per)[::-1][:4]
    print(f"\n exp {e:.0f} cm-1  <-  alpha mode {ia+1} at {fs:.1f} (raw {fa[ia]:.1f}), RamanAct {rr:.2f}, relI {ii:.1f}%")
    print(f"   ring fraction: {rf*100:.1f}%")
    print(f"   top atoms: " + ", ".join(f"{ea[j]}{j}({per[j]*100:.1f}%)" for j in top))

# ---------- tolerance sensitivity (guard against survivorship bias) ----------
print(f"\n{'='*84}\nTOLERANCE SENSITIVITY - how many unmatched bands does alpha 'explain'?\n{'='*84}")
print(f"{'tol':>5} {'alpha matches':>14} {'beta matches':>13} {'alpha-only':>11}")
for tol in [5,8,10,12,15,18,20,25]:
    na=sum(1 for e in unmatched if np.abs(fas-e).min()<=tol)
    nb=sum(1 for e in unmatched if np.abs(fbs-e).min()<=tol)
    ao=sum(1 for e in unmatched if np.abs(fas-e).min()<=tol and np.abs(fbs-e).min()>tol)
    print(f"{tol:5d} {na:14d} {nb:13d} {ao:11d}")

# ---------- null test: random frequencies ----------
print(f"\n{'='*84}\nNULL TEST - would ANY 111-mode set match this well by chance?\n{'='*84}")
rng=np.random.default_rng(0)
lo,hi=fas.min(),fas.max()
cnt=[]
for _ in range(2000):
    fake=rng.uniform(400,1800,111)
    cnt.append(sum(1 for e in unmatched if np.abs(fake-e).min()<=TOL))
cnt=np.array(cnt)
real=sum(1 for e in unmatched if np.abs(fas-e).min()<=TOL)
print(f" alpha matches {real}/{len(unmatched)} unmatched bands at +/-{TOL:.0f}")
print(f" random 111-mode sets match {cnt.mean():.1f} +/- {cnt.std():.1f} (p={np.mean(cnt>=real):.3f})")

# ---------- energies ----------
print(f"\n{'='*84}\nENERGETICS (gas phase, single conformer each)\n{'='*84}")
print(f" {'quantity':<38}{'beta':>14}{'alpha':>14}{'alpha-beta':>14}")
for nm,b,a in [("Electronic SCF (Ha)",-1087.57064455,-1087.56495412),
               ("+ ZPE (Ha)",-1087.252763,-1087.246711),
               ("Gibbs free energy (Ha)",-1087.304371,-1087.299425)]:
    print(f" {nm:<38}{b:>14.6f}{a:>14.6f}{(a-b)*627.5095:>+11.2f} kcal")

np.save("/sessions/dazzling-modest-faraday/mnt/outputs/fas.npy",fas)
with open("/sessions/dazzling-modest-faraday/mnt/outputs/alpha_modes.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["mode","freq_raw","freq_scaled","raman_activity","rel_intensity","ring_frac"])
    for i in range(len(fa)):
        rf,_=frac(da[i],RING_A,ea)
        w.writerow([i+1,round(fa[i],4),round(fas[i],4),round(ra[i],4),round(Ia[i],3),round(rf,4)])
print("\nwrote alpha_modes.csv")
