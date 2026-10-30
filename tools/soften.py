import subprocess, numpy as np
SR = 44100
def load(p, af):
    raw = subprocess.run(['ffmpeg','-v','error','-i',p,'-af',af,'-ac','2','-ar',str(SR),'-f','f32le','-'],capture_output=True).stdout
    return np.frombuffer(raw,dtype=np.float32).reshape(-1,2).copy()
def stats(x, label):
    m = x.mean(axis=1); n = SR
    w = len(m)//n
    db = np.array([20*np.log10(np.sqrt(np.mean(m[i*n:(i+1)*n]**2))+1e-9) for i in range(w)])
    sp = np.abs(np.fft.rfft(m[:SR*60]))**2; f = np.fft.rfftfreq(len(m[:SR*60]),1/SR)
    cen = (f*sp).sum()/sp.sum()
    print(f'{label}: niveau moyen {db.mean():.1f} dBFS, écart 5%-95% {np.percentile(db,95)-np.percentile(db,5):.1f} dB, pic {np.abs(x).max():.2f}, centre spectral {cen:.0f} Hz')

orig = load('snd_raw/waves.mp3', 'anull')
stats(orig, 'avant (source)')

# 1) retirer le sifflement d'écume et les basses parasites
x = load('snd_raw/waves.mp3', 'highpass=f=70,lowpass=f=2200:poles=2,treble=g=-5:f=1200')

# 2) lisser les houles : la fin de chaque vague ne doit plus dominer (compression douce de l'enveloppe lente)
m = np.sqrt((x**2).mean(axis=1))
win = int(1.5*SR)
k = np.ones(win)/win
env = np.sqrt(np.convolve(m**2, k, mode='same') + 1e-10)
ref = np.median(env)
gain = (ref/env)**0.7
gain = np.convolve(gain, np.ones(int(0.5*SR))/int(0.5*SR), mode='same')
x = x*gain[:,None]

# 3) boucle sans coupure
def loop(x, trim, xf):
    x = x[int(trim[0]*SR): len(x)-int(trim[1]*SR)]
    n = int(xf*SR); t = np.linspace(0,np.pi/2,n)[:,None]
    seam = x[-n:]*np.cos(t) + x[:n]*np.sin(t)
    return np.concatenate([x[n:-n], seam])
x = loop(x, (1.5,1.5), 4)

# 4) plus doux : niveau -28 dBFS
rms = np.sqrt(np.mean(x**2)); x = x*(10**(-28/20)/rms)
if np.abs(x).max() > 0.85: x *= 0.85/np.abs(x).max()
stats(x, 'après (adouci)')
subprocess.run(['ffmpeg','-y','-v','error','-f','f32le','-ar',str(SR),'-ac','2','-i','-','-codec:a','libmp3lame','-b:a','80k','audio/mer.mp3'],input=x.astype(np.float32).tobytes(),check=True)
print('durée %.1f s'%(len(x)/SR))
