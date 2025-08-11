# QR Generator (Python)

Generate scannable QR codes from links or text using a simple Python CLI.

## Quick start

1) Create a virtual environment and install dependencies

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install -U pip
./.venv/bin/python -m pip install -r requirements.txt
```

2) Generate a QR code (PNG)

```bash
./.venv/bin/python -m qrgen.cli "https://example.com" -o out.png
```

3) Generate from a file, change error correction and size

```bash
./.venv/bin/python -m qrgen.cli --input-file ./message.txt -o out.png --ec H --size 8 --border 2
```

4) Generate SVG

```bash
./.venv/bin/python -m qrgen.cli "Hello SVG" -o out.svg
```

## CLI options

```text
usage: python -m qrgen.cli [-h] [-o OUTPUT] [--size SIZE] [--border BORDER] [--ec {L,M,Q,H}] [--fill-color FILL_COLOR] [--bg-color BG_COLOR] [--input-file INPUT_FILE] data

positional arguments:
  data                  Text or URL to encode (ignored if --input-file is provided)

options:
  -h, --help            Show this help message and exit
  -o, --output OUTPUT   Output file path (extension determines format: .png or .svg) [default: qr.png]
  --size SIZE           Box size (pixels per module) for raster output [default: 10]
  --border BORDER       Quiet-zone border width (modules) [default: 4]
  --ec {L,M,Q,H}        Error correction level: L (7%), M (15%), Q (25%), H (30%) [default: M]
  --fill-color FILL_COLOR
                        Foreground color (e.g., black, #000000)
  --bg-color BG_COLOR   Background color (e.g., white, #FFFFFF)
  --input-file INPUT_FILE
                        Read input text from a file path
```

## Notes
- PNG output requires Pillow (installed via qrcode[pil]).
- SVG output does not require Pillow and is vector-based.
- The output directory is created automatically if it does not exist.