# Grattisimo · Bloques animados para Wix

Widgets para "Embed a Widget / HTML iFrame" de Wix. Todo autocontenido
(sin librerías externas). El scroll de la página padre NO es accesible desde
el iframe, así que las animaciones de entrada usan **IntersectionObserver
(root:null)** — funciona dentro del embed de Wix — y las interacciones son
locales (drag/swipe/click).

## Archivos

| Archivo | Qué es |
|---|---|
| **grattisimo-completo.html** | ⭐ PÁGINA COMPLETA standalone: nav · hero (logo Verde + foto mano) · visor Selección 2026 (helados flotando) · por qué · menú (17 helados sin fondo) · aliados/cifras · 11 tiendas · CTA · footer |
| **index.html** | Copia exacta de la anterior (doble-click y listo) |
| **helados/** | 20 PNG de sabores SIN FONDO, optimizados a ~900px (recortados + comprimidos). Los usa el carrusel y el menú. |
| **logo-verde.png** | Logo oficial completo en Verde #014638 (para el hero) |
| grattisimo-mani-cafe.jpg | Foto de la mano con el maní‑café (720×900) |
| contenido-extraido.md | Todo el contenido real de grattisimo.com (copy, cifras, links PY) |
| wix-test.html | Simulador con scroll (para probar como si fuera Wix) |
| grattisimo-hand-foto*.html / grattisimo-selector.html / grattisimo-sel-sprite.jpg | Bloques sueltos y sprite de la etapa "embed de Wix" (ya no los usa la página principal) |

## Cómo verla / publicarla (página standalone)

Es una página web normal. Para verla: **doble‑click en `index.html`**.
Para subirla a un hosting, sube estos archivos manteniendo la estructura:

```
index.html  (o grattisimo-completo.html)
logo-verde.png
grattisimo-mani-cafe.jpg
helados/  ← la carpeta completa con los 20 PNG
```

Los helados y el logo Verde son locales; los logos de aliados y el logo
menta de la banda/nav/footer cargan del CDN de Wix (`static.wixstatic.com`),
y Montserrat de Google Fonts. Con internet, todo carga solo.

> Si algún día se vuelve a un **embed de Wix**: habría que subir `helados/`,
> `logo-verde.png` y la foto de la mano a Wix Media y reemplazar las rutas
> relativas por las URLs de Wix. Hoy la página apunta a rutas locales.

## Contenido integrado (aprobado)
- Cifra de alcance: **+10,000 clientes/mes** (elegida por consistencia con
  10 locales; el sitio también decía "+1,000 pedidos a domicilio/mes" —
  queda comentada en el HTML por si se confirma la otra).
- "+30 sabores" (claim del sitio; el menú publica 17 con foto).
- WhatsApp con link corregido: wa.me/50255740469 (el del sitio estaba roto,
  sin código de país) + texto precargado.
- Typos corregidos: Elige/diabéticos/Tú eliges/Guanábana/alérgenos; "0% culpa"
  una sola vez; bloque "lo peor del postre" una sola vez como comparativa.
- URL de Facebook asumida: facebook.com/grattisimo (el arte solo dice @grattisimo).

## Qué hace cada sección

**La mano (post del maní con café):** la foto real se desliza hacia arriba
dentro de una tarjeta del mismo gris que el fondo del JPG — se ve como si la
mano alzara el helado, sin recortes. Anima UNA vez al entrar al viewport,
con rebote + inclinación final + destellos + copy escalonado.
Botón "Ver de nuevo" para repetirla. Respeta `prefers-reduced-motion`.

**Visor Selección 2026 (estilo Apple):** tarjeta central + vecinas asomando
atenuadas; drag con mouse / swipe táctil con inercia (máx. una tarjeta por
gesto), escala y opacidad interpoladas en cada frame, easing tipo iOS,
dots + chevrons circulares + flechas del teclado. `touch-action: pan-y`
para no bloquear el scroll vertical en móvil.

## Pendiente para la revisión

- ✏️ **Copy:** todos los textos son placeholder (marcados con `✏️ COPY` en el
  HTML). Faltan los 6 problemas de copy/estructura identificados en la sesión
  anterior — no los tengo registrados; pásalos y los integro.
- 👀 **Vista final en navegador:** la lógica quedó verificada por
  instrumentación (geometría, estados, física del drag), pero Chrome perdió
  la conexión de automatización a mitad de las pruebas visuales del slider
  Apple. Abre `wix-test.html` y confirma que el movimiento se siente bien.
- 📸 Si consigues fotos de UN helado desde varios ángulos, se puede hacer el
  visor giratorio 360°/mecedora original.
