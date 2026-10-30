"""Grillons très lointains, en séquences : quelques secondes de chant, puis un long silence.
Le calendrier des séquences est tiré avec une graine fixe et couvre exactement la durée de la boucle,
donc le raccord de la boucle est continu."""
import subprocess, numpy as np
SR = 44100
SRC = 'snd_raw/crickets4.mp3'
# éloignement : on garde l'essentiel du chant, on atténue les aigus et on ajoute un peu d'écho de plein air
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', SRC, '-af',
                      'highpass=f=300,lowpass=f=4600:poles=2,aecho=0.6:0.5:140|310:0.35|0.2',
                      '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
x = np.frombuffer(raw, dtype=np.float32).reshape(-1, 2).copy()
x = x[int(3 * SR): len(x) - int(3 * SR)]
n = int(5 * SR); t = np.linspace(0, np.pi / 2, n)[:, None]
x = np.concatenate([x[n:-n], x[-n:] * np.cos(t) + x[:n] * np.sin(t)])      # boucle sans coupure
L = len(x) / SR
# séquences : 4 à 9 s de chant, 10 à 26 s de silence, enchaînées jusqu'à couvrir toute la boucle
rng = np.random.default_rng(11)
bouts = []; pos = float(rng.uniform(2, 6))
while pos < L - 12:
    on = float(rng.uniform(4, 9)); bouts.append((pos, min(pos + on, L - 3)))
    pos += on + float(rng.uniform(10, 26))
tt = np.arange(len(x)) / SR
env = np.full(len(x), 0.0)
ramp = 1.5
for a, b in bouts:
    up = np.clip((tt - a) / ramp, 0, 1); down = np.clip((b - tt) / ramp, 0, 1)
    env = np.maximum(env, 0.5 - 0.5 * np.cos(np.pi * np.minimum(up, down)))
env = 0.015 + 0.985 * env      # jamais un silence absolu : un fond très lointain reste
# les bords de la boucle sont dans un silence, donc le raccord est continu
x = x * env[:, None]
# niveau : mesuré sur les séquences seulement, très bas
on_mask = env > 0.9
rms_on = np.sqrt(np.mean(x[on_mask] ** 2))
x = x * (10 ** (-50 / 20) / rms_on)
pk = np.abs(x).max()
if pk > 0.3: x *= 0.3 / pk
print('boucle %.1f s | %d séquences de chant | part du temps en chant : %.0f %% | pic %.3f' % (L, len(bouts), on_mask.mean() * 100, np.abs(x).max()))
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-', '-codec:a', 'libmp3lame', '-b:a', '64k', 'audio/nuit.mp3'], input=x.astype(np.float32).tobytes(), check=True)
m = x.mean(axis=1); w = 4 * SR
db = [20 * np.log10(np.sqrt(np.mean(m[i:i + w] ** 2)) + 1e-9) for i in range(0, len(m) - w, w)]
print('niveau par fenêtre de 4 s (dBFS) :', ' '.join('%.0f' % d for d in db))
