# DIGITAL DEVIL SAGA Avatar Tuner A's TEST Server: English Patch

This is a fan translation of *G-MODE Archives+ DIGITAL DEVIL SAGA アバタール・チューナー A's TEST Server 完全版* (PC).

**No game data is included. You need your own copy of the game.** The build reads the original resources from your copy and writes the English versions next to them.

## What gets translated
- The full story script: 1,460 lines, every branch, through the ending.
- All 1,390 menu, item, skill, mantra, enemy and system strings. Names use the official Digital Devil Saga English terms.
- Japanese sprite labels: character names, stat labels, the Varna/Agni/Prithivi names, the vendor and Karma Terminal headings, and the mantra labels. These are redrawn with small pixel fonts.
- The archive wrapper: the title screen, the OPTION menu and the how-to-play pages.

The game wraps text one character at a time, which splits English words. The patch adds a hook that wraps dialogue and help boxes at whole words.

## Install
Requirements:
- Python 3.10+ with `pip install -r requirements.txt`
- The .NET SDK (8 or newer), used to build the small code patch

Put this folder next to the game's `game` folder, or pass `--game` with the folder that contains `avatartuner.exe`:

```
python build.py --game "D:\Games\DDSAT\game"
```

The first run backs up the original `Assembly-CSharp.dll` and extracts the resources the patch needs into `backup/`. It then installs:
- a patched `avatartuner_Data/Managed/Assembly-CSharp.dll`
- the new hook library `DDSA_EN.dll`
- the English data in `avatartuner_Data/StreamingAssets/english/`

The original asset bundles are never modified.

To uninstall:
```
python build.py --game "<game folder>" --uninstall
```

## How it works
- `tools/Patcher`: a Mono.Cecil tool that adds calls into `DDSA_EN.dll` to the game assembly.
- `tools/Hooks`: the runtime hooks. They load files from `StreamingAssets/english/` in place of the built-in resources (`text_b`, `outt_b`, `png`), replace the dialogue printer and the help-box wrapper with word-wrapping versions, and swap the wrapper's strings and how-to-play images to English.
- `tools/textfmt.py`: reads and writes the game's string-table and story-script containers.
- `tools/extract.py`: pulls the originals out of your copy of the game.

## Editing the translation
- UI and data strings: `translation/text_en_src.py`
- Story: `translation/story_part1.py` to `story_part3.py`, keyed `block.line` → English. Lines repeated in other branches are filled in automatically.
- Sprite labels: `tools/images.py`. Guide pages: `tools/guide.py`.

After editing, run `python build.py --text` to rebuild just the data.

DIGITAL DEVIL SAGA © ATLUS. G-MODE Archives © G-MODE Corporation. This is an unofficial fan project and is not affiliated with either company.
