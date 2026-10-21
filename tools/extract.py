"""Pull the original data the patch is built from out of your own copy of the game.

    python tools/extract.py <game folder containing avatartuner.exe>

Writes backup/ (original DLL, text/script/sprite resources, guide images) and
translation/text_ja.json + story_ja.json. Nothing here is shipped with the repo.
"""
import glob, json, os, shutil, sys

import UnityPy

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import textfmt  # noqa: E402

BACKUP = os.path.join(ROOT, 'backup')
GUIDE = ['howtoplay_keyguide_steam_00', 'howtoplay_keyguide_steam_01',
         'howtoplay_keyguide_steam_02', 'howtoplay_keyguide_steam_03']


def text_assets(bundle):
    out = {}
    for o in UnityPy.load(bundle).objects:
        if o.type.name == 'TextAsset':
            t = o.read()
            out[t.m_Name] = t.m_Script.encode('utf-8', 'surrogateescape')
    return out


def main(game):
    data = os.path.join(game, 'avatartuner_Data')
    bundles = os.path.join(data, 'StreamingAssets', 'aa', 'StandaloneWindows64')
    if not os.path.isdir(bundles):
        sys.exit('game data not found under ' + game)
    os.makedirs(os.path.join(BACKUP, 'howto'), exist_ok=True)

    dll = os.path.join(data, 'Managed', 'Assembly-CSharp.dll')
    target = os.path.join(BACKUP, 'Assembly-CSharp.dll')
    if not os.path.exists(target):
        if b'DDSA_EN' in open(dll, 'rb').read():
            sys.exit('Assembly-CSharp.dll is already patched; restore the original first')
        shutil.copy2(dll, target)

    res = text_assets(glob.glob(os.path.join(bundles, 'file_assets_all_*.bundle'))[0])
    for name, out in (('text_mod.bin', 'text_b.orig'), ('outt_b', 'outt_b.orig'), ('png', 'png.orig')):
        open(os.path.join(BACKUP, out), 'wb').write(res[name])

    for o in UnityPy.load(glob.glob(os.path.join(bundles, 'achiveui-guide_*.bundle'))[0]).objects:
        if o.type.name == 'Texture2D':
            t = o.read()
            if t.m_Name in GUIDE:
                t.image.save(os.path.join(BACKUP, 'howto', t.m_Name + '.png'))

    ja, _ = textfmt.read_textmod(res['text_mod.bin'])
    _, story = textfmt.read_outt(res['outt_b'])
    tr = os.path.join(ROOT, 'translation')
    json.dump(ja, open(os.path.join(tr, 'text_ja.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    json.dump(story, open(os.path.join(tr, 'story_ja.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('extracted originals to backup/')


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(ROOT), 'game'))
