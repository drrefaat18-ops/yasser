"""Canonical PNG writer (plan Task 9.1): identical pixels give identical bytes. Every PNG the harness writes goes here."""
import pathlib


def write_canonical(image, path, dpi):
    """Fixed Pillow parameters; the only metadata chunk is pHYs (dpi). No time or text chunks."""
    from PIL import Image
    if image.mode not in ("RGB", "L"):
        base = Image.new("RGB", image.size, (255, 255, 255))
        rgba = image.convert("RGBA")
        base.paste(rgba, mask=rgba.getchannel("A"))
        image = base
    else:
        image = image.copy()
    image.info = {}
    path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, format="PNG", optimize=False, compress_level=9, dpi=(dpi, dpi))


def width_px(width_cm, dpi):
    """Pixel width of a figure placed at `width_cm` and `dpi`."""
    return round(width_cm / 2.54 * dpi)
