"""Recraft helper (optional). Standard library only.

The API key is read from the RECRAFT_API_KEY environment variable and is never printed or saved.

Generate:
  python3 -I recraft.py <outdir> <name> <prompt-file> [--n 2] [--size 1:1] [--model recraftv4_1_flash]
                        [--style <style>] [--substyle <substyle>] [--style-id <uuid>] [--extra '{"k": "v"}']
Create a style from 1-5 reference images:
  python3 -I recraft.py style <outdir> <style-name> --model recraftv4_1_vector --base vector_illustration ref1.svg [ref2.svg ...]

Writes <outdir>/<name>-<i>.<webp|png|svg|jpg> and <name>.json (request + response, no key).
Models, prices, and parameters change: check https://www.recraft.ai/docs before relying on defaults.
"""
import argparse
import base64
import json
import mimetypes
import os
import re
import sys
import urllib.error
import urllib.request
import uuid

API = "https://external.api.recraft.ai/v1"
ENV_KEY = "RECRAFT_API_KEY"


def api_key():
    key = os.environ.get(ENV_KEY)
    if not key:
        sys.exit(f"{ENV_KEY} is not set: skip generated assets, make hand/derived assets, and note it in your report.")
    return key


def safe_name(name):
    if not re.fullmatch(r"[A-Za-z0-9._-]+", name) or name.startswith("."):
        sys.exit(f"invalid name {name!r}: use letters, digits, dot, dash, underscore")
    return name


def call(req):
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.read()[:800].decode(errors='replace')}")


def download(url, path):
    if not url.startswith("https://"):
        sys.exit(f"refusing non-https download URL: {url[:80]}")
    with urllib.request.urlopen(url, timeout=300) as r, open(path, "wb") as f:
        f.write(r.read())


def fix_ext(path):
    with open(path, "rb") as f:
        head = f.read(64)
    if head[8:12] == b"WEBP":
        ext = "webp"
    elif head[:4] == b"\x89PNG":
        ext = "png"
    elif b"<svg" in head or head.lstrip().startswith(b"<"):
        ext = "svg"
    else:
        ext = "jpg"
    final = os.path.splitext(path)[0] + "." + ext
    os.replace(path, final)
    return final


def generate(a):
    name = safe_name(a.name)
    with open(a.prompt_file, encoding="utf-8") as f:
        prompt = f.read().strip()
    body = {"prompt": prompt, "model": a.model, "n": a.n, "size": a.size}
    if a.style:
        body["style"] = a.style
    if a.substyle:
        body["substyle"] = a.substyle
    if a.style_id:
        body["style_id"] = a.style_id
    if a.extra:
        body.update(json.loads(a.extra))
    req = urllib.request.Request(
        f"{API}/images/generations", data=json.dumps(body).encode(), method="POST",
        headers={"Authorization": "Bearer " + api_key(), "Content-Type": "application/json"})
    d = call(req)
    os.makedirs(a.outdir, exist_ok=True)
    with open(os.path.join(a.outdir, name + ".json"), "w", encoding="utf-8") as f:
        json.dump({"request": body, "response": d}, f, indent=1, ensure_ascii=False)
    for i, item in enumerate(d.get("data", [])):
        p = os.path.join(a.outdir, f"{name}-{i + 1}.img")
        if item.get("url"):
            download(item["url"], p)
        elif item.get("b64_json"):
            with open(p, "wb") as f:
                f.write(base64.b64decode(item["b64_json"]))
        else:
            continue
        print("saved", fix_ext(p))
    print(name, "credits", d.get("credits"))


def style(a):
    name = safe_name(a.name)
    boundary = uuid.uuid4().hex
    parts = [f'--{boundary}\r\nContent-Disposition: form-data; name="style"\r\n\r\n{a.base}\r\n'.encode()]
    if a.model:
        parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="model"\r\n\r\n{a.model}\r\n'.encode())
    for i, ref in enumerate(a.refs[:5]):
        mime = "image/svg+xml" if ref.endswith(".svg") else mimetypes.guess_type(ref)[0] or "application/octet-stream"
        with open(ref, "rb") as f:
            data = f.read()
        parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="file{i + 1}"; '
                     f'filename="{os.path.basename(ref)}"\r\nContent-Type: {mime}\r\n\r\n'.encode() + data + b"\r\n")
    parts.append(f"--{boundary}--\r\n".encode())
    req = urllib.request.Request(
        f"{API}/styles", data=b"".join(parts), method="POST",
        headers={"Authorization": "Bearer " + api_key(),
                 "Content-Type": f"multipart/form-data; boundary={boundary}"})
    d = call(req)
    os.makedirs(a.outdir, exist_ok=True)
    with open(os.path.join(a.outdir, name + ".style.json"), "w", encoding="utf-8") as f:
        json.dump({"base": a.base, "model": a.model, "refs": a.refs, "response": d}, f, indent=1)
    print("style_id", d.get("id"))


def main(argv):
    if len(argv) > 1 and argv[1] == "style":
        p = argparse.ArgumentParser(description="Create a Recraft style from reference images.")
        p.add_argument("cmd")
        p.add_argument("outdir")
        p.add_argument("name")
        p.add_argument("--base", default="vector_illustration")
        p.add_argument("--model")
        p.add_argument("refs", nargs="+")
        style(p.parse_args(argv[1:]))
    else:
        p = argparse.ArgumentParser(description="Generate images with Recraft.")
        p.add_argument("outdir")
        p.add_argument("name")
        p.add_argument("prompt_file")
        p.add_argument("--n", type=int, default=2)
        p.add_argument("--size", default="1:1")
        p.add_argument("--model", default="recraftv4_1_flash")
        p.add_argument("--style")
        p.add_argument("--substyle")
        p.add_argument("--style-id")
        p.add_argument("--extra", help="extra JSON fields merged into the request body")
        generate(p.parse_args(argv[1:]))


if __name__ == "__main__":
    main(sys.argv)
