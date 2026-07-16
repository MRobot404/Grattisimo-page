# Grattisimo — Landing

Rediseño de la landing de **Grattisimo** (heladería artesanal, Ciudad de Guatemala).
Página autónoma en HTML/CSS/JS, sin build ni framework.

> **tu sabor, tu salud**

## Cómo verla

Doble‑click en **`index.html`**. Necesita internet para Montserrat (Google Fonts),
GSAP (CDN) y los videos/logos del CDN de Wix.

## Estructura de la página

| # | Sección | Qué hace |
|---|---|---|
| 1 | Portada | Logo oficial + abanico de 3 tarjetas con los videos reales del sitio (coco, reel de fresa) y la foto de la niña |
| 2 | Paleta 3D | Dos caras («tu sabor» / «tu salud») que giran con el scroll (GSAP ScrollTrigger, pinned) y se arrastran con inercia |
| 3 | La mano | Foto real del maní con café que se alza al entrar en pantalla |
| 4 | Selección 2026 | Carrusel estilo Apple: helados sin fondo flotando, escala y brillo por distancia al centro, paginación de píldora |
| 5 | Por qué Grattisimo | Comparativa postre tradicional vs. Grattisimo |
| 6 | Menú | Los 17 sabores con foto recortada (11 de fruta + 6 cremosos) |
| 7 | Respaldo | Aliados comerciales + cifras con contador animado |
| 8 | Encuéntranos | 11 tiendas con link directo a su menú en PedidosYa |
| 9 | Cómo pedir | PedidosYa · WhatsApp · Tiendas + CTA |
| 10 | Footer | Contacto y redes |

## Archivos

| Archivo | Qué es |
|---|---|
| `index.html` / `grattisimo-completo.html` | ⭐ La página (copias idénticas) |
| `helados/` | 20 sabores en PNG sin fondo, optimizados (~900px) |
| `logo-verde.png` | Logo oficial completo en Verde |
| `grattisimo-mani-cafe.jpg` | Foto de la mano con el maní‑café |
| `prueba-3d.html` + `flavors-data.js` | Demo comparativo: pseudo‑3D (tilt/giroscopio) vs. modelo WebGL |
| `contenido-extraido.md` | Contenido real extraído de grattisimo.com (copy, cifras, assets, links) |
| `LEEME.md` | Guía de publicación y notas |
| `wix-test.html`, `grattisimo-hand*.html`, `grattisimo-selector.html`, `grattisimo-pseudo3d.html`, `sabor-*.jpg`, `grattisimo-sel-sprite.jpg` | Etapas previas (embed de Wix), se conservan como historial |

## Línea gráfica

Según el Manual de Marca oficial (2021):

| Color | HEX | Uso |
|---|---|---|
| Verde | `#014638` | Principal |
| Menta | `#6CC1B0` | Principal |
| Menta Pastel | `#97CFC1` | Principal |
| Rosa | `#FFA9C6` | Secundario |
| Rosa Chicle | `#F279A1` | Secundario |
| Rosa Pastel | `#FFCAD5` | Secundario |
| Cobre | `#DB9677` | Solo detalles |

Tipografía: **Montserrat** (única institucional).

## Accesibilidad y rendimiento

- Animaciones de entrada por `IntersectionObserver`, una sola vez.
- Solo se animan `transform`, `opacity` y `filter` (GPU).
- Posiciones del carrusel calculadas, sin lecturas de layout por frame.
- `prefers-reduced-motion` respetado; hover con desplazamiento limitado a punteros finos.

## Notas pendientes

- Cifra de alcance: se usa **+10,000 clientes/mes**; el sitio original también
  menciona "+1,000 pedidos a domicilio/mes" (por confirmar cuál es la oficial).
- El sitio publica "+30 sabores" pero el menú lista 17 con foto.
- URL de Facebook asumida (`facebook.com/grattisimo`); el arte oficial solo dice `@grattisimo`.
