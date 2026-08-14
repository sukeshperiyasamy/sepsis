import re, csv, numpy as np
LOG="/sessions/dazzling-modest-faraday/mnt/uploads/nam-alpha.LOG"
ARCH="/sessions/dazzling-modest-faraday/mnt/mtp/NAM_Raman_Archive/"

def parse(log):
    t=open(log,errors="ignore").read().replace("\r","")
    f=np.array([float(x) for l in re.findall(r"Frequencies --(.*)",t) for x in l.split()])
    r=np.array([float(x) for l in re.findall(r"Raman Activ --(.*)",t) for x in l.split()])
    return f,r
fa,ra=parse(LOG); fb,rb=parse(ARCH+"02_DFT_Calculation/NAM_beta_Gaussian16_B3LYP-D3BJ_6-311++Gdp.log")
sc=lambda f: np.where(f<1800,f*0.980,f*0.967)
fas,fbs=sc(fa),sc(fb)

NU0=1e7/785.0
def placz(f,S,T=298.15):
    f=np.maximum(f,1e-6); return S*(NU0-f)**4/(f*(1-np.exp(-1.4388*f/T)))
Ia=placz(fa,ra); Ia=Ia/Ia.max()*100
Ib=placz(fb,rb); Ib=Ib/Ib.max()*100

comp=list(csv.DictReader(open(ARCH+"03_Processed_Results/Experimental_vs_DFT_comparison.csv")))
allexp=np.array([float(r["exp"]) for r in comp])
unm=np.array([float(r["exp"]) for r in comp if r["calc"].strip()==""])

W=(400,1800)
inw=lambda f:(f>=W[0])&(f<=W[1])
na,nb=inw(fas).sum(),inw(fbs).sum()
print("="*80); print("1. MODE DENSITY — is +/-18 cm-1 even a discriminating test?"); print("="*80)
for nm,n in [("beta",nb),("alpha",na)]:
    cov=n*2*18/(W[1]-W[0])
    print(f"  {nm:6s}: {n:3d} modes in 400-1800  ->  mean spacing {(W[1]-W[0])/n:5.1f} cm-1"
          f"   coverage at +/-18 = {cov*100:5.1f}% of the axis")
print("\n  A band placed at random matches with probability ~= coverage.")
print("  Coverage near or above 100% means the test cannot discriminate.")

print("\n"+"="*80); print("2. THE SURVIVORSHIP TRAP IN MY OWN FRAMING"); print("="*80)
print(f"  The {len(unm)} 'unmatched' bands were DEFINED as those beta failed to match.")
print("  So 'beta matches 0/8, alpha matches 3/8' is guaranteed by construction,")
print("  not evidence. Beta cannot score above 0 on its own leftovers.")
print("  The honest question: does alpha improve the fit ACROSS ALL 41 BANDS")
print("  more than any arbitrary extra 111 modes would?")

def stats(exp,modes,tol=18.):
    d=np.abs(modes[None,:]-exp[:,None]).min(1)
    m=d<=tol
    return m.sum(), d[m].mean() if m.any() else np.nan
print("\n"+"="*80); print("3. ALL 41 BANDS — beta vs alpha vs combined"); print("="*80)
print(f"  {'model':<28}{'modes':>7}{'matched/41':>12}{'MAE(matched)':>14}")
for nm,mo in [("beta only",fbs),("alpha only",fas),("alpha+beta combined",np.concatenate([fas,fbs]))]:
    n,mae=stats(allexp,mo)
    print(f"  {nm:<28}{inw(mo).sum():>7}{n:>12}{mae:>14.2f}")

print("\n"+"="*80); print("4. DECOY CONTROL — does ANY extra 111-mode set help this much?"); print("="*80)
print("  Decoy = beta modes rigidly shifted by a random offset (same count,")
print("  same spacing statistics, but chemically meaningless).")
rng=np.random.default_rng(1)
base,_=stats(allexp,fbs)
real,_=stats(allexp,np.concatenate([fas,fbs]))
gains=[]
for _ in range(5000):
    sh=rng.uniform(-60,60)
    n,_=stats(allexp,np.concatenate([fbs+sh,fbs]))
    gains.append(n-base)
gains=np.array(gains)
print(f"\n  beta alone                : {base}/41")
print(f"  beta + real alpha         : {real}/41   (gain +{real-base})")
print(f"  beta + shifted-beta decoy : {base+gains.mean():.1f}/41  (gain +{gains.mean():.2f} +/- {gains.std():.2f})")
print(f"  p(decoy gain >= real gain) = {np.mean(gains>=(real-base)):.4f}")

print("\n"+"="*80); print("5. INTENSITY FILTER — are the matched alpha modes strong enough to see?"); print("="*80)
print(f"  {'exp':>7}{'alpha':>9}{'delta':>8}{'RamanAct':>10}{'relInt%':>9}   verdict")
for e in unm:
    i=np.abs(fas-e).argmin()
    if abs(fas[i]-e)<=18:
        v = "credible" if Ia[i]>=1.0 else "TOO WEAK to be observable"
        print(f"  {e:7.0f}{fas[i]:9.1f}{fas[i]-e:+8.1f}{ra[i]:10.2f}{Ia[i]:9.2f}   {v}")

print("\n"+"="*80); print("6. TIGHT-TOLERANCE TEST (+/-8 cm-1, where coverage is low)"); print("="*80)
for tol in [5,8,10]:
    cov=na*2*tol/(W[1]-W[0])
    ba,_=stats(allexp,fbs,tol); ra_,_=stats(allexp,fas,tol); ca,_=stats(allexp,np.concatenate([fas,fbs]),tol)
    g=[]
    for _ in range(3000):
        sh=rng.uniform(-60,60); n,_=stats(allexp,np.concatenate([fbs+sh,fbs]),tol); g.append(n-ba)
    g=np.array(g)
    print(f"  tol +/-{tol:2d} (coverage {cov*100:4.1f}%): beta {ba:2d}/41  alpha {ra_:2d}/41  combined {ca:2d}/41"
          f"   real gain +{ca-ba}  decoy gain +{g.mean():.2f}+/-{g.std():.2f}  p={np.mean(g>=(ca-ba)):.4f}")
