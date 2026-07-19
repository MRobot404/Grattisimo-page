# -*- coding: utf-8 -*-
"""Mordidas aleatorias pero creíbles, para todos los sabores.

En vez de poner la mordida en un punto fijo, se detecta el CONTORNO real del
helado y se muerde desde un punto al azar de ese borde. Así cada sabor recibe
una dentada en un lugar distinto (arriba, al lado, en la esquina...) y siempre
sobre la silueta, nunca en el aire ni en el palito.

Detalle clave: los dientes se orientan HACIA EL CUERPO del helado. Si se
orientan al azar caen en el vacío y el mordisco queda como un círculo liso,
que es justo lo que se ve falso.

Cada candidata se valida: si se come de más o de menos, se reintenta.

Uso:  python gen-mordidas.py
Genera helados/<sabor>-mordido.png para cada PNG de la carpeta.
"""
import math, random, os, glob
from PIL import Image, ImageDraw, ImageFilter, ImageChops

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'helados')
COMIDO_MIN, COMIDO_MAX = 9.0, 21.0    # % del helado que debe desaparecer
ALTO_SALIDA = 500                      # las mordidas solo se ven en miniatura
VARIANTES = 4                          # mordidas distintas por sabor; el JS elige una al azar


def opacos(a):
    """Cuenta píxeles visibles (rápido: point + histogram corren en C)."""
    return a.point(lambda v: 255 if v > 40 else 0).histogram()[255]


def puntos_del_borde(alpha, x0, y0, x1, y1, alto_cuerpo):
    """Contorno del CUERPO (sin el palito ni la base donde se une)."""
    solido = alpha.point(lambda v: 255 if v > 128 else 0)
    borde = ImageChops.subtract(solido, solido.filter(ImageFilter.MinFilter(5)))
    px = borde.load()
    y_max = min(y0 + int(alto_cuerpo * 0.85), y1)   # deja fuera la unión con el palito
    y_min = y0 + int(alto_cuerpo * 0.04)
    return [(x, y) for y in range(y_min, y_max, 2)
                   for x in range(x0, x1, 2) if px[x, y] > 100]


def tallar(W, H, cx, cy, R, rnd, hacia):
    """Arco principal + marcas de dientes + mordisquitos: borde irregular.

    `hacia` = ángulo (rad) del centro de la mordida hacia el cuerpo del helado.
    """
    m = Image.new('L', (W, H), 0)
    d = ImageDraw.Draw(m)
    circ = lambda x, y, r: d.ellipse([x - r, y - r, x + r, y + r], fill=255)

    circ(cx, cy, R)
    n, abanico = 9, math.radians(210)
    for i in range(n):
        ang = hacia - abanico / 2 + (i / (n - 1)) * abanico
        f = rnd.uniform(0.90, 1.06)
        circ(cx + math.cos(ang) * R * f, cy + math.sin(ang) * R * f,
             R * rnd.uniform(0.13, 0.24))
    for _ in range(3):
        ang = hacia + math.radians(rnd.uniform(-95, 95))
        f = rnd.uniform(0.95, 1.12)
        circ(cx + math.cos(ang) * R * f, cy + math.sin(ang) * R * f,
             R * rnd.uniform(0.07, 0.12))

    m = m.filter(ImageFilter.GaussianBlur(1.6))
    m = m.point(lambda v: 255 if v > 128 else 0)      # bordes nítidos
    return m.filter(ImageFilter.GaussianBlur(0.7))    # antialias limpio


def generar(slug, intentos=40):
    """Genera VARIANTES mordidas distintas del mismo sabor.

    Cada variante se fuerza a una ZONA diferente del contorno, para que no
    salgan cuatro mordidas casi iguales: el JS elige una al azar en cada
    carga y hay que notar el cambio.
    """
    src = os.path.join(BASE, slug + '.png')
    im = Image.open(src).convert('RGBA')
    W, H = im.size
    alpha = im.split()[3]
    caja = alpha.getbbox()
    if not caja:
        return [f'{slug}: imagen vacía']
    x0, y0, x1, y1 = caja
    bw, bh = x1 - x0, y1 - y0
    alto_cuerpo = int(bh * 0.62)                      # abajo va el palito

    pts = puntos_del_borde(alpha, x0, y0, x1, y1, alto_cuerpo)
    if not pts:
        return [f'{slug}: sin contorno']

    ccx, ccy = x0 + bw / 2, y0 + alto_cuerpo / 2      # centro del cuerpo
    total = opacos(alpha)

    # repartir el contorno en zonas y darle una a cada variante
    def zona(p):
        arriba = p[1] < y0 + alto_cuerpo * 0.45
        izq = p[0] < ccx
        return ('arriba' if arriba else 'abajo') + ('-izq' if izq else '-der')
    porzona = {}
    for p in pts:
        porzona.setdefault(zona(p), []).append(p)
    zonas = [z for z in ['arriba-izq', 'arriba-der', 'abajo-izq', 'abajo-der'] if porzona.get(z)]

    lineas = []
    for v in range(1, VARIANTES + 1):
        rnd = random.Random((hash(slug) & 0xffff) + v * 7919)
        cand = porzona[zonas[(v - 1) % len(zonas)]]   # una zona distinta por variante
        hecho = False
        for intento in range(intentos):
            ex, ey = rnd.choice(cand)
            R = bw * rnd.uniform(0.30, 0.46)

            # empujar el centro hacia AFUERA: muerde el borde, no deja un agujero
            vx, vy = ex - ccx, ey - ccy
            n = math.hypot(vx, vy) or 1
            salida = R * rnd.uniform(0.42, 0.62)
            cx, cy = ex + vx / n * salida, ey + vy / n * salida

            hacia = math.atan2(ccy - cy, ccx - cx)    # los dientes, hacia el cuerpo
            mordida = tallar(W, H, cx, cy, R, rnd, hacia)
            nueva = Image.composite(Image.new('L', (W, H), 0), alpha, mordida)
            comido = 100 * (total - opacos(nueva)) / total

            if COMIDO_MIN <= comido <= COMIDO_MAX:
                out_im = im.copy()
                out_im.putalpha(nueva)
                if H > ALTO_SALIDA:                   # solo se usa en miniatura
                    out_im = out_im.resize(
                        (round(W * ALTO_SALIDA / H), ALTO_SALIDA), Image.LANCZOS)
                out = os.path.join(BASE, f'{slug}-mordido-{v}.png')
                out_im.save(out, 'PNG', optimize=True)
                lineas.append(f'{slug:16s} v{v}  {os.path.getsize(out)//1024:4d} KB  '
                              f'comio {comido:4.1f}%  ·  {zona((ex, ey))}')
                hecho = True
                break
        if not hecho:
            lineas.append(f'{slug:16s} v{v}  sin mordida válida')
    return lineas


if __name__ == '__main__':
    sabores = sorted(
        os.path.basename(f)[:-4] for f in glob.glob(os.path.join(BASE, '*.png'))
        if '-mordido' not in f)
    print(f'Generando {VARIANTES} mordidas x {len(sabores)} sabores...\n')
    for s in sabores:
        for linea in generar(s):
            print('  ' + linea)
    archivos = glob.glob(os.path.join(BASE, '*-mordido-*.png'))
    kb = sum(os.path.getsize(f) for f in archivos) // 1024
    print(f'\n{len(archivos)} mordidas · {kb} KB ({kb/1024:.1f} MB) en disco')
    print(f'Por visita solo se carga 1 por sabor: ~{kb//VARIANTES} KB')
