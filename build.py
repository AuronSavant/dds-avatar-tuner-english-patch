"""Build and install the English patch.

    python build.py [--game DIR]              build everything and install into the game
    python build.py [--game DIR] --text       only rebuild the text/image data files
    python build.py [--game DIR] --uninstall  restore the original game

DIR is the folder containing avatartuner.exe (default: ../game). On first run the
original resources are extracted from that game into backup/ (see tools/extract.py).

Sources:
    translation/text_en_src.py   1390 UI/data strings
    translation/story_part*.py   story script
    tools/images.py, guide.py    sprite labels / archive guide pages
"""
import json, os, shutil, struct, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.join(os.path.dirname(ROOT), 'game')
if '--game' in sys.argv:
    GAME = os.path.abspath(sys.argv[sys.argv.index('--game') + 1])
DATA = os.path.join(GAME, 'avatartuner_Data')
MANAGED = os.path.join(DATA, 'Managed')
OUT = os.path.join(DATA, 'StreamingAssets', 'english')
# MSBuild cannot cope with the apostrophe in the game folder name, so compile in a temp dir
BUILD = os.path.join(tempfile.gettempdir(), 'ddsa_en_build')
BACKUP = os.path.join(ROOT, 'backup')
TR = os.path.join(ROOT, 'translation')

sys.path.insert(0, os.path.join(ROOT, 'tools'))
sys.path.insert(0, TR)
import textfmt  # noqa: E402


def ensure_extracted():
    if not os.path.exists(os.path.join(BACKUP, 'outt_b.orig')):
        import extract
        extract.main(GAME)


def run(*cmd):
    print('>', ' '.join(os.path.basename(c) if os.sep in c else c for c in cmd))
    subprocess.run(cmd, check=True)


def build_code():
    os.makedirs(BACKUP, exist_ok=True)
    orig = os.path.join(BACKUP, 'Assembly-CSharp.dll')
    if not os.path.exists(orig):
        shutil.copy2(os.path.join(MANAGED, 'Assembly-CSharp.dll'), orig)
    ref = os.path.join(BUILD, 'ref')
    os.makedirs(ref, exist_ok=True)
    for f in os.listdir(MANAGED):
        if f.endswith('.dll') and f not in ('Assembly-CSharp.dll', 'DDSA_EN.dll'):
            shutil.copy2(os.path.join(MANAGED, f), ref)
    shutil.copy2(orig, os.path.join(ref, 'Assembly-CSharp.dll'))
    src = os.path.join(BUILD, 'src')
    shutil.copytree(os.path.join(ROOT, 'tools'), src, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns('bin', 'obj', '__pycache__'))
    patcher_proj = os.path.join(src, 'Patcher', 'Patcher.csproj')
    patcher_out = os.path.join(BUILD, 'patcher')
    run('dotnet', 'build', patcher_proj, '-c', 'Release', '-o', patcher_out, '-nologo', '-v', 'q')
    patcher = os.path.join(patcher_out, 'Patcher.dll')
    run('dotnet', patcher, 'publicize', os.path.join(ref, 'Assembly-CSharp.dll'),
        os.path.join(ref, 'Assembly-CSharp.public.dll'))
    hooks_out = os.path.join(BUILD, 'hooks')
    run('dotnet', 'build', os.path.join(src, 'Hooks', 'DDSA_EN.csproj'), '-c', 'Release',
        '-o', hooks_out, '-nologo', '-v', 'q', '-p:ManagedDir=' + ref)
    hooks = os.path.join(hooks_out, 'DDSA_EN.dll')
    # input from ref/ so Cecil can resolve the Unity assemblies; write to temp, then install
    patched = os.path.join(BUILD, 'Assembly-CSharp.patched.dll')
    run('dotnet', patcher, 'patch', os.path.join(ref, 'Assembly-CSharp.dll'), hooks, patched)
    shutil.copy2(patched, os.path.join(MANAGED, 'Assembly-CSharp.dll'))
    shutil.copy2(hooks, os.path.join(MANAGED, 'DDSA_EN.dll'))


def load(name):
    with open(os.path.join(TR, name), encoding='utf-8') as f:
        return json.load(f)


def build_text():
    import text_en_src, story_en_src
    for mod in (text_en_src, story_en_src):
        missing = mod.build()
        if missing:
            print('warning: %d untranslated lines in %s' % (len(missing), mod.__name__))
    os.makedirs(OUT, exist_ok=True)
    # text_b (UI / data strings + event bytecode tail)
    ja_bin = open(os.path.join(BACKUP, 'text_b.orig'), 'rb').read()
    ja, tail = textfmt.read_textmod(ja_bin)
    en = load('text_en.json')
    assert len(en) == len(ja), (len(en), len(ja))
    strs = [e if e is not None else j for e, j in zip(en, ja)]
    open(os.path.join(OUT, 'text_b'), 'wb').write(textfmt.write_textmod(strs, tail))
    # outt_b (story)
    head, blocks = textfmt.read_outt(open(os.path.join(BACKUP, 'outt_b.orig'), 'rb').read())
    story = load('story_en.json')
    assert len(story) == len(blocks)
    out = []
    for bi, (eb, jb) in enumerate(zip(story, blocks)):
        assert len(eb) == len(jb), ('block', bi, len(eb), len(jb))
        out.append([e if e is not None else j for e, j in zip(eb, jb)])
    open(os.path.join(OUT, 'outt_b'), 'wb').write(textfmt.write_outt(head, out))
    # image pack and archive guide pages
    import images, guide
    images.main()
    guide.main()
    png = os.path.join(ROOT, 'images', 'png')
    if os.path.exists(png):
        shutil.copy2(png, os.path.join(OUT, 'png'))
    howto = os.path.join(ROOT, 'images', 'howto')
    if os.path.isdir(howto):
        shutil.copytree(howto, os.path.join(OUT, 'howto'), dirs_exist_ok=True)
    print('data files written')


def uninstall():
    orig = os.path.join(BACKUP, 'Assembly-CSharp.dll')
    if os.path.exists(orig):
        shutil.copy2(orig, os.path.join(MANAGED, 'Assembly-CSharp.dll'))
    for p in (os.path.join(MANAGED, 'DDSA_EN.dll'),):
        if os.path.exists(p):
            os.remove(p)
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    print('original game restored')


if __name__ == '__main__':
    if '--uninstall' in sys.argv:
        uninstall()
    else:
        ensure_extracted()
        if '--text' not in sys.argv:
            build_code()
        build_text()
