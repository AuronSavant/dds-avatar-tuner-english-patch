"""English versions of the archive's how-to-play pages (930x632, white text on transparent).

    python tools/guide.py     reads backup/howto/*.png, writes images/howto/*.png
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'backup', 'howto')
DST = os.path.join(ROOT, 'images', 'howto')
FONT = 'C:/Windows/Fonts/segoeuib.ttf'
WHITE = (255, 255, 255, 255)
DARK = (20, 20, 30, 255)

SUBTITLE = "< DIGITAL DEVIL SAGA Avatar Tuner A's TEST Server Complete Edition >"
BOOST = ['This game has an "EXP & Reward Boost" feature.',
         'Turn "EXP & Reward Boost" ON in OPTION to triple the EXP',
         'and rewards earned after battle, making the game easier to progress.']
FOOTER = ['This game does not support auto-save.',
          'Please use the in-game save feature before quitting.']
ACTIONS = ['OPTION', 'Confirm', 'Cancel', 'Move Character / Cursor', 'Menu']
ROWS = [123, 183, 243, 303, 363]  # table row tops, each 55px tall


def font(size):
    return ImageFont.truetype(FONT, size)


def clear(im, box):
    ImageDraw.Draw(im).rectangle(box, fill=(0, 0, 0, 0))


def fill_like(im, box, sample):
    ImageDraw.Draw(im).rectangle(box, fill=im.getpixel(sample))


def center(d, y, text, f, fill=WHITE, cx=465):
    w = d.textlength(text, font=f)
    d.text((cx - w / 2, y), text, font=f, fill=fill)


def fit(d, text, size, maxw):
    while d.textlength(text, font=font(size)) > maxw:
        size -= 1
    return font(size)


def key_page(name, title, left_labels):
    im = Image.open(os.path.join(SRC, name + '.png')).convert('RGBA')
    d = ImageDraw.Draw(im)
    clear(im, (0, 20, 929, 108))
    center(d, 28, title, font(34))
    center(d, 74, SUBTITLE, fit(d, SUBTITLE, 24, 900))
    for top, act in zip(ROWS, ACTIONS):
        fill_like(im, (455, top + 6, 888, top + 50), (890, top + 28))
        d.text((465, top + 12), act, font=font(26), fill=DARK)
    for top, label in zip(ROWS, left_labels):
        if label is None:
            continue
        x0, text = label
        fill_like(im, (x0, top + 6, 440, top + 50), (442, top + 28))
        d.text((x0 + 2, top + 12), text, font=font(26), fill=WHITE)
    clear(im, (45, 440, 885, 522))
    for i, line in enumerate(BOOST):
        center(d, 448 + i * 23, line, fit(d, line, 19, 820))
    clear(im, (0, 552, 929, 631))
    for i, line in enumerate(FOOTER):
        center(d, 560 + i * 24, line, font(19))
    im.save(os.path.join(DST, name + '.png'))


def text_page(name, logo_y, blocks):
    im = Image.new('RGBA', (930, 632), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    center(d, logo_y, 'G-MODE ARCHIVES+', font(68))
    y = logo_y + 125
    for block in blocks:
        for line in block:
            center(d, y, line, fit(d, line, 23, 880))
            y += 32
        y += 22
    im.save(os.path.join(DST, name + '.png'))


ABOUT = [
    ['"G-MODE Archives+" is a revival project that faithfully',
     'recreates classic feature-phone games just as they were.'],
    ['* For the port from feature phones, some controls and',
     'features have been adjusted for more comfortable play.'],
    ['* In-game instructions and menus are kept as they were originally.',
     'For this release\'s controls, see "How to play" in this menu.'],
]
NOTICE = [
    ['< Notice >'],
    ['Because this game faithfully recreates the original app,',
     'some menus or buttons may appear that do not work',
     '(e.g. "WEB (Site)", "Catalog", "Backlight").'],
    ['Help text may also mention communication charges,',
     'but this game does not incur any such charges.'],
]


def main():
    os.makedirs(DST, exist_ok=True)
    key_page('howtoplay_keyguide_steam_00', 'Controls',
             [(50, 'START Button'), (50, 'A Button'), (50, 'B Button'), (98, 'Stick / D-Pad'), None])
    key_page('howtoplay_keyguide_steam_01', 'Keyboard Controls', [None] * 5)
    text_page('howtoplay_keyguide_steam_02', 55, ABOUT)
    text_page('howtoplay_keyguide_steam_03', 55, NOTICE)
    print('guide pages written')


if __name__ == '__main__':
    main()
