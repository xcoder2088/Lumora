import re, os
REPO = '/home/user/lumora'
SP = '/chemin/vers/le/dossier/de/travail'  # à adapter
# la version 4 est FIGÉE : on part de la sauvegarde
s = open(SP + '/../v4_final.html', encoding='utf-8').read()

def rep(old, new, count=1):
    global s
    assert s.count(old) == count, (old[:90], s.count(old))
    s = s.replace(old, new)

rep('Version 4 · révision 7', 'Version 5 · révision 1')
rep("kind: 'j', s: d.s,", "kind: 'j', k: d.k, s: d.s,")
rep('Version 5 · révision 1', 'Version 5 · révision 2')

# ================= ACCUEIL : la luciole qui écrit « Lumora » (même logo que la page d'accueil) =================
root = open(REPO + '/index.html', encoding='utf-8').read()
w_css = root[root.index('/* ---------- Accueil'):root.index('button { font: inherit')]
w_sec = root[root.index('<section id="welcome"'):root.index('</section>\n') + len('</section>\n')]
a0 = root.index("<script>\n/* L'accueil est indépendant"); w_scr = root[a0:root.index('</script>\n', a0) + len('</script>\n')]
rep('button { font: inherit; color: inherit; cursor: pointer; }', w_css + 'button { font: inherit; color: inherit; cursor: pointer; }')
rep('<body>\n<canvas id="scene" aria-hidden="true"></canvas>', '<body>\n' + w_sec + '<canvas id="scene" aria-hidden="true"></canvas>')
rep('<div id="bar"></div>\n\n<script>\n', '<div id="bar"></div>\n\n' + w_scr + '\n<script>\n')
rep('function frame(now) {\n  requestAnimationFrame(frame);\n', "function frame(now) {\n  requestAnimationFrame(frame);\n  if (document.body.classList.contains('welcome-active')) { last = now; return; }   // le minuteur attend la fin de l'accueil\n")

# ================= GRANDS ÉCRANS (tableau blanc interactif) : interface agrandie, dessin allégé =================
rep("  const d = Math.min(window.devicePixelRatio || 1, 2);\n  W = window.innerWidth; H = window.innerHeight;",
    """  W = window.innerWidth; H = window.innerHeight;
  let d = Math.min(window.devicePixelRatio || 1, 2);
  if (W * H * d * d > 4.2e6) d = Math.max(0.5, Math.sqrt(4.2e6 / (W * H)));   // très grand écran : le dessin est limité à environ 4 millions de points
  document.documentElement.style.setProperty('--ui', Math.max(1, Math.min(2.6, Math.min(W, H) / 760)).toFixed(3));   // boutons et textes agrandis sur un grand écran""")
rep("</style>\n</head>", "#setup, #hud, #end, #welcomeSkip { zoom: var(--ui, 1); }\n.welcome-mark { width: min(82vw, calc(680px * var(--ui, 1))); }\n</style>\n</head>")

# ================= MÉDUSES : arrivées et traversées dans toutes les directions =================
helpers = '''// distance à parcourir depuis (px, py), dans la direction (dx, dy), pour être entièrement hors de l'écran (marges mx, my)
function distToOutside(px, py, dx, dy, mx, my) {
  let s = 0;
  while (s < 5000 && px + dx * s > -mx && px + dx * s < W + mx && py + dy * s > -my && py + dy * s < H + my) s += 8;
  return s;
}
// nouvelle traversée d'une méduse : le type de traversée est tiré au hasard (verticale, oblique vers le haut, horizontale, oblique en descendant doucement),
// puis l'entrée se fait par le bord d'où elle vient : la gauche, la droite ou le bas, jamais le haut.
let JELLY_BAG = [];
function newJellyPass(c, R, first) {
  const mx = R * 2.6, my = R * 3.4;
  // le type de traversée sort d'un « sac » mélangé (3 verticales, 3 obliques, 3 horizontales, 1 descendante sur 10) : le mélange reste équilibré
  if (!JELLY_BAG.length) JELLY_BAG = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3].sort(() => Math.random() - 0.5);
  const type = JELLY_BAG.pop();
  let dx = 0, dy = -1, E = [W / 2, H + my];
  for (let k = 0; k < 14; k++) {
    const sg = Math.random() < 0.5 ? -1 : 1;
    const deg = type === 0 ? lerp(-12, 12, Math.random()) : type === 1 ? sg * lerp(25, 65, Math.random()) : type === 2 ? sg * lerp(75, 105, Math.random()) : sg * lerp(110, 130, Math.random());
    const ang = deg / 57.3;
    dx = Math.sin(ang); dy = -Math.cos(ang);
    if (type === 3) { E = [dx > 0 ? -mx : W + mx, lerp(0.06, 0.45, Math.random()) * H]; break; }   // en descendant : elle vient d'un côté, dans la partie haute
    const Mx = lerp(0.1, 0.9, Math.random()) * W, My = lerp(0.1, 0.9, Math.random()) * H;        // un point de l'écran par où elle passera
    const s = distToOutside(Mx, My, -dx, -dy, mx, my);                                          // on remonte sa route jusqu'au bord : c'est son entrée
    E = [Mx - dx * s, My - dy * s];
    if (E[1] > -my * 0.9) break;                                                                // pas d'entrée par le haut
  }
  c.dx = dx; c.dy = dy; c.ang = Math.atan2(dx, -dy);
  c.spd = Math.max(minWH() * 0.026, 9) * lerp(0.85, 1.2, Math.random());
  c.x = c.ex = E[0]; c.y = c.ey = E[1];
  c.vx = c.dx * c.spd * 0.5; c.vy = c.dy * c.spd * 0.5;
  c.seen = false; c.passT = 0;
  c.tilt = c.tiltT = c.ang; c.tw = 0;   // elle entre déjà la tête dans le sens du mouvement
  for (const t of c.tents) t.init = false;
}
'''
rep("function updateJelly(c, dt, el) {", helpers + "function updateJelly(c, dt, el) {")

rep("let tx, ty, gvx = 0, exitQ = 0, stx = 0, sty = 0, freeFlight = false, vUp = 0;",
    "let tx, ty, gvx = 0, exitQ = 0, stx = 0, sty = 0, freeFlight = false, vUp = 0, thrAng = 0;")

i = s.index("  } else if (JELLY_MODE === 'loop') {")
j = s.index("  } else if (!JELLY_AQUARIUM) {")
new_loop = '''  } else if (JELLY_MODE === 'loop') {
    // elle nage librement et traverse l'écran dans une direction au hasard (par le bas, par un côté, en diagonale), sort d'un côté puis revient d'un autre.
    // Seul son dernier passage est guidé, pour qu'elle sorte exactement à son instant c.e.
    const Tw = Math.min(55, Math.max(5, c.e * 0.9)), tw = c.e - Tw;
    if (c.x === null) newJellyPass(c, R, true);
    if (el >= tw) {   // dernier passage : de là où elle est jusqu'au bord de l'écran, dans sa direction
      if (c.yw === undefined) {
        c.xw = c.x; c.yw = c.y;
        const sx = distToOutside(c.x, c.y, c.dx, c.dy, R * 2.8, R * 3.6);
        c.xe = c.x + c.dx * sx; c.ye = c.y + c.dy * sx;
      }
      u = clamp((el - tw) / Tw, 0, 1);
      tx = lerp(c.xw, c.xe, u); ty = lerp(c.yw, c.ye, u);
      const u2 = Math.min(1, u + 0.12);
      stx = lerp(c.xw, c.xe, u2); sty = lerp(c.yw, c.ye, u2);
      thrAng = Math.atan2(stx - c.x, c.y - sty);
    } else {   // vol libre
      c.arr = 1 - smooth(clamp((el - c.tin) / 22, 0, 1));   // à l'arrivée, elle va plus vite pour que l'écran se remplisse en une trentaine de secondes
      freeFlight = true;
      c.vtx = c.dx * c.spd * (1 + 1.5 * c.arr); c.vty = c.dy * c.spd * (1 + 1.5 * c.arr);
      u = 0; tx = c.x + c.dx * 300; ty = c.y + c.dy * 300; stx = tx; sty = ty; thrAng = c.ang;
      if (c.x > -R && c.x < W + R && c.y > -R && c.y < H + R) c.seen = true;
      c.passT += dt;
      const outside = c.x < -R * 2.6 || c.x > W + R * 2.6 || c.y < -R * 3.4 || c.y > H + R * 2.6;
      if (el >= c.tin && ((c.seen && outside) || c.passT > 240)) newJellyPass(c, R);   // elle est sortie : nouvelle traversée, par un autre bord
    }
'''
s = s[:i] + new_loop + s[j:]

rep("    if (avm > 0.02) { tx += avx * R * 3; stx += avx * R * 5; if (JELLY_AQUARIUM) ty += avy * R * 2; }",
    "    if (avm > 0.02) { tx += avx * R * 3; stx += avx * R * 5; if (JELLY_AQUARIUM) ty += avy * R * 2; if (freeFlight) { c.vx += avx * minWH() * 0.06 * dt; c.vy += avy * minWH() * 0.03 * dt; } }")
rep("      : JELLY_AQUARIUM ? clamp(0.4 + far, 0.4, 2.2) * (ty - c.y > minWH() * 0.08 ? 0.3 : 1)\n      : clamp(1 + (c.y - ty) / (minWH() * 0.35), 0.2, 2.2);",
    "      : JELLY_AQUARIUM ? clamp(0.4 + far, 0.4, 2.2) * (ty - c.y > minWH() * 0.08 ? 0.3 : 1)\n      : JELLY_MODE === 'loop' ? clamp(1 + ((tx - c.x) * c.dx + (ty - c.y) * c.dy) / (minWH() * 0.35), 0.2, 2.2)\n      : clamp(1 + (c.y - ty) / (minWH() * 0.35), 0.2, 2.2);")
rep("const thr = c.giant ? c.side * 1.3 : c.tilt;", "const thr = c.giant ? c.side * 1.3 : JELLY_MODE === 'loop' ? thrAng : c.tilt;   // en traversée, la poussée suit la direction du trajet, même presque horizontale")
rep("const kx = lerp((c.giant ? 0.12 : JELLY_AQUARIUM ? 0.1 : 0.05) * (0.5 + 0.5 * loose), ", "const kx = lerp((c.giant ? 0.12 : JELLY_AQUARIUM ? 0.1 : 0.05) * (0.5 + 0.5 * loose) * (freeFlight ? 0 : 1), ")
rep("const kperp = c.giant ? 0 : 2.6, drag", "const kperp = c.giant || JELLY_MODE === 'loop' ? 0 : 2.6, drag")
rep("(c.giant ? (gvx - c.vx) * 0.35 : 0)) * dt;", "(c.giant ? (gvx - c.vx) * 0.35 : 0) + (freeFlight ? (c.vtx - c.vx) * 0.5 : 0)) * dt;")
rep("(freeFlight ? (-vUp - c.vy) * 0.5 : 0)) * dt;", "(freeFlight ? (c.vty - c.vy) * 0.5 : 0)) * dt;")
rep("  if (el < c.tin) { c.vx = 0; c.vy = 0; c.y = H + R * 2.2; }   // pas encore arrivée : elle attend sous l'écran",
    "  if (el < c.tin && c.ex !== undefined) { c.vx = 0; c.vy = 0; c.x = c.ex; c.y = c.ey; }   // pas encore arrivée : elle attend hors de l'écran, à son point d'entrée")
# l'inclinaison dessinée suit la direction (limitée) : plus de rotation brutale
rep("clamp(Math.atan2(stx - c.x, c.y - sty), -0.6, 0.6) + (Math.random() - 0.5) * 0.3; }", "(JELLY_MODE === 'loop' ? clamp(thrAng, -2.2, 2.2) : clamp(Math.atan2(stx - c.x, c.y - sty), -0.6, 0.6)) + (Math.random() - 0.5) * 0.1; }")

rep("if (freeFlight) { c.vx += avx * minWH() * 0.06 * dt; c.vy += avy * minWH() * 0.03 * dt; } }", "}")
rep("if (avm > 0.25) c.tiltT = clamp(Math.atan2(stx - c.x, c.y - sty), -0.6, 0.6);", "if (avm > 0.25 && JELLY_MODE !== 'loop') c.tiltT = clamp(Math.atan2(stx - c.x, c.y - sty), -0.6, 0.6);")
rep("c.tilt += (c.tiltT * (1 - guide) + ", "c.tilt += (c.tiltT * (JELLY_MODE === 'loop' ? 1 : 1 - guide) + ")   # en traversée, la tête pointe toujours dans le sens du mouvement
rep("* Math.min(1, dt * (avm > 0.25 ? 1.0 : 0.6));", "* Math.min(1, dt * (JELLY_MODE === 'loop' ? 0 : avm > 0.25 ? 1.0 : 0.6));")
rep("  if (c.alpha0 === undefined) c.alpha0 = c.alpha;\n  c.X = c.x; c.Y = c.y;", """  if (c.alpha0 === undefined) c.alpha0 = c.alpha;
  if (JELLY_MODE === 'loop' && !c.giant) {   // la tête pointe dans le sens du trajet, avec une rotation douce (ressort amorti, vitesse de rotation limitée)
    let dh = thrAng + Math.sin(c.pp * TAU) * 0.05 + Math.sin(T * 0.6 + c.ph) * 0.04 - c.tilt;
    dh = Math.atan2(Math.sin(dh), Math.cos(dh));
    c.tw = clamp((c.tw || 0) + (dh * 3.0 - 2.4 * (c.tw || 0)) * dt, -0.7, 0.7);
    c.tilt += c.tw * dt;
  }
  c.X = c.x; c.Y = c.y;""")
rep("(Math.sin(c.pp * TAU) * 0.1 + Math.sin(T * 0.6 + c.ph) * 0.07) - c.tilt)", "(Math.sin(c.pp * TAU) * 0.05 + Math.sin(T * 0.6 + c.ph) * 0.04) - c.tilt)")
rep("      const dx = c.x - o.x, dy = c.y - o.y, d = Math.hypot(dx, dy) || 1, mn = (R + o.R) * 1.25;\n      if (d < mn) { const f = (mn - d) * 2.2 * dt;", "      const dx = c.x - o.x, dy = c.y - o.y, d = Math.hypot(dx, dy) || 1, mn = (R + o.R) * 0.95;\n      if (d < mn) { const f = (mn - d) * 2.2 * dt;")
yield_block = """  // priorités : une méduse laisse passer celles qui ont la priorité au lieu de les bousculer. Elle ralentit jusqu'à ce que le chemin soit libre, puis reprend sa route.
  // (une méduse en dernier passage passe toujours en premier ; sinon la priorité va à la plus ancienne : aucun blocage possible)
  if (c.yieldF === undefined) c.yieldF = 1;
  if (!c.giant) {
    let wantYield = false;
    if (freeFlight) {
      const prio = q => q.yw !== undefined ? -1 : q.k;
      const vcx = c.dx * c.spd, vcy = c.dy * c.spd;
      for (const o of live) {
        if (o === c || o.kind !== 'j' || o.x === null || o.giant || o.alpha < 0.15 || !(prio(o) < prio(c))) continue;
        const dx = o.x - c.x, dy = o.y - c.y, wx = o.vx - vcx, wy = o.vy - vcy, ww = wx * wx + wy * wy;
        const ts = ww > 1e-6 ? clamp(-(dx * wx + dy * wy) / ww, 0, 5) : 0;
        const lim = (R + o.R) * 1.15;
        if (Math.hypot(dx + wx * ts, dy + wy * ts) < lim && (ts > 0 || Math.hypot(dx, dy) < lim)) { wantYield = true; break; }
      }
    }
    // si elle attend depuis trop longtemps, elle repart un moment quand même (jamais de longue attente)
    if (c.noYield > 0) { c.noYield -= dt; wantYield = false; }
    else if (wantYield) { c.waitT = (c.waitT || 0) + dt; if (c.waitT > 7) { c.noYield = 6; c.waitT = 0; wantYield = false; } }
    else c.waitT = Math.max(0, (c.waitT || 0) - dt * 2);
    c.yieldF += ((wantYield ? 0.05 : 1) - c.yieldF) * Math.min(1, dt * (wantYield ? 2.0 : 1.2));
  }
"""
rep("  // Allure : de temps en temps la méduse change de comportement", yield_block + "  // Allure : de temps en temps la méduse change de comportement")
rep("      : freeFlight ? 1 + 1.3 * (c.arr || 0)\n", "      : freeFlight ? (1 + 1.3 * (c.arr || 0)) * Math.max(0.2, c.yieldF)\n")
rep("(freeFlight ? (c.vtx - c.vx) * 0.5 : 0)) * dt;", "(freeFlight ? (c.vtx * c.yieldF - c.vx) * 0.5 : 0)) * dt;")
rep("(freeFlight ? (c.vty - c.vy) * 0.5 : 0)) * dt;", "(freeFlight ? (c.vty * c.yieldF - c.vy) * 0.5 : 0)) * dt;")

# ================= PAPILLONS : arrivées et traversées dans toutes les directions =================
# calendrier : le premier passage de chaque papillon commence exactement à son instant d'arrivée, le dernier se termine à son instant de sortie
rep("for (let k = 0; k < N; k++) sched.push({ k, seed: runSeed + k, e: D - k * P, T: lerp(34, 52, r()), s: -60, n: N, loop: true, x0: 0.5, x1: 0.5 });",
    """for (let k = 0; k < N; k++) {
      const e = D - k * P, tin = arrivalTime({ k, n: N, e }), m = Math.max(1, Math.round((e - tin) / lerp(34, 52, r())));
      sched.push({ k, seed: runSeed + k, e, T: (e - tin) / m, s: -60, n: N, loop: true, x0: 0.5, x1: 0.5 });   // T : durée d'un passage, choisie pour qu'un passage commence pile à l'arrivée
    }""")
rep("const q = (el - c.e) / c.T, n = Math.floor(q);", "const q = (el - c.e) / c.T + 1e-6, n = Math.floor(q);")
rep("""      const rt = h(1);
      c.far = rt < 0.25; c.rise = rt >= 0.25 && rt < 0.4;
      c.side = h(2) < 0.5 ? -1 : 1; c.ya = lerp(0.22, 0.8, h(3)); c.yb = lerp(-0.2, 0.2, h(4)); c.farY = lerp(0.5, 0.62, h(5));
      c.x0 = h(6) * 1.1 - 0.05; c.x1 = clamp(c.x0 + (h(7) - 0.5) * 0.3, -0.08, 1.08);""",
"""      // chaque passage : entrée par un bord au hasard (gauche, droite, bas ou haut), sortie par un autre, donc de côté, en diagonale, vers le haut ou vers le bas
      const rt = h(1), mgp = Math.max(0.08 * W, Sz * 2.2);
      c.far = rt < 0.15; c.rise = false;
      const edge = w => w < 0.35 ? 0 : w < 0.7 ? 1 : 2;   // entrée : 0 gauche, 1 droite, 2 bas (jamais par le haut) ; la sortie peut se faire par n'importe quel bord
      const e1 = edge(h(2)), e2 = (e1 + 1 + Math.floor(h(4) * 3)) % 4;   // sortie par n'importe quel autre bord
      const pt = (e, f) => e === 0 ? [-mgp, lerp(0.12, 0.85, f) * H] : e === 1 ? [W + mgp, lerp(0.12, 0.85, f) * H] : e === 2 ? [lerp(0.08, 0.92, f) * W, H + mgp] : [lerp(0.08, 0.92, f) * W, -mgp];
      c.P1 = pt(e1, h(5)); c.P2 = pt(e2, h(6));
      c.farY = lerp(0.5, 0.62, h(8)); c.x0 = h(6) * 1.1 - 0.05; c.x1 = clamp(c.x0 + (h(7) - 0.5) * 0.3, -0.08, 1.08);""")
rep("  const cross = !c.far && !c.rise;\n", "  const cross = !c.far;   // trajet en ligne : entre un bord et un autre\n  const tp = smooth(u / 0.12);\n")
rep("""  const X = cross ? lerp(c.side < 0 ? W + mg : -mg, c.side < 0 ? -mg : W + mg, ue) + wx * W * 0.3
    : (lerp(c.x0, c.far ? lerp(c.x1, 0.5, 0.45) : c.x1, u) + wx * (c.far ? lerp(1, 0.3, u) : 1)) * W;
  const Y = cross ? (lerp(c.ya, clamp(c.ya + c.yb, 0.12, 0.85), u) + wy * 2.2) * H
    : c.far ? lerp(H + Sz * 2.6, c.farY * H, Math.pow(u, 0.75)) + wy * H * lerp(1, 0.25, u) : lerp(H + Sz * 2.6, -Sz * 2.8, u) + wy * H * smooth(u / 0.12);""",
"""  const X = cross ? lerp(c.P1[0], c.P2[0], ue) + wx * W * 0.3 * tp
    : (lerp(c.x0, lerp(c.x1, 0.5, 0.45), u) + wx * lerp(1, 0.3, u)) * W;
  const Y = cross ? lerp(c.P1[1], c.P2[1], ue) + wy * H * 1.2 * tp
    : lerp(H + Sz * 2.6, c.farY * H, Math.pow(u, 0.75)) + wy * H * lerp(1, 0.25, u);""")
# plus d'arrivée depuis la prairie : l'arrivée est le début du premier passage
i = s.index("  // arrivée : au début, le papillon s'envole de la prairie"); j = s.index("  // atterrissage : certains papillons se posent")
s = s[:i] + s[j:]
rep("const px = (!c.far && !c.rise) ? lerp(c.side < 0 ? W + mg : -mg, c.side < 0 ? -mg : W + mg, u0) : lerp(c.x0, c.x1, u0) * W;",
    "const px = c.P1 ? lerp(c.P1[0], c.P2[0], u0) : lerp(c.x0, c.x1, u0) * W;")
rep("!c.far && c.T > 30 && Math.random() < 0.55", "!c.far && c.T > 24 && Math.random() < 0.55")

# ================= sorties =================
out_dir = REPO + '/versions/v5-traversees'
os.makedirs(out_dir, exist_ok=True)
open(out_dir + '/index.html', 'w', encoding='utf-8').write(s)
art = s.replace('../../assets/', 'assets/').replace('../../audio/', 'audio/')
art = art.replace('<!doctype html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n', '')
art = art.replace('</head>\n<body>\n', '').replace('\n</body>\n</html>\n', '\n')
art = art.replace('<title>Lumora</title>', '<title>Lumora Version 5</title>')
os.makedirs(SP + '/stage5', exist_ok=True)
open(SP + '/stage5/index.html', 'w', encoding='utf-8').write(art)
print('v5 écrit :', len(s), 'octets')
