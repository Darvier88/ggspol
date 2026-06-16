#!/usr/bin/env python3
"""Compila content/juegos/*.md -> games.json (lo que consume la web).
Se ejecuta automáticamente con GitHub Actions cada vez que cambias contenido
desde el panel /admin. También puedes correrlo a mano: python scripts/build-games.py
"""
import os, glob, json, sys
import yaml  # pyyaml

CONTENT = "content/juegos"
OUT = "games.json"

def parse_md(path):
    raw = open(path, encoding="utf-8").read()
    if raw.startswith("---"):
        _, fm, body = raw.split("---", 2)
        data = yaml.safe_load(fm) or {}
        body = body.strip()
    else:
        data, body = {}, raw.strip()
    return data, body

def to_list(v):
    if v is None: return []
    if isinstance(v, list):
        out = []
        for x in v:
            if isinstance(x, dict):
                out.append(next(iter(x.values())))
            else:
                out.append(x)
        return [str(x) for x in out if x]
    return [str(v)]

games = []
for path in glob.glob(f"{CONTENT}/*.md"):
    data, body = parse_md(path)
    slug = data.get("slug") or os.path.splitext(os.path.basename(path))[0]
    fecha_orden = data.get("fecha_orden") or ""
    if fecha_orden and not isinstance(fecha_orden, str):
        fecha_orden = str(fecha_orden)
    games.append({
        "slug": str(slug),
        "nombre": data.get("nombre", ""),
        "portada": data.get("portada") or "",
        "descripcion": body or data.get("descripcion", ""),
        "fecha_texto": data.get("fecha_texto", "Sin fecha"),
        "fecha_orden": fecha_orden,
        "generos": to_list(data.get("generos")),
        "plataformas": to_list(data.get("plataformas")),
        "demo": data.get("demo", "Sin demo"),
        "trailer": data.get("trailer") or "",
        "desarrollador": data.get("desarrollador") or "",
        "tienda": data.get("tienda") or "",
        "estado": data.get("estado", "Confirmado"),
        "galeria": to_list(data.get("galeria")),
    })

games.sort(key=lambda r: (0, r["fecha_orden"]) if r["fecha_orden"] else (1, "9999"))
json.dump(games, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"games.json compilado: {len(games)} juegos")
