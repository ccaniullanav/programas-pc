"""Descarga los instaladores OFICIALES de la instalación normal (la que hace TI) y los deja en un .zip ordenado.

Uso (lo ejecuta GitHub Actions, flujo «Instaladores oficiales»):
    python descargar_oficiales.py [--python 3.13.17] [--libreoffice 25.8.7] [--salida dist]

- Python: la versión exacta indicada, desde python.org. La huella sha256 se toma de la API oficial de python.org.
- LibreOffice: la versión indicada, desde download.documentfoundation.org. La huella sha256 es la que publica junto a cada archivo.
Si alguna huella no coincide o no está publicada, se detiene sin armar nada.

Resultado: Instaladores_<python>_<libreoffice>.zip con
    Windows/         instalador de Python (64 bits) y de LibreOffice (x86-64)
    Mac/Silicon/     instalador de Python (universal2, sirve para ambos Mac) y LibreOffice para chip Apple (aarch64)
    Mac/Intel/       instalador de Python (universal2) y LibreOffice para Intel (x86-64)
    SHA256SUMS.txt   huellas de todos los archivos, con su enlace oficial
    LEEME.txt
"""
import os, re, sys, json, hashlib, zipfile, argparse, urllib.request, urllib.parse, shutil

UA = {'User-Agent': 'panel-eeff-instaladores'}

def leer_url(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r: return r.read()

def bajar(url, destino):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=600) as r, open(destino, 'wb') as f:
        shutil.copyfileobj(r, f, 1 << 20)
    h = hashlib.sha256()
    with open(destino, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()

def archivos_python(version):
    """Instaladores de python.org con su sha256 oficial (API de python.org)."""
    rel = json.loads(leer_url('https://www.python.org/api/v2/downloads/release/?name=' + urllib.parse.quote(f'Python {version}')))
    if not rel: raise SystemExit(f'python.org no tiene la versión {version}')
    rid = rel[0]['resource_uri'].rstrip('/').split('/')[-1]
    files = json.loads(leer_url(f'https://www.python.org/api/v2/downloads/release_file/?release={rid}'))
    def buscar(patron):
        for f in files:
            if re.search(patron, f['url']): return f
        raise SystemExit(f'No se encontró en python.org el instalador {patron} de {version}')
    out = {}
    for clave, patron in (('win', rf'python-{re.escape(version)}-amd64\.exe$'), ('mac', rf'python-{re.escape(version)}-macos\d+\.pkg$')):
        f = buscar(patron)
        if not f.get('sha256_sum'): raise SystemExit(f'python.org no publica la huella sha256 de {f["url"]}')
        out[clave] = (f['url'], f['sha256_sum'].lower())
    return out

def archivos_libreoffice(v):
    for base in ('https://download.documentfoundation.org/libreoffice/stable/', 'https://downloadarchive.documentfoundation.org/libreoffice/old/'):
        urls = {'win': f'{base}{v}/win/x86_64/LibreOffice_{v}_Win_x86-64.msi',
                'silicon': f'{base}{v}/mac/aarch64/LibreOffice_{v}_MacOS_aarch64.dmg',
                'intel': f'{base}{v}/mac/x86_64/LibreOffice_{v}_MacOS_x86-64.dmg'}
        try:
            return {k: (u, leer_url(u + '.sha256').decode().split()[0].lower()) for k, u in urls.items()}
        except Exception as e:
            print(f'  no disponible en {base}: {e}')
    raise SystemExit(f'No se encontró LibreOffice {v} con huellas publicadas')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--python', default='3.13.17')
    ap.add_argument('--libreoffice', default='25.8.7')
    ap.add_argument('--salida', default='dist')
    a = ap.parse_args()
    py = a.python
    lo = a.libreoffice
    py_f, lo_f = archivos_python(py), archivos_libreoffice(lo)
    plan = [('Windows', py_f['win']), ('Windows', lo_f['win']),
            ('Mac/Silicon', py_f['mac']), ('Mac/Silicon', lo_f['silicon']),
            ('Mac/Intel', py_f['mac']), ('Mac/Intel', lo_f['intel'])]
    tmp = os.path.join(a.salida, 'descargas'); os.makedirs(tmp, exist_ok=True)
    sumas, locales = [], {}
    for carpeta, (url, esperada) in plan:
        nombre = url.rsplit('/', 1)[1]
        if url not in locales:
            p = os.path.join(tmp, nombre)
            print(f'Descargando {url}', flush=True)
            real = bajar(url, p)
            if real != esperada: raise SystemExit(f'HUELLA DISTINTA en {nombre}: publicada {esperada}, descargada {real}')
            print(f'  sha256 verificada: {real}', flush=True)
            locales[url] = p
        sumas.append(f'{esperada}  {carpeta}/{nombre}    ({url})')
    leeme = f'''INSTALADORES OFICIALES · PYTHON Y LIBREOFFICE
Python {py} (python.org) y LibreOffice {lo} (documentfoundation.org), sin modificar.
Cada archivo fue verificado contra la huella sha256 publicada por su fuente oficial (ver SHA256SUMS.txt).

Windows/      python-{py}-amd64.exe: marcar "Add python.exe to PATH". Sin admin: elegir instalar solo para el usuario.
              LibreOffice_{lo}_Win_x86-64.msi
Mac/Silicon/  Mac con chip Apple (M1, M2, M3, M4...). El instalador de Python sirve para ambos Mac (universal2).
Mac/Intel/    Mac con procesador Intel.
              En Mac, Python pide clave de administrador. LibreOffice no: basta arrastrarlo a la carpeta Aplicaciones del usuario.
'''
    zp = os.path.join(a.salida, f'Instaladores_Python{py}_LibreOffice{lo}.zip')
    with zipfile.ZipFile(zp, 'w', zipfile.ZIP_STORED, allowZip64=True) as z:     # los instaladores ya vienen comprimidos
        for carpeta, (url, _) in plan:
            z.write(locales[url], f'Instaladores/{carpeta}/{url.rsplit("/", 1)[1]}')
        z.writestr('Instaladores/SHA256SUMS.txt', '\n'.join(sumas) + '\n')
        z.writestr('Instaladores/LEEME.txt', leeme)
    open(os.path.join(a.salida, 'SHA256SUMS.txt'), 'w').write('\n'.join(sumas) + '\n')
    print(f'Listo: {zp} ({os.path.getsize(zp) / 1e6:.0f} MB)')
    with open(os.environ.get('GITHUB_OUTPUT', os.devnull), 'a') as f: f.write(f'zip={zp}\nsumas={os.path.join(a.salida, "SHA256SUMS.txt")}\npy={py}\nlo={lo}\n')

if __name__ == '__main__':
    main()
