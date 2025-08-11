from __future__ import annotations

from pathlib import Path
from typing import Literal, Optional

import qrcode
from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H
from qrcode.image.svg import SvgImage


ErrorCorrection = Literal["L", "M", "Q", "H"]


def _map_error_correction(level: ErrorCorrection) -> int:
    mapping = {
        "L": ERROR_CORRECT_L,
        "M": ERROR_CORRECT_M,
        "Q": ERROR_CORRECT_Q,
        "H": ERROR_CORRECT_H,
    }
    return mapping[level]


def generate_qr(
    data: str,
    output_path: str | Path,
    *,
    box_size: int = 10,
    border: int = 4,
    error_correction: ErrorCorrection = "M",
    fill_color: str = "black",
    back_color: str = "white",
) -> Path:
    """Generate a QR code image from text and save it.

    Automatically selects PNG or SVG based on the output file extension.

    Args:
        data: Text or URL to encode.
        output_path: Destination file path. Extension determines format (.png or .svg).
        box_size: Pixel size of each QR module (PNG only).
        border: Quiet-zone border in modules.
        error_correction: Error correction level: L, M, Q, or H.
        fill_color: Foreground color.
        back_color: Background color.

    Returns:
        The path to the saved file.
    """
    if not isinstance(data, str) or len(data.strip()) == 0:
        raise ValueError("Input 'data' must be a non-empty string")

    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)

    extension = destination.suffix.lower()
    ec = _map_error_correction(error_correction)

    if extension == ".svg":
        # Vector output (no Pillow required)
        qr = qrcode.QRCode(
            version=None,
            error_correction=ec,
            box_size=box_size,  # Not used for SVG but kept for API symmetry
            border=border,
            image_factory=SvgImage,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color=fill_color, back_color=back_color)
        img.save(destination)
        return destination

    # Default to PNG (raster) output
    qr = qrcode.QRCode(
        version=None,
        error_correction=ec,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    img.save(destination)
    return destination