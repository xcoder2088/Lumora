import subprocess, numpy as np
def load(p, sr):
    raw = subprocess.run(['ffmpeg','-v','error','-i',p,'-ac','2','-ar',str(sr),'-f','f32le','-'],capture_output=True).stdout
    return np.frombuffer(raw,dtype=np.float32).reshape(-1,2).copy()
def loop(x, sr, trim, xf):
    """Rend x bouclable : rogne les bords puis fond la fin dans le début (fondu enchaîné à puissance égale)."""
    x = x[int(trim[0]*sr): len(x)-int(trim[1]*sr)]
    n = int(xf*sr)
    t = np.linspace(0, np.pi/2, n)[:,None]
    head, tail = x[:n], x[-n:]
    seam = tail*np.cos(t) + head*np.sin(t)       # la fin s'efface pendant que le début arrive
    return np.concatenate([x[n:-n], seam])
def level(x, target_db):
    rms = np.sqrt(np.mean(x**2)); g = 10**(target_db/20)/rms
    y = x*g
    pk = np.abs(y).max()
    if pk > 0.85: y *= 0.85/pk
    return y
def save(x, sr, name, kbps):
    raw = x.astype(np.float32).tobytes()
    subprocess.run(['ffmpeg','-y','-v','error','-f','f32le','-ar',str(sr),'-ac','2','-i','-','-codec:a','libmp3lame','-b:a',f'{kbps}k',f'audio/{name}.mp3'],input=raw,check=True)
jobs = [('crickets4','nuit',44100,(3,3),5,-23,64),
        ('waves','mer',44100,(1.5,1.5),4,-23,80),
        ('aquaria','profondeurs',44100,(0.05,0.0),0.6,-23,80)]
for src,name,sr,trim,xf,db,kb in jobs:
    x = load(f'snd_raw/{src}.mp3', sr)
    y = level(loop(x, sr, trim, xf), db)
    save(y, sr, name, kb)
    print(name, 'durée %.1f s'%(len(y)/sr), 'pic %.2f'%np.abs(y).max())
