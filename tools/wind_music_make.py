import subprocess, numpy as np
SR=44100
def mavg(x, win):                       # moyenne glissante rapide
    c=np.cumsum(np.insert(x,0,0.0)); h=win//2
    idx=np.arange(len(x)); lo=np.clip(idx-h,0,len(x)); hi=np.clip(idx+h,0,len(x))
    return (c[hi]-c[lo])/np.maximum(hi-lo,1)
def load(src, af, ch):
    raw=subprocess.run(['ffmpeg','-v','error','-i',src,'-af',af,'-ac',str(ch),'-ar',str(SR),'-f','f32le','-'],capture_output=True).stdout
    a=np.frombuffer(raw,dtype=np.float32).copy()
    return a.reshape(-1,ch)
def compress(x, win_s, power):          # ramène les passages forts vers les passages calmes
    m=np.sqrt((x**2).mean(axis=1)); e=np.sqrt(mavg(m**2,int(win_s*SR))+1e-10)
    g=(np.median(e)/e)**power; g=mavg(g,int(0.7*SR)); return x*g[:,None]
def loop(x, trim, xf, trim_end=None):
    x=x[int(trim*SR):len(x)-int((trim if trim_end is None else trim_end)*SR)]
    n=int(xf*SR); t=np.linspace(0,np.pi/2,n)[:,None]
    return np.concatenate([x[n:-n], x[-n:]*np.cos(t)+x[:n]*np.sin(t)])
def finish(x, out, target_db, kbps, peak=0.6):
    rms=np.sqrt(np.mean(x**2)); x=x*(10**(target_db/20)/rms)
    pk=np.abs(x).max()
    if pk>peak: x*=peak/pk
    subprocess.run(['ffmpeg','-y','-v','error','-f','f32le','-ar',str(SR),'-ac','2','-i','-','-codec:a','libmp3lame','-b:a',f'{kbps}k',out],input=x.astype(np.float32).tobytes(),check=True)
    m=x.mean(axis=1); w=4*SR
    db=[20*np.log10(np.sqrt(np.mean(m[i:i+w]**2))+1e-9) for i in range(0,len(m)-w,w)]
    print(out,'durée %.1f s | pic %.2f | niveau par 4 s: min %.0f max %.0f dBFS'%(len(x)/SR,np.abs(x).max(),min(db),max(db)))
# brise : vent doux dans les arbres
w=load('papillons_raw/vent_arbres.mp3','highpass=f=120,lowpass=f=2400:poles=2',2)
w=compress(w,6.0,0.4)                  # on garde de douces ondulations, on ne ramène que les pointes
w=loop(w,2.0,6.0)
finish(w,'audio/brise.mp3',-42,64,peak=0.3)
# musique de nuit : calme, sans gros écarts de volume
m=load('papillons_raw/musique.mp3','lowpass=f=5000:poles=2',2)
m=compress(m,5.0,0.65)
m=loop(m,0.5,8.0,trim_end=27.0)        # on retire la fin (la musique s'éteint) pour que la boucle reste régulière
finish(m,'audio/musique-nuit.mp3',-34,64,peak=0.6)
