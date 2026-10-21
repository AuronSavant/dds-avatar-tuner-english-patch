"""Redraw the Japanese labels in the game's sprite atlases (resource 'png') in English.

    python tools/images.py      reads backup/png.orig, writes images/png
"""
import io, os, struct, sys
from collections import Counter
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pixfont  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (atlas, x, y, w, h, text, font, align)   rects come from the sprite table in 'game'
LABELS = [
    (2, 0, 0, 22, 6, 'SERPH', '3x5', 'l'),
    (2, 22, 0, 31, 6, 'ARGILLA', '3x5', 'l'),
    (2, 53, 0, 19, 8, 'HEAT', '3x5', 'l'),
    (2, 0, 27, 11, 11, 'ST', '5x7', 'c'),
    (2, 0, 38, 11, 11, 'VI', '5x7', 'c'),
    (2, 0, 49, 11, 12, 'MA', '5x7', 'c'),
    (2, 0, 61, 11, 13, 'AG', '5x7', 'c'),
    (2, 0, 74, 11, 12, 'LU', '5x7', 'c'),
    (2, 20, 36, 44, 10, 'VARNA', '5x7', 'l'),
    (2, 20, 46, 37, 10, 'AGNI', '5x7', 'l'),
    (2, 20, 56, 70, 10, 'PRITHIVI', '5x7', 'l'),
    (2, 98, 44, 43, 9, 'EQUIPPED', '4x7', 'l'),
    (2, 98, 53, 43, 9, 'INNATE', '4x7', 'l'),
    (2, 151, 44, 44, 9, 'ITEMS', '4x7', 'l'),
    (2, 151, 53, 43, 8, 'DERIVED', '4x7', 'l'),
    (2, 98, 77, 79, 10, 'ITEM VENDOR', '5x7', 'l'),
    (2, 98, 87, 20, 10, 'BUY', '4x7', 'l'),
    (2, 98, 98, 20, 10, 'SELL', '4x7', 'l'),
    (3, 1, 18, 61, 10, 'LG TERMINAL', '4x7', 'l'),
    (3, 1, 28, 61, 10, 'SM TERMINAL', '4x7', 'l'),
    (3, 64, 18, 25, 11, 'HEAL', '4x7', 'c'),
    (3, 64, 29, 25, 11, 'HEAL', '4x7', 'c'),
    (3, 91, 18, 25, 11, 'WARP', '4x7', 'c'),
    (3, 1, 214, 44, 11, 'RECOVERY', '4x7', 'l'),
    (3, 46, 215, 56, 10, 'DATA LOAD', '5x7', 'l'),
    (3, 131, 41, 59, 10, 'DATA SAVE', '5x7', 'l'),
    (3, 131, 30, 65, 10, 'MANTRA DATA', '5x7', 'l'),
    (3, 131, 18, 51, 12, 'AVAILABLE', '4x7', 'l'),
    (3, 183, 52, 51, 12, 'LOCKED', '5x7', 'l'),
    (3, 131, 52, 50, 12, 'EQUIPPED', '4x7', 'l'),
    (3, 191, 42, 43, 9, 'MASTER', '5x7', 'l'),
    (3, 215, 23, 41, 10, 'ACQUIRED', '4x7', 'l'),
    (3, 183, 1, 68, 11, 'DIFFICULTY', '4x7', 'l'),
    (3, 183, 12, 21, 10, '', '4x7', 'l'),
    (3, 204, 12, 23, 10, 'REQ:', '4x7', 'l'),
]


def read_pack(d):
    n = d[0]; p = 1; out = []
    for _ in range(n):
        size = struct.unpack('>H', d[p:p + 2])[0]
        out.append(d[p + 2:p + 2 + size]); p += 2 + size
    return out


def write_pack(blobs):
    return bytes([len(blobs)]) + b''.join(struct.pack('>H', len(b)) + b for b in blobs)


def main():
    os.makedirs(os.path.join(ROOT, 'images'), exist_ok=True)
    blobs = read_pack(open(os.path.join(ROOT, 'backup', 'png.orig'), 'rb').read())
    for atlas in sorted({l[0] for l in LABELS}):
        im = Image.open(io.BytesIO(blobs[atlas]))
        im.load()
        trans = im.info.get('transparency')
        for a, x, y, w, h, text, font, align in LABELS:
            if a != atlas:
                continue
            px = [im.getpixel((i, j)) for j in range(y, y + h) for i in range(x, x + w)]
            colors = Counter(c for c in px if c != trans)
            color = colors.most_common(1)[0][0]
            for j in range(y, y + h):
                for i in range(x, x + w):
                    im.putpixel((i, j), trans)
            if not text:
                continue
            tw = pixfont.text_width(text, font)
            th = len(pixfont.FONTS[font]['A'])
            assert tw <= w, (text, tw, w)
            tx = x if align == 'l' else x + (w - tw) // 2
            ty = y + (h - th) // 2
            pixfont.draw(im, tx, ty, text, font, color)
        buf = io.BytesIO()
        im.save(buf, 'GIF', transparency=trans)
        blobs[atlas] = buf.getvalue()
        im.convert('RGBA').resize((im.width * 3, im.height * 3), 0).save(
            os.path.join(ROOT, 'images', 'preview_atlas%d.png' % atlas))
    open(os.path.join(ROOT, 'images', 'png'), 'wb').write(write_pack(blobs))
    print('sprite atlases written')


if __name__ == '__main__':
    main()
