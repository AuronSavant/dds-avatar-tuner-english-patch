"""Merge story_part*.py into story_en.json.

Each part maps "block.line" -> English for the first occurrence of a Japanese line;
identical Japanese lines elsewhere in the script get the same English automatically.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
JA = json.load(open(os.path.join(HERE, 'story_ja.json'), encoding='utf-8'))

S = {}
for name in ('story_part1', 'story_part2', 'story_part3'):
    S.update(__import__(name).S)

JP = re.compile('[぀-ヿ一-鿿！-～ｦ-ﾟ　-〿]')


def build():
    by_ja = {}
    for key, en in S.items():
        b, l = map(int, key.split('.'))
        j = JA[b][l]
        if j in by_ja and by_ja[j] != en:
            print('conflict', key, j)
        by_ja[j] = en
    out, missing = [], []
    for b, blk in enumerate(JA):
        ob = []
        for l, j in enumerate(blk):
            en = by_ja.get(j)
            if en is None and JP.search(j):
                missing.append('%d.%d %s' % (b, l, j))
            ob.append(en)
        out.append(ob)
    json.dump(out, open(os.path.join(HERE, 'story_en.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    return missing


if __name__ == '__main__':
    m = build()
    print('untranslated:', len(m))
    for x in m:
        print(x)
