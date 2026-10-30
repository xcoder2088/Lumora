import subprocess, numpy as np
SR=44100
def process(src, out, seed):
    raw=subprocess.run(['ffmpeg','-v','error','-i',src,'-af','asetrate=16000,aresample=44100,highpass=f=90,lowpass=f=1400:poles=2,aecho=0.7:0.6:180|370:0.3|0.18','-ac','1','-ar',str(SR),'-f','f32le','-'],capture_output=True).stdout
    m=np.frombuffer(raw,dtype=np.float32).copy()
    # adoucir les écarts : les appels forts sont ramenés vers les passages calmes (compression douce, fenêtre de 3 s)
    win=int(3*SR); env=np.sqrt(np.convolve(m**2,np.ones(win)/win,mode='same')+1e-10)
    g=(np.median(env)/env)**0.5; g=np.convolve(g,np.ones(SR)/SR,mode='same'); m=m*g
    # boucle sans coupure : la fin se fond dans le début
    m=m[int(2*SR):len(m)-int(2*SR)]
    n=int(6*SR); t=np.linspace(0,np.pi/2,n)
    m=np.concatenate([m[n:-n], m[-n:]*np.cos(t)+m[:n]*np.sin(t)])
    # stéréo légère : le canal droit est retardé de 9 ms, pour une sensation d'espace
    d=int(0.009*SR); R=np.concatenate([np.zeros(d),m[:-d]])
    x=np.stack([m,R],axis=1)
    rms=np.sqrt(np.mean(x**2)); x=x*(10**(-38/20)/rms)
    pk=np.abs(x).max()
    if pk>0.6: x*=0.6/pk
    subprocess.run(['ffmpeg','-y','-v','error','-f','f32le','-ar',str(SR),'-ac','2','-i','-','-codec:a','libmp3lame','-b:a','64k',out],input=x.astype(np.float32).tobytes(),check=True)
    mm=x.mean(axis=1); w=4*SR
    db=[20*np.log10(np.sqrt(np.mean(mm[i:i+w]**2))+1e-9) for i in range(0,len(mm)-w,w)]
    print(out,'durée %.1f s | pic %.2f | niveau par 4 s : min %.0f max %.0f dBFS'%(len(x)/SR,np.abs(x).max(),min(db),max(db)))
process('whales_raw/bleue_ouest_pacifique.oga','audio/baleines1.mp3',1)
process('whales_raw/bleue_atlantique3.oga','audio/baleines2.mp3',2)
