import subprocess, numpy as np, sys
def load(p, sr=22050):
    raw = subprocess.run(['ffmpeg','-v','error','-i',p,'-ac','1','-ar',str(sr),'-f','f32le','-'],capture_output=True).stdout
    return np.frombuffer(raw,dtype=np.float32), sr
for name in ['crickets4','waves','aquaria']:
    x, sr = load('snd_raw/%s.mp3'%name)
    n = sr
    w = len(x)//n
    rms = np.array([np.sqrt(np.mean(x[i*n:(i+1)*n]**2)) for i in range(w)])
    db = 20*np.log10(rms+1e-9)
    med = np.median(db)
    # bands per second
    def band(lo,hi):
        out=[]
        for i in range(w):
            seg = x[i*n:(i+1)*n]*np.hanning(n)
            sp = np.abs(np.fft.rfft(seg))**2
            f = np.fft.rfftfreq(n,1/sr)
            out.append(10*np.log10(sp[(f>=lo)&(f<hi)].sum()+1e-12))
        return np.array(out)
    b_low, b_mid, b_hi, b_ck = band(20,300), band(300,2000), band(2000,4000), band(4000,10000)
    print('==',name,'dur %.1fs'%(len(x)/sr),'median %.1f dBFS'%med,'min %.1f max %.1f'%(db.min(),db.max()),'p95-p5 spread %.1f dB'%(np.percentile(db,95)-np.percentile(db,5)))
    loud = [(i,round(db[i]-med,1)) for i in range(w) if db[i]-med>4]
    print('  seconds >4 dB above median:', loud[:20], '(total %d)'%len(loud))
    print('  mean band dB  low<300: %.0f  300-2k: %.0f  2-4k: %.0f  4-10k: %.0f'%(b_low.mean(),b_mid.mean(),b_hi.mean(),b_ck.mean()))
    peak = np.abs(x).max()
    print('  peak %.2f'%peak)
