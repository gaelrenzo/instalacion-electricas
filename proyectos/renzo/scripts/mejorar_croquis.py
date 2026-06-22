#!/usr/bin/env python3
"""Mejora croquis arquitectónicos con limpieza para planos profesionales."""
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1] / "fuentes" / "croquis"
DST_DIR = Path(__file__).resolve().parents[1] / "fuentes" / "croquis-mejorados"


def enhance_sketch(img_path, output_path, upscale=3):
    print(f"  Mejorando {img_path.name}...")
    img = Image.open(img_path).convert("RGBA")

    bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
    bg.paste(img, mask=img.split()[3])
    gray = bg.convert("L")

    arr = np.array(gray, dtype=np.float32)
    bg_blur = np.array(
        gray.filter(ImageFilter.GaussianBlur(radius=25)), dtype=np.float32
    )

    diff = bg_blur - arr
    diff = np.clip(diff, 0, 255)

    contrasty = Image.fromarray(diff.astype(np.uint8))
    contrasty = ImageEnhance.Contrast(contrasty).enhance(1.5)

    arr2 = np.array(contrasty, dtype=np.float32)

    nonzero = arr2[arr2 > 8]
    threshold = np.percentile(nonzero, 55) if len(nonzero) > 100 else 40
    threshold = max(threshold, 25)

    binary = arr2 > threshold

    binary_img = Image.fromarray((binary * 255).astype(np.uint8))

    binary_img = binary_img.filter(ImageFilter.MaxFilter(3))
    binary_img = binary_img.filter(ImageFilter.MinFilter(3))

    if upscale > 1:
        binary_img = binary_img.resize(
            (img.width * upscale, img.height * upscale), Image.NEAREST
        )

    result = Image.new("RGBA", binary_img.size, (255, 255, 255, 255))
    mask = Image.eval(binary_img, lambda x: 255 if x > 128 else 0)
    result.paste((0, 0, 0, 255), mask=mask)

    DST_DIR.mkdir(parents=True, exist_ok=True)
    result.save(output_path)
    print(f"    -> {output_path.name} ({result.size[0]}x{result.size[1]})")


def main():
    print("Mejorando croquis arquitectónicos...")
    pngs = sorted(SRC_DIR.glob("piso-*.png"))
    if not pngs:
        print(f"  No se encontraron PNGs en {SRC_DIR}")
        return
    for p in pngs:
        out = DST_DIR / p.name
        enhance_sketch(p, out)


if __name__ == "__main__":
    main()
