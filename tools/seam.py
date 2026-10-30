import subprocess, numpy as np
for name in ['nuit','mer','profondeurs']:
    raw = subprocess.run(['ffmpeg','-v','error','-i',f'audio/{name}.mp3','-ac','1','-ar','44100','-f','f32le','-'],capture_output=True).stdout
    x = np.frombuffer(raw,dtype=np.float32)
    y = np.concatenate([x,x]); s = len(x)
    d = np.abs(np.diff(y))
    win = d[s-2000:s+2000]
    typ = np.median(d)
    r = lambda a: np.sqrt(np.mean(a**2))
    print(name, 'durée décodée %.2f s'%(len(x)/44100),
          '| saut max au raccord %.4f vs saut typique x20 = %.4f'%(d[s-5:s+5].max(), typ*20),
          '| niveau avant/après raccord (dB): %.1f / %.1f'%(20*np.log10(r(y[s-22050:s])+1e-9), 20*np.log10(r(y[s:s+22050])+1e-9)))
