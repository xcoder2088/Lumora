import subprocess, numpy as np
SR = 44100
raw = subprocess.run(['ffmpeg','-v','error','-i','snd_raw/crickets4.mp3','-af','highpass=f=100,lowpass=f=6000:poles=2','-ac','2','-ar',str(SR),'-f','f32le','-'],capture_output=True).stdout
x = np.frombuffer(raw,dtype=np.float32).reshape(-1,2).copy()
x = x[int(3*SR): len(x)-int(3*SR)]
n = int(5*SR); t = np.linspace(0,np.pi/2,n)[:,None]
x = np.concatenate([x[n:-n], x[-n:]*np.cos(t) + x[:n]*np.sin(t)])
rms = np.sqrt(np.mean(x**2)); x = x*(10**(-33/20)/rms)
print('pic %.2f, durée %.1f s'%(np.abs(x).max(), len(x)/SR))
subprocess.run(['ffmpeg','-y','-v','error','-f','f32le','-ar',str(SR),'-ac','2','-i','-','-codec:a','libmp3lame','-b:a','64k','audio/nuit.mp3'],input=x.astype(np.float32).tobytes(),check=True)
