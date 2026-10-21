"""English source for text_b (UI / data string table). Run to regenerate text_en.json.

Index = entry number in text_ja.json. Entries not listed keep the Japanese original
(only used for things that are already ASCII: numbers, floors, sprite labels).
Space budget: menu labels <= ~16 chars, help/description boxes ~3 lines of ~24 chars.
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
JA = json.load(open(os.path.join(HERE, 'text_ja.json'), encoding='utf-8'))
T = {}

def put(start, *items):
    for i, s in enumerate(items):
        T[start + i] = s

# --- system / title / menus -------------------------------------------------
put(0, 'Quit', 'Menu', 'Back', 'Next', 'Start', 'Retry', 'Rank')
# 7: line-break exemption characters (kinsoku list) - keep as is
put(11, 'Yes', 'No')
put(17, 'Volume 1', 'Volume 2', 'Volume 3', 'Volume 4')
put(21, '-- No Data --', 'Overwrite the save file. Is that OK?', 'Game saved.')
put(32, 'Quick Load', 'Load')
put(34, 'Start a new game.', 'Continue from your last save.', 'Change game settings.',
    'Quit the game.', 'Carry over data from the subscription version.',
    'Connect to Megaten Alpha.', 'Resume from your Quick Save.',
    'Resume from your last Karma Terminal save.')
put(42, 'Skill', 'Item', 'Set', 'Mantra', 'Status', 'Config', 'Quick Save',
    'Use a skill.', 'Use items and check key items.',
    'Equip learned skills to make them usable.', 'View Mantra status.',
    'View character status.', 'Change game settings.',
    'Make a temporary save to take a break.', 'To Title')
put(57, 'BGM', 'Sound FX', 'Vibration', 'Return to the title screen.',
    'Turn music ON/OFF.', 'Turn sound effects ON/OFF.', 'Turn vibration ON/OFF.',
    '--- Remove ---', 'Remove an equipped skill.',
    'Physical Skills', 'Magic Skills', 'Wait Skills', 'Auto Skills',
    'Strong: Ice / Weak: Fire', '', 'Strong: Earth / Weak: Force', '',
    'Strong: Fire / Weak: Ice', '')
put(76, 'Save', 'Get Mantra', 'Transfer', 'Recover', 'Quit',
    'Save your data.', 'Obtain Mantras.', 'Travel between Karma Terminals.',
    'Restore HP/MP and status.', 'Leave the terminal.',
    '-- Unknown --', 'Already equipped.', 'Already mastered.',
    'Requirements not met.', '',
    'Purchase it. Is that OK?', '<BR>Download this Mantra?',
    ' switched from ', '<BR>to ', '.')
put(96, 'Buy', 'Sell', 'Quit', 'Purchase items.', 'Sell your items.',
    'Leave the vendor.', 'x', 'Owned ', 'Item', 'Price',
    'Purchase it. Is that OK?', 'Sell it. Is that OK?',
    'Nothing was found.', ' obtained.',
    'A strange object sits here. Touch it?',
    'An eerie object is floating here. Touch it?',
    'Save carry-over data? Existing data will be overwritten.',
    'Saved.', '', '', ' <BR>Saving failed.<BR>Retry?', 'Saving...',
    'Cannot read carry-over data. Create game data in the latest '
    'subscription version first, then carry it over.',
    'External Memory', 'Device open error', 'File access error',
    'File creation error', 'File deletion error', 'File write error',
    'File read error', 'File search error', 'File size error',
    'File capacity error', 'Error', 'Avatar Tuner',
    'About 2MB of data files will be downloaded. Check your free space first.',
    'Data will be updated, so the files will be downloaded again.',
    'Download complete. Please restart the app.', '', '',
    'Connecting...', 'Saving...',
    'An error occurred.<BR>Please restart the app.',
    'Could not connect.<BR>Retry?',
    'Check your connection and restart.',
    'Failed to save the file. You may be out of space.<BR> <BR>Retry?',
    'Member authentication error. Check your registration or connection settings.',
    'Could not connect. Restart somewhere with a signal.', '',
    'Sending save data...<BR> <BR>Please wait.', 'Save data registered.',
    'Could not connect. Try again somewhere with a signal.', '',
    'The app has been updated. Check the site for details.', '', '', '')
# item effect tags
put(153, '[HP Full]', '[HP+', ']', '[MP Full]', '[MP+', ']', '[Cure All]',
    '[', ' Cured]', '[', ']', '[', ' Up', ']', '[', '+', ']')
put(180, 'Level rose to ', '!', 'Learned ', '!', 'Sword level rose to ', '!',
    'Obtained ', '!')
put(188, 'Max HP', 'Max MP', 'Damage', 'Max Damage', 'Hit Rate', 'Spell Rate')
# battle
put(194, 'Hunt', 'Skill', 'Item', 'Escape', 'Pass',
    'Light physical damage to one foe.', 'Use a skill.', 'Use an item.',
    'Flee from battle.', 'End your action using a little of the gauge.',
    'Lead me from the unreal to the real,', 'from darkness to light,',
    'from death to immortality...',
    'Waiting', 'Not enough MP!', 'Not enough HP!', ': ', '', 'Sealed!',
    'Escape failed!', '[', ']', 'LV', 'LV--', '/', 'HP ', 'HP ----/----',
    'MP ', 'MP ----/----', '-Skills-', '-Affinity-', 'Strong', 'Weak', 'Player')
# ailments
put(228, 'Down', 'Berserk', 'Bat', 'Stone', 'Curse', 'Charm', 'Paralyze',
    'Poison', 'Ache', 'Confuse', 'Mute', 'Sleep', 'Freeze', 'Shock', 'Fear',
    'Normal', 'Guard')
# attributes / affinities
put(251, 'All Ail', 'Phys', 'Gun', 'Hunt', 'Fire', 'Ice', 'Elec', 'Force',
    'Earth', 'Almighty', 'Expel', 'Death', 'Charm', 'Poison', 'Mute',
    'Confuse', 'Nerve', 'Heal', 'Support', 'Special', 'None')
put(276, 'Magic', 'All Elem', 'All Ail', 'All NB', 'Normal', 'Normal OFF',
    'Weak', 'Weak OFF', 'Null', 'Drain', 'Repel')
put(289, 'Normal', 'Event', 'Boss')
put(293, 'Asura', 'Mitama', 'Flier', 'Dragon', 'Beast', 'Fiend', 'Deity',
    'Oni', 'Kishin', 'Onmyo')
put(308, 'Test Terminal')

# --- items --------------------------------------------------------------------
ITEMS = {
    'レーション': 'Ration', 'チャクラチップ': 'Chakra Chip', 'ランチアビーズ': 'Lancia Bead',
    'ディスポイズン': 'Dis-Poison', 'ディスエイク': 'Dis-Ache', 'パナシーア': 'Panacea',
    'デビルセル': 'Devil Cell', 'アニマトセル': 'Animato Cell', 'タグリング': 'Tag Ring',
    'インフェレスセル': 'Inferless Cell', 'エラッタセル': 'Errata Cell',
    'オーガニックセル': 'Organic Cell', 'クォンタムセル': 'Quantum Cell',
    'クリプトセル': 'Crypto Cell', 'コンプレスセル': 'Compress Cell',
    'ヒーホーセル': 'Hee-Ho Cell', 'レイヤーセル': 'Layer Cell', 'ロジックセル': 'Logic Cell',
    '（空白）': '(Blank)', '英雄のレーション': 'Hero Ration',
    'グラヴァンの欠片': 'Gravan Shard', 'グラヴァンの石像': 'Gravan Statue',
    'グレイトチャクラ': 'Great Chakra', 'ソーマ': 'Soma', 'ソーマドロップ': 'Soma Drop',
    'チャクラ金剛丹': 'Chakra Elixir', 'チャクラボックス': 'Chakra Box',
    'メディカルキット': 'Medical Kit', '烈士のレーション': 'Warrior Ration',
    'ガボアットボム': 'Gaboat Bomb', 'ファイアウォール': 'Fire Wall',
    'ファイアスタータ': 'Fire Starter', 'アル・アジフ': 'Al Azif', '殺生石': 'Killing Stone',
    'ダークファイバ': 'Dark Fiber', 'ウィンドウォール': 'Wind Wall',
    'サイクロンボム': 'Cyclone Bomb', 'ソニックストーン': 'Sonic Stone',
    'ランチアオーブ': 'Lancia Orb', 'ランチアジュエル': 'Lancia Jewel',
    'クエイクアームズ': 'Quake Arms', 'グランドウォール': 'Ground Wall',
    'グランドウォ－ル': 'Ground Wall', 'マグナスボム': 'Magnus Bomb',
    'ディスカース': 'Dis-Curse', 'ディスクローズ': 'Dis-Mute', 'ディストーン': 'Dis-Stone',
    'ディスパライズ': 'Dis-Paralyze', 'デカジャストーン': 'Dekaja Stone',
    'カンデオンボム': 'Candeon Bomb', 'サンダーウォール': 'Thunder Wall',
    'サンダーロッド': 'Thunder Rod', '万里の望遠鏡': 'Far Telescope',
    'マジックミラー': 'Magic Mirror', 'エンジェルアロウ': 'Angel Arrow',
    'ＨＰノイズ': 'HP Noise', 'ＭＰノイズ': 'MP Noise', 'クイックノイズ': 'Quick Noise',
    'バイタルノイズ': 'Vital Noise', 'パワーノイズ': 'Power Noise',
    'マジックノイズ': 'Magic Noise', 'ラックノイズ': 'Luck Noise',
    'メギドファイア': 'Megido Fire', 'ワイルドカード': 'Wild Card', 'ワイルドボム': 'Wild Bomb',
    'アイスボール': 'Ice Ball', 'フリーズウォール': 'Freeze Wall',
    'ブリザトンボム': 'Blizzaton Bomb', 'フィジカルミラー': 'Physical Mirror',
    'ブラックパール': 'Black Pearl', 'ホワイトパール': 'White Pearl', 'レッドルビー': 'Red Ruby',
    '認証カルマリング': 'Karma ID Ring', '蛇の形の鍵': 'Serpent Key', '叢雲の鈴': 'Murakumo Bell',
    '秘密の部屋の鍵': 'Secret Room Key', '蒼いトルコ石': 'Blue Turquoise',
    '大天使の羽': 'Archangel Wing', 'アオダンゴ': 'Blue Dango',
    'スメルグレイビー': 'Smelly Gravy', 'マッスルドリンコ': 'Muscle Drink',
    'ミステリーフード': 'Mystery Food', 'エストマスプレー': 'Estoma Spray',
    'リベラマフルート': 'Liberama Flute', 'バイオレンス': 'Violence',
    'ギガバイオレンス': 'Giga Violence', '破魔リフレクト': 'Expel Reflect',
    '------------': '------------',
}
for i in range(438, 521):
    if JA[i] in ITEMS:
        T[i] = ITEMS[JA[i]]
for i in range(942, 1001):
    if JA[i] in ITEMS:
        T[i] = ITEMS[JA[i]]

put(522,
    'Restores 50 HP to one ally.',
    'Restores 50 MP to one ally.',
    'Revives one ally with a little HP. Battle only.',
    'Cures Poison on one ally.',
    'Cures Ache on one ally.',
    'Cures Confuse, Charm and Sleep on one ally. Battle only.',
    'Can be sold for money.', 'Can be sold for money.',
    'Ring that records battle points. Every Junkyard soldier carries one.',
    *['Can be sold for money.'] * 9,
    '(Blank)',
    'Restores 300 HP to one ally.',
    'Dia effect on one ally. Unlimited uses.',
    'Diarama effect on one ally. Unlimited uses.',
    'Fully restores MP of all allies.',
    '(Blank)',
    'Fully restores HP and MP of all allies.',
    'Fully restores HP and MP of one ally.',
    'Restores 50 MP to one ally. Unlimited uses.',
    'Restores 150 MP to one ally.',
    '(Blank)', '(Blank)',
    'Restores 150 HP to all allies.',
    'Restores 150 HP to one ally.',
    'Fire attack on all foes. Power B.',
    'Nullifies Fire for all allies for 1 turn.',
    'Fire attack on all foes. Power C.',
    'Death attack on all: instant kill. Unlimited uses.',
    'Death attack on all: high-rate instant kill. Unlimited.',
    'Death attack on all: instant kill.',
    'Nullifies Force for all allies for 1 turn.',
    'Force attack on all foes. Power B.',
    'Force attack on all foes. Power C.',
    'Revives one ally with full HP. Unlimited. Battle only.',
    'Revives one ally with full HP. Battle only.',
    'Earth attack on all foes. Power C.',
    'Nullifies Earth for all allies for 1 turn.',
    'Earth attack on all foes. Power B.',
    'Cures Curse on one ally.',
    'Cures Mute on one ally.',
    'Cures Stone on one ally.',
    'Cures Paralyze on one ally.',
    'Cancels all foes\' -kaja buffs.',
    'Elec attack on all, may Shock. Power B.',
    'Nullifies Elec for all allies for 1 turn.',
    'Elec attack on all foes, may Shock. Power C.',
    '(Blank)',
    'Devil Analyze on one foe. Unlimited uses.',
    'Reflects magic for all allies for 1 turn.',
    '(Blank)',
    'Expel attack on all foes.',
    'One ally: Max HP +10, full HP/MP restore.',
    'One ally: Max MP +10, full HP/MP restore.',
    'One ally: Agility +2, full HP/MP restore.',
    'One ally: Vitality +2, full HP/MP restore.',
    'One ally: Strength +2, full HP/MP restore.',
    'One ally: Magic +2, full HP/MP restore.',
    'One ally: Luck +2, full HP/MP restore.',
    'Almighty attack on all foes. Power B. Unlimited.',
    'Almighty attack on all foes. Power C.',
    'Almighty attack on all foes. Power B.',
    'Ice attack on all foes, may Freeze. Power C.',
    'Nullifies Ice for all allies for 1 turn.',
    'Ice attack on all foes, may Freeze. Power B.',
    'Reflects physical attacks for all allies for 1 turn.',
    'Black orb. Proof of Genbu\'s defeat. Gather all 4 orbs...',
    'White orb. Proof of Byakko\'s defeat. Gather all 4 orbs...',
    'Red orb. Proof of Suzaku\'s defeat. Gather all 4 orbs...',
    'Karma Temple ring. Its ID code works elevators and terminals.',
    'A key whose serpent eyes glow eerily. It opens some room.',
    'A mystic key engraved with clouds veiling the moon.',
    'A key shaped like a tangled puzzle ring. It opens some room.',
    'Blue orb. Proof of Seiryu\'s defeat. Gather all 4 orbs...',
    'Proof of Metatron\'s defeat. Holy power dwells in it.')

# --- mantras ------------------------------------------------------------------
MANTRA = ['Frost', 'Earth', 'Queen', 'Guardian', 'Devour', 'Hero', 'Arcane', 'Blaze',
          'Volt', 'Wyvern', 'Yaksha', 'Angel', 'General', 'Demon', 'Wrath', 'Spirit',
          'Evil']
for g, rank in enumerate('CBA'):
    for k, name in enumerate(MANTRA):
        T[605 + g * 17 + k] = '%s Mantra %s' % (name, rank)
T[604] = '------------ '
UNLOCK = ['Ice magic', 'Earth magic', 'all-target', 'healing magic', 'Hunt & physical',
          'curing magic', 'special', 'Fire magic', 'Elec magic', 'Force magic',
          'Death magic', 'Expel magic', 'Almighty magic', 'buff magic', 'defense magic',
          'support magic', 'ultimate magic']
for g in range(3):
    for k, u in enumerate(UNLOCK):
        T[657 + g * 17 + k] = 'Unlocks %s skills.' % u

# --- skills ---------------------------------------------------------------------
SK = {
    '狩る': 'Hunt', 'ブフ': 'Bufu', 'マハブフ': 'Mabufu', 'テラ': 'Tera', 'マハテラ': 'Matera',
    'ディア': 'Dia', 'メディア': 'Media', 'パトラ': 'Patra', 'ポズムディ': 'Posumudi',
    'エイクディ': 'Akedi', '喰らいつき': 'Bite', '喰い散らし': 'Scatter Feast',
    'デビルアナライズ': 'Devil Analyze',
    'アギ': 'Agi', 'マハラギ': 'Maragi', 'アギラオ': 'Agilao', 'マハラギオン': 'Maragion',
    'アギダイン': 'Agidyne', 'マハラギダイン': 'Maragidyne', '灼熱ブレス': 'Scorch Breath',
    'ブフーラ': 'Bufula', 'マハブフーラ': 'Mabufula', 'ブフダイン': 'Bufudyne',
    'マハブフダイン': 'Mabufudyne', '極寒ブレス': 'Frigid Breath', '大冷界': 'Ice Age',
    'ジオ': 'Zio', 'マハジオ': 'Mazio', 'ジオンガ': 'Zionga', 'マハジオンガ': 'Mazionga',
    'ジオダイン': 'Ziodyne', 'マハジオダイン': 'Maziodyne', '雷起': 'Thunder Call',
    'ザン': 'Zan', 'マハザン': 'Mazan', 'ザンマ': 'Zanma', 'マハザンマ': 'Mazanma',
    'ザンダイン': 'Zandyne', 'マハザンダイン': 'Mazandyne', 'カマイタチ': 'Kamaitachi',
    'テラジ': 'Terazi', 'マハテラジ': 'Materazi', 'テラダイン': 'Teradyne',
    'マハテラダイン': 'Materadyne', '岩責め': 'Stone Press',
    'ムド': 'Mudo', 'マハムド': 'Mamudo', 'ムドオン': 'Mudoon', 'マハムドオン': 'Mamudoon',
    '石化光線': 'Petrify Ray', '呪いの言霊': 'Cursed Word', 'カースエピタフ': 'Curse Epitaph',
    'ハマ': 'Hama', 'マハンマ': 'Mahama', 'ハマオン': 'Hamaon', 'マハンマオン': 'Mahamaon',
    'ザナドゥ': 'Xanadu', 'ロストワード': 'Lost Word',
    'メギド': 'Megido', 'メギドラ': 'Megidola', 'メギドラオン': 'Megidolaon',
    '太極光輪': 'Taiji Halo', '魔法リフレクト': 'Magic Reflect',
    'フルデストロイア': 'Full Destroia', '色即是空': 'Form Is Void',
    '終わる世界': "World's End", 'シナイの神火': 'Fire of Sinai',
    '死蝿の葬列': 'Death Flies', '体力泥棒': 'Life Thief',
    'ディアラマ': 'Diarama', 'メディラマ': 'Mediarama', 'ディアラハン': 'Diarahan',
    'メディアラハン': 'Mediarahan', 'リカーム': 'Recarm', 'サマリカーム': 'Samarecarm',
    'リカームドラ': 'Recarmdra', 'メシアライザー': 'Messiah Riser',
    'オートソーマ': 'Auto Soma', 'パララディ': 'Paraladi', 'メパトラ': 'Mepatra',
    'クロズディ': 'Klosedi', 'カースディ': 'Cursedi', 'ペトラディ': 'Petradi',
    'ＢＳデストロイア': 'Ailment Destroia',
    'タルンダ': 'Tarunda', 'スクンダ': 'Sukunda', 'ラクンダ': 'Rakunda',
    'マカトラ': 'Makatora', 'マカンダ': 'Makanda', 'プリンパ': 'Pulinpa',
    'マカジャマ': 'Makajama', 'ドルミナー': 'Dormina', 'タルカジャ': 'Tarukaja',
    'マリンカリン': 'Marin Karin', 'ラクカジャ': 'Rakukaja', 'スクカジャ': 'Sukukaja',
    'マカジャマオン': 'Makajamaon', 'マカカジャ': 'Makakaja', 'デカジャ': 'Dekaja',
    'デクンダ': 'Dekunda', 'ランダマイザ': 'Debilitate',
    'まるかじり': 'Chomp', '鬼喰い': 'Oni Eater', 'まる呑み': 'Swallow Whole',
    '暴飲暴食': 'Gluttony', '大嘗祭': 'Great Feast', '最後の晩餐': 'Last Supper',
    '地獄突き': 'Hell Thrust', '大毒牙': 'Great Venom Fang', 'ヘルファング': 'Hell Fang',
    '心の叫び': "Heart's Cry", 'バイオクロウ': 'Bio Claw', 'マッスルボンバー': 'Muscle Bomber',
    '毒針': 'Poison Sting', '乱心の一刀': 'Frenzy Slash', '昏睡ステップ': 'Coma Step',
    '痺れ針': 'Stun Needle', '悩殺スラッシュ': 'Seductive Slash', '桜花閃乱': 'Blossom Flurry',
    'アカシックバリツ': 'Akashic Baritsu', 'デスシャワー': 'Death Shower',
    '紅蓮剣': 'Crimson Blade', 'パワーウェイヴ': 'Power Wave', '黙殺': 'Silent Kill',
    '脳天割り': 'Skull Splitter', '血祭り': 'Bloodbath', 'ズンバラリン': 'Zunbararin',
    '鉄死拳': 'Iron Death Fist', '大屠殺': 'Massacre', 'ギロチンクロウ': 'Guillotine Claw',
    'デモンレイヴ': 'Demon Rave', '黙示録': 'Apocalypse', '冥界の門': 'Gate of Hades',
    '物理アブソーバ': 'Phys Absorber',
    '催眠ガス': 'Hypno Gas', '痺れ玉': 'Stun Ball', '痺れ大波動': 'Stun Wave',
    '大往生': 'Eternal Rest', '有害吐息': 'Toxic Breath', '怪音波': 'Eerie Sound',
    'テンタラフー': 'Tentarafoo', '極上の肉体': 'Perfect Body', '魔力泥棒': 'Mana Thief',
    '逃走アクセラ': 'Escape Accel', 'アボイﾄﾞスリーパ': 'Avoid Sleeper',
    'マインドチャージ': 'Mind Charge', 'マスタキャンセラ': 'Master Canceler',
    'ストマックガード': 'Stomach Guard', 'クリティカ': 'Critica',
    '会心キャンセラ': 'Crit Canceler', '代謝アクセラ': 'Metabolic Accel',
    'デスキャンセラ': 'Death Canceler', 'ＭＩＮクリティカ': 'MIN Critica',
    'ＭＡＸクリティカ': 'MAX Critica', '挑発': 'Provoke', 'カウンタ': 'Counter',
    'パワーカウンタ': 'Power Counter', 'ハイパーカウンタ': 'Hyper Counter',
    '先制エキスパンダ': 'First Strike Up', 'パワーチャージ': 'Power Charge',
    'オールアタッカ': 'All Attacker', 'フルスペキュトラ': 'Full Specutra',
    'チャクラウォーカ': 'Chakra Walker', 'ハッピーウォーカ': 'Happy Walker',
    'ＭＰブースタ': 'MP Booster', 'ＭＰハイブースタ': 'MP Hi-Booster',
    'ＭＰメガブースタ': 'MP Mega Booster', 'ＭＰテイスタ': 'MP Taster',
    'ＭＰハイテイスタ': 'MP Hi-Taster', 'ＨＰブースタ': 'HP Booster',
    'ＨＰハイブースタ': 'HP Hi-Booster', 'ＨＰメガブースタ': 'HP Mega Booster',
    'カルマゲッタ': 'Karma Getter', 'フルカルマゲッタ': 'Full Karma Getter',
    'ＡＰブースタ': 'AP Booster', 'ＡＰディバイダ': 'AP Divider',
}
ELEM = {'火炎': 'Fire', '氷結': 'Ice', '電撃': 'Elec', '衝撃': 'Force', '地変': 'Earth',
        '呪殺': 'Death', '破魔': 'Expel', '物理': 'Phys', '神経': 'Nerve', '猛毒': 'Poison',
        '混乱': 'Confuse', '魅了': 'Charm', '魔封': 'Mute'}
SUFFIX = {'ブレイク': '%s Break', 'ブースタ': '%s Booster', 'リフレクト': '%s Reflect',
          'ドレイン': '%s Drain', 'ハイブースタ': '%s Hi-Booster', 'ストロンガ': '%s Stronger',
          'デストロイア': '%s Destroia', 'スペキュラ': '%s Specula'}
for i in range(709, 1001):
    j = JA[i]
    if j in SK:
        T[i] = SK[j]
    elif j in ITEMS:
        T[i] = ITEMS[j]
    elif j == '':
        T[i] = ''
    else:
        for e, en in ELEM.items():
            if j.startswith(e) and j[len(e):] in SUFFIX:
                T[i] = SUFFIX[j[len(e):]] % en
                break
        if j == 'フルカルマゲッタ':
            T[i] = 'Full Karma Get'

# --- skill descriptions (pattern based) --------------------------------------------
SIZE = {'小': 'light', '中': 'medium', '大': 'heavy', '特大': 'severe', '超特大': 'colossal'}
EL = dict(ELEM, 万能='Almighty')
AIL = {'猛毒': 'Poison', '麻痺': 'Paralyze', '混乱': 'Confuse', '睡眠': 'Sleep', '魅了': 'Charm',
       '呪い': 'Curse', '魔封': 'Mute', '石化': 'Stone', '氷結': 'Freeze', '感電': 'Shock'}

def who(s):
    return {'敵単体': 'one foe', '敵全体': 'all foes', '味方単体': 'one ally',
            '味方全体': 'all allies', '単体': 'one target', '全体': 'all targets'}[s]

def desc(j):
    s = j.replace('<BR>', '')
    m = re.fullmatch(r'(敵単体|敵全体)に(\S\S)属性の(小|中|大|特大|超特大)ダメージ'
                     r'(?:＆(\S\S)効果)?(?:更に低確率で(\S\S)効果)?(残りＨＰで威力変化)?'
                     r'(クリティカル率が高い)?(人間には効かない)?', s)
    if m:
        out = '%s %s damage to %s' % (SIZE[m[3]].capitalize(), EL[m[2]], who(m[1]))
        if m[4]: out += ' + %s' % AIL[m[4]]
        if m[5]: out += '. May %s' % AIL[m[5]]
        out += '.'
        if m[6]: out += ' Scales with HP left.'
        if m[7]: out += ' High crit rate.'
        if m[8]: out += ' No effect on humans.'
        return out
    m = re.fullmatch(r'(敵単体|敵全体)に(\S\S)属性の(\S\S)効果', s)
    if m: return '%s %s on %s.' % (EL[m[2]], AIL.get(m[3], m[3]), who(m[1]))
    m = re.fullmatch(r'味方全体に(\S\S)(無効|反射|吸収)バリアを張る', s)
    if m: return 'Shields all allies: %s %s.' % ({'無効': 'nullify', '反射': 'reflect', '吸収': 'absorb'}[m[2]], EL.get(m[1], m[1]))
    m = re.fullmatch(r'(\S\S)属性攻撃の威力が(大幅)?アップ', s)
    if m: return '%s %s attack power.' % ('Greatly raises' if m[2] else 'Raises', EL[m[1]])
    m = re.fullmatch(r'(\S\S)属性の攻撃に強くなり弱点も打ち消す|(\S\S)属性の攻撃を受けにくくなり弱点も打ち消す', s)
    if m: return 'Resist %s and remove that weakness.' % EL[m[1] or m[2]]
    m = re.fullmatch(r'(\S\S)属性の攻撃を(無効にする|反射する|吸収する)', s)
    if m: return {'無効にする': 'Nullifies', '反射する': 'Reflects', '吸収する': 'Absorbs'}[m[2]] + ' %s attacks.' % EL[m[1]]
    m = re.fullmatch(r'(味方単体|味方全体)の(\S\S)を治療', s)
    if m: return 'Cures %s on %s.' % (AIL[m[2]] if m[2] != '腹痛' else 'Ache', who(m[1]))
    m = re.fullmatch(r'(味方単体|味方全体)のＨＰを(小|中|全)回復', s)
    if m: return {'小': 'Slightly restores', '中': 'Restores', '全': 'Fully restores'}[m[2]] + ' HP of %s.' % who(m[1])
    return None

for i in range(1002, 1291):
    j = JA[i]
    if j == '':
        T[i] = ''
        continue
    d = desc(j)
    if d: T[i] = d

DESC = {
    1002: 'Light physical damage to a foe.',
    1009: 'Cures Confuse, Charm and Sleep on one ally.',
    1012: 'Light-damage Hunt on one foe. Kill to gain AP.',
    1013: 'Light-damage Hunt on all foes. Kill to gain AP.',
    1014: 'Examine a defeated foe\'s data.',
    1030: 'Medium Fire damage to all foes.',
    1041: 'Medium Ice damage to all foes. May Freeze.',
    1042: 'Medium Ice damage to all foes.',
    1055: 'Medium Elec damage to all foes. May Shock.',
    1068: 'Medium Force damage to all foes.',
    1079: 'Medium Earth damage to all foes.',
    1080: 'Death: instant kill on one foe.',
    1081: 'Death: instant kill on all foes.',
    1082: 'Death: high-rate instant kill on one foe.',
    1083: 'Death: high-rate instant kill on all foes.',
    1084: 'Death: Stone on one foe.',
    1085: 'Death: Curse on one foe.',
    1086: 'Death: Curse on all foes.',
    1092: 'Expel: halves one foe\'s HP. No effect on humans.',
    1093: 'Expel: halves all foes\' HP. No effect on humans.',
    1094: 'Expel: slashes one foe\'s HP. No effect on humans.',
    1095: 'Expel: slashes all foes\' HP. No effect on humans.',
    1105: 'Severe Almighty damage + random ailment to all foes.',
    1106: 'Shields all allies: reflect magic.',
    1107: 'Nullifies Fire, Ice, Force, Elec and Earth.',
    1108: 'Almighty random ailment on all foes.',
    1109: 'Heavy Almighty damage to all foes + lowers defense.',
    1111: 'Severe Almighty damage + Death instant kill on all foes.',
    1112: 'Drains HP from one foe (Almighty).',
    1117: 'Revives one ally with a little HP. Battle only.',
    1118: 'Revives one ally with full HP. Battle only.',
    1119: 'Sacrifice self to fully restore and revive allies.',
    1120: 'Fully restores HP and cures ailments of all allies.',
    1121: 'Full HP/MP after battle. Participants only.',
    1123: 'Cures Confuse, Charm and Sleep on all allies.',
    1127: 'Nullifies Nerve, Charm, Mute and Confuse.',
    1128: 'Lowers all foes\' attack.',
    1129: 'Lowers all foes\' agility.',
    1130: 'Lowers all foes\' defense.',
    1131: 'Gives 50 MP to one ally. Battle only.',
    1132: 'Lowers all foes\' magic attack.',
    1133: 'Confuse on one foe.',
    1134: 'Mute (seal magic) on one foe.',
    1135: 'Nerve: Sleep on all foes.',
    1136: 'Raises all allies\' attack.',
    1137: 'Charm on one foe.',
    1138: 'Raises all allies\' defense.',
    1139: 'Raises all allies\' agility.',
    1140: 'Mute (seal magic) on all foes.',
    1141: 'Raises all allies\' magic power.',
    1142: 'Cancels all foes\' -kaja buffs.',
    1143: 'Cancels all allies\' -nda debuffs.',
    1144: 'Lowers all stats of all foes.',
    1145: 'Heavy-damage Hunt on one foe. Kill to gain AP.',
    1146: 'Low-rate instant-kill Hunt on one foe. Gain AP.',
    1147: 'High-rate instant-kill Hunt on one foe. Gain AP.',
    1148: 'Medium-damage Hunt on all foes. Kill to gain AP.',
    1149: 'Low-rate instant-kill Hunt on all foes. Gain AP.',
    1150: 'High-rate instant-kill Hunt on all foes. Gain AP.',
    1177: 'Absorbs physical attacks.',
    1183: 'Nerve: Sleep on one foe.',
    1184: 'Nerve: Paralyze on one foe.',
    1185: 'Nerve: Paralyze on all foes.',
    1188: 'Nerve: instant kill on a sleeping foe.',
    1192: 'Confuse on all foes.',
    1196: 'Charm on all foes.',
    1201: 'Drains MP from one foe (Mute).',
    1202: 'Makes escape easier when the user tries it.',
    1203: 'Dodge all attacks while asleep.',
    1204: 'Next attack spell deals over 2x damage.',
    1205: 'Nullifies all attacks except Almighty.',
    1206: 'Fully prevents Ache from a successful Hunt.',
    1207: 'Doubles critical rate of normal attacks (capped).',
    1208: 'Harder to receive critical hits.',
    1209: 'Raises ailment recovery rate each turn.',
    1210: 'Once per battle, likely survive a fatal blow.',
    1211: 'Not implemented.', 1212: 'Not implemented.',
    1213: 'Lowers all foes\' defense but raises their attack.',
    1214: 'Low chance to counter physical hits. Weak power.',
    1215: 'Average chance to counter physical hits. Medium power.',
    1216: 'High chance to counter physical hits. High power.',
    1217: 'Raises first-strike rate. Participants only.',
    1218: 'Next physical attack deals over 2x damage.',
    1219: 'Normal attacks hit all foes.',
    1220: 'Reflects Fire, Ice, Force, Elec and Earth.',
    1221: 'Regain MP while walking. Participants only.',
    1222: 'Regain lots of MP while walking. Participants only.',
    1223: 'Max MP +10%.', 1224: 'Max MP +20%.', 1225: 'Max MP +30%.',
    1226: 'Restore a little MP on a successful Hunt.',
    1227: 'Restore 50% MP on a successful Hunt.',
    1228: 'Max HP +10%.', 1229: 'Max HP +20%.', 1230: 'Max HP +30%.',
    1231: 'Gain 1/2 Karma even when not in battle.',
    1232: 'Gain Karma even when not in battle.',
    1233: 'More AP after battle. Participants only.',
    1234: 'Successful Hunts also give AP to allies.',
}
T.update(DESC)

# --- characters / enemies -------------------------------------------------------
NAMES = {
    'サーフ': 'Serph', 'アルジラ': 'Argilla', 'ヒート': 'Heat', 'ヴァルナ': 'Varna',
    'プリティヴィー': 'Prithivi', 'アグニ': 'Agni', 'ガキ': 'Gaki', 'ギュウキ': 'Gyuki',
    'ケルピー': 'Kelpie', 'スライム': 'Slime', 'ヤカー': 'Yaka', 'コカトライス': 'Cockatrice',
    'カルマ教会ガード': 'Temple Guard', 'ピクシー': 'Pixie', 'ゲンブ': 'Genbu',
    'スザク': 'Suzaku', 'ビャッコ': 'Byakko', 'セイリュウ': 'Seiryu', 'ベルゼブブ': 'Beelzebub',
    'メタトロン': 'Metatron', 'フレスベルグ': 'Hresvelgr', 'ユニコーン': 'Unicorn',
    'ブロブ': 'Blob', 'ナーガ': 'Naga', 'ブラックウーズ': 'Black Ooze', 'ホルス': 'Horus',
    'バフォメット': 'Baphomet', '枢密院議長シホン': 'Chancellor Sihon',
    '闇の軍団長オーグ': 'Dark Lord Ogue', 'アピス': 'Apis', 'トゥルダク': 'Turdak',
    'ジャックフロスト': 'Jack Frost', 'ジャックランタン': 'Jack Lantern', 'イソラ': 'Isora',
}
for i in range(1291, 1388):
    if JA[i] in NAMES: T[i] = NAMES[JA[i]]
    elif JA[i] == '': T[i] = ''
T[1388] = 'Their two souls shall wander forever...'
T[1389] = 'Nothing happens.'


def build():
    out = []
    missing = []
    for i, j in enumerate(JA):
        if i in T:
            out.append(T[i])
        else:
            out.append(None)
            if re.search('[぀-ヿ一-鿿！-～ｦ-ﾟ]', j) and i != 7 \
                    and not re.fullmatch('[Ａ-Ｚ ]+', j):
                missing.append(i)
    json.dump(out, open(os.path.join(HERE, 'text_en.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=0)
    return missing


if __name__ == '__main__':
    miss = build()
    print('untranslated:', len(miss))
    for i in miss:
        print(i, JA[i])
