import subprocess, numpy as np
SR=44100
OLD='snd_raw/crickets4.mp3'
raw=subprocess.run(['ffmpeg','-v','error','-i',OLD,'-af','highpass=f=250,lowpass=f=5200:poles=2','-ac','2','-ar',str(SR),'-f','f32le','-'],capture_output=True).stdout
x=np.frombuffer(raw,dtype=np.float32).reshape(-1,2).copy()
x=x[int(3*SR):len(x)-int(3*SR)]
n=int(5*SR); t=np.linspace(0,np.pi/2,n)[:,None]
x=np.concatenate([x[n:-n], x[-n:]*np.cos(t)+x[:n]*np.sin(t)])      # boucle sans coupure
L=len(x)/SR
# enveloppe « chœur de grillons » : des vagues lentes avec de vrais silences, périodique sur la boucle (raccord continu)
tt=np.arange(len(x))/SR
rng=np.random.default_rng(7)
comp=[(8,.45),(14,.30),(23,.15),(37,.10)]
nn=sum(a*np.sin(2*np.pi*k*tt/L+rng.uniform(0,2*np.pi)) for k,a in comp)   # entre -1 et 1
nn=0.5+0.5*nn
env=np.clip((nn-0.32)/0.43,0,1)**1.3
env=0.02+0.98*env                                                   # jamais un silence absolu : un fond très lointain reste
x=x*env[:,None]
# niveau : très lointain
rms=np.sqrt(np.mean(x**2)); x=x*(10**(-44/20)/rms)
pk=np.abs(x).max()
if pk>0.5: x*=0.5/pk
print('durée %.1f s | moyenne -44 dBFS | pic %.3f | part du temps presque silencieux (env<0.1): %.0f %%'%(L,np.abs(x).max(),(env<0.1).mean()*100))
subprocess.run(['ffmpeg','-y','-v','error','-f','f32le','-ar',str(SR),'-ac','2','-i','-','-codec:a','libmp3lame','-b:a','64k','audio/nuit.mp3'],input=x.astype(np.float32).tobytes(),check=True)
# contrôle : niveau par fenêtre de 4 s
m=x.mean(axis=1); w=4*SR
db=[20*np.log10(np.sqrt(np.mean(m[i:i+w]**2))+1e-9) for i in range(0,len(m)-w,w)]
print('niveau par fenêtres de 4 s (dBFS), min %.0f max %.0f'%(min(db),max(db)))
