from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .generator import generate_qr


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate QR codes from text or links.")
    parser.add_argument(
        "data",
        type=str,
        nargs="?",
        help="Text or URL to encode (ignored if --input-file is provided)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("qr.png"),
        help="Output file path (extension determines format: .png or .svg)",
    )
    parser.add_argument(
        "--size",
        type=int,
        default=10,
        help="Box size (pixels per module) for raster output",
    )
    parser.add_argument(
        "--border",
        type=int,
        default=4,
        help="Quiet-zone border width (modules)",
    )
    parser.add_argument(
        "--ec",
        choices=["L", "M", "Q", "H"],
        default="M",
        help="Error correction level: L (7%), M (15%), Q (25%), H (30%)",
    )
    parser.add_argument(
        "--fill-color",
        type=str,
        default="black",
        help="Foreground color (e.g., black, #000000)",
    )
    parser.add_argument(
        "--bg-color",
        type=str,
        default="white",
        help="Background color (e.g., white, #FFFFFF)",
    )
    parser.add_argument(
        "--input-file",
        type=Path,
        help="Read input text from a file path",
    )

    args = parser.parse_args(argv)

    if args.input_file:
        if not args.input_file.exists():
            parser.error(f"Input file not found: {args.input_file}")
        args.data = args.input_file.read_text(encoding="utf-8")

    if not args.data:
        parser.error("No input provided. Pass text/URL as positional arg or use --input-file.")

    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])

    try:
        saved = generate_qr(
            data=args.data,
            output_path=args.output,
            box_size=args.size,
            border=args.border,
            error_correction=args.ec,
            fill_color=args.fill_color,
            back_color=args.bg_color,
        )
    except Exception as exc:  # noqa: BLE001
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Saved QR to: {saved}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())