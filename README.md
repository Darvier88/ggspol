# GG'spol — Juegos por lanzarse

Catálogo comunitario de videojuegos próximos a lanzarse. Web estática (gratis),
con panel de administración (Decap CMS) para agregar/editar juegos y subir
imágenes, y buzón de sugerencias vía Issues de GitHub.

---

## 📁 Estructura

```
ggspol/
├─ index.html              ← la web pública (catálogo + fichas)
├─ games.json              ← datos que consume la web (se compila solo)
├─ admin/
│  ├─ index.html           ← panel de administración (/admin)
│  └─ config.yml           ← configuración del panel (EDITAR el repo)
├─ content/juegos/*.md     ← un archivo por juego (lo edita el panel)
├─ assets/img/
│  ├─ logo.png             ← logo
│  └─ juegos/              ← imágenes subidas desde el panel
├─ scripts/build-games.py  ← compila los .md en games.json
└─ .github/workflows/build-data.yml  ← recompila games.json automáticamente
```

---

## ✏️ Antes de subir: 2 ediciones obligatorias

Cambia `TU_USUARIO/ggspol` por tu repositorio real en estos dos sitios:

1. **`index.html`** → busca `const CONFIG = { repo: "TU_USUARIO/ggspol" }`
   (se usa para el botón “Sugerir juego”).
2. **`admin/config.yml`** → la línea `repo: TU_USUARIO/ggspol`.

---

## 🚀 Subir gratis — Opción A (recomendada): Netlify

Netlify resuelve solo la autenticación de GitHub del panel, que es la parte
más engorrosa. Sigue siendo 100% gratis y el código vive en tu repo de GitHub.

1. Sube esta carpeta a un repositorio de GitHub (público).
2. En **app.netlify.com** → *Add new site → Import from GitHub* → elige el repo.
   Sin comandos de build; *publish directory* = la raíz. Deploy.
3. Crea una **GitHub OAuth App** (GitHub → *Settings → Developer settings →
   OAuth Apps → New*):
   - *Homepage URL*: la URL que te dio Netlify.
   - *Authorization callback URL*: `https://api.netlify.com/auth/done`
   - Copia el **Client ID** y genera un **Client Secret**.
4. En Netlify → *Site configuration → Access & security → OAuth → Install
   provider → GitHub* → pega Client ID y Secret.
5. Entra a `https://tu-sitio.netlify.app/admin/` y pulsa **Login with GitHub**.

## 🚀 Subir gratis — Opción B: GitHub Pages

La web funciona igual, pero el panel `/admin` necesita un pequeño proxy OAuth
(Netlify no está en medio). Lo más simple es desplegar el proxy gratuito de
Cloudflare Workers/Pages y poner su URL en `admin/config.yml` bajo `base_url:`.
Si no quieres lidiar con eso, usa la Opción A: el panel queda listo sin proxy.

Para activar Pages: repo → *Settings → Pages → Source: `main` / root*.

---

## 🎮 Usar el panel (/admin)

- Entra a `/admin/`, inicia sesión con GitHub.
- **Juegos → New Juego** para agregar, o clic en uno para editar.
- Sube la **portada** y arrastra imágenes a la **galería** (se guardan en el repo).
- Al **publicar**, Decap hace commit al repo. La GitHub Action recompila
  `games.json` en ~1 min y la web se actualiza sola.

> Las portadas iniciales usan la miniatura del tráiler de YouTube. Puedes
> reemplazarlas subiendo tu propia imagen desde el panel.

---

## 💡 Buzón de sugerencias

El botón **“Sugerir juego”** abre un Issue de GitHub ya pre-rellenado con la
etiqueta `sugerencia`. Crea esa etiqueta una vez en tu repo
(*Issues → Labels → New label → `sugerencia`*) para tenerlas ordenadas.

---

## 🧪 Probar en local

Por seguridad del navegador, ábrela con un servidor local (no doble clic):

```bash
cd ggspol
python3 -m http.server 8000
# abre http://localhost:8000
```

El panel `/admin` solo funciona ya desplegado (necesita la autenticación).

---

## 🔧 Recompilar datos a mano (opcional)

```bash
pip install pyyaml
python scripts/build-games.py
```
