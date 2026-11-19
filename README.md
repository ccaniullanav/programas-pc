# Programas para los equipos

Instaladores **oficiales y sin modificar** de **Python 3.13.17** y **LibreOffice 25.8.7** para Windows y macOS (Intel y Apple Silicon).

## Descarga

En [Releases](../../releases/latest):

- **Todo (Windows y Mac):** [Instaladores_Python3.13.17_LibreOffice25.8.7.zip](https://github.com/ccaniullanav/programas-pc/releases/download/python3.13.17-libreoffice25.8.7/Instaladores_Python3.13.17_LibreOffice25.8.7.zip) (≈1,1 GB)
- **Solo Windows:** [Instaladores_Windows_Python3.13.17_LibreOffice25.8.7.zip](https://github.com/ccaniullanav/programas-pc/releases/download/python3.13.17-libreoffice25.8.7/Instaladores_Windows_Python3.13.17_LibreOffice25.8.7.zip) (≈400 MB)
- [SHA256SUMS.txt](https://github.com/ccaniullanav/programas-pc/releases/download/python3.13.17-libreoffice25.8.7/SHA256SUMS.txt)

| Carpeta del zip | Contenido |
|---|---|
| `Windows/` | `python-3.13.17-amd64.exe` y `LibreOffice_25.8.7_Win_x86-64.msi` |
| `Mac/Silicon/` | `python-3.13.17-macos11.pkg` (universal2) y `LibreOffice_25.8.7_MacOS_aarch64.dmg` |
| `Mac/Intel/` | `python-3.13.17-macos11.pkg` (universal2) y `LibreOffice_25.8.7_MacOS_x86-64.dmg` |

Para saber qué Mac es: menú Apple > Acerca de este Mac. «Chip Apple M…» es Silicon; «Procesador Intel» es Intel.

## Notas de instalación

- **Python en Windows**: marcar «Add python.exe to PATH». Se puede instalar sin administrador eligiendo instalar solo para el usuario.
- **Python en Mac**: el instalador oficial pide clave de administrador.
- **LibreOffice en Mac**: no requiere administrador si se arrastra a la carpeta Aplicaciones del usuario.

## Origen y verificación

| Archivo | Enlace oficial |
|---|---|
| Python Windows | https://www.python.org/ftp/python/3.13.17/python-3.13.17-amd64.exe |
| Python Mac | https://www.python.org/ftp/python/3.13.17/python-3.13.17-macos11.pkg |
| LibreOffice Windows | https://download.documentfoundation.org/libreoffice/stable/25.8.7/win/x86_64/LibreOffice_25.8.7_Win_x86-64.msi |
| LibreOffice Mac Apple Silicon | https://download.documentfoundation.org/libreoffice/stable/25.8.7/mac/aarch64/LibreOffice_25.8.7_MacOS_aarch64.dmg |
| LibreOffice Mac Intel | https://download.documentfoundation.org/libreoffice/stable/25.8.7/mac/x86_64/LibreOffice_25.8.7_MacOS_x86-64.dmg |

El zip lo arma GitHub Actions ([`scripts/descargar_oficiales.py`](scripts/descargar_oficiales.py)): descarga cada archivo de su fuente oficial y lo compara con la huella SHA-256 que publica esa fuente (API de python.org y archivos `.sha256` de documentfoundation.org). Si alguna no coincide, no se publica nada.

Para comprobar un archivo descargado:
- Windows (PowerShell): `Get-FileHash .\archivo -Algorithm SHA256`
- Mac (Terminal): `shasum -a 256 archivo`
