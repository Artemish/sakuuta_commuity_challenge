import os
import sys
import re
import argparse
import pprint
import csv

name_dict = {
    # In VNDB Character list order
    # Protagonist
    '直哉': 'Naoya',
    # Main Characters
    '里奈': 'Rina',
    '稟': 'Rin',
    '藍': 'Ai',
    '雫': 'Shizuku',
    '真琴': 'Makoto',
    # Side Characters
    '小牧': 'Komaki',
    '小沙智': 'Kosachi',
    '明石': 'Akashi',
    '伯奇': 'Hakuki',
    'ノノ未': 'Nonomi',
    'ルリヲ': 'Ruriwo',
    '片貝': 'Katami',
    '鈴菜': 'Suzuna',
    '優美': 'Yuumi',
    '奈津子': 'Natsuko',
    '健一郎': "Ken'ichiro",
    'フリッドマン': 'Friedman',
    '香奈': 'Kana',
    '水菜': 'Mizuna',
    '義貞': 'Yoshisada',
    '圭': 'Kei',
    '琴子': 'Kotoko',
    '霧乃': 'Kirino',
    '寧': 'Nei',
    '咲崎': 'Sakizaki',
    '桜子': 'Sakurako',  # TODO: Does her name really change throught the novel??? I saw both
    '吹': 'Sui',
    'トーマス': 'Thomas',
    '紗希': 'Saki',
    '若田': 'Wakata',
    # Makes an appearance
    '琢磨': 'Takuma',
    # Not on VNDB
    '？？？': '???',
    '葛': 'Kuzu',
    '中村章一': "Sho'ichi Nakamura",
    '方相氏': 'Master of the Astral Square',
    '村山理事': 'Director Murayama',
    '丘沢': 'Okazawa',  # TODO: Who is this even? Check if name is correct
    '村田': 'Murata',
    '坂本': 'Sakamoto',
    '麗華': 'Reika',
    '御桜父親': "Rin's Father",
    '東浪見': 'Put name here later',  # TODO
    '一宮': 'Put name here later',  # TODO
    '中里': 'Put name here later',  # TODO
    '一同': 'Everyone',
    '中年': 'Old Man',
    '店主': 'Shopkeeper',
    '女性店主': 'Female Shopkeeper',
    '生徒会長': 'Student Council President',
    '副会長': 'Student Council Vice President',
    '男': 'Man',
    '少女': 'Girl',
    '校長': 'Principal',
    '直哉＆吹': 'Naoya and Sui',
    '教師': 'Teacher',
    '報道陣': 'Press',
    '男司会者': 'Male MC',
    '女司会者': 'Female MC',
    '女弁護士': 'Female Lawyer',
    '女子校生': 'Schoolgirl',
    '女子校生達': 'Schoolgirls',
    '教師Ａ': 'Teacher A',
    '教師Ｂ': 'Teacher B',
    '客Ａ': 'Customer A',
    '客Ｂ': 'Customer B',
    '客Ｃ': 'Customer C',
    '常連客Ａ': 'Regular Customer A',
    '常連客Ｂ': 'Regular Customer B',
    '常連客Ｃ': 'Regular Customer C',
    '常連客Ｄ': 'Regular Customer D',
    '男子校生Ａ': 'Schoolboy A',
    '男子校生Ｂ': 'Schoolboy B',
    '男子校生Ｃ': 'Schoolboy C',
    '女子校生Ａ': 'Schoolgirl A',
    '女子校生Ｂ': 'Schoolgirl B',
    '女子校生Ｃ': 'Schoolgirl C',
    '女子校生Ｄ': 'Schoolgirl D',
    '女子校生Ｅ': 'Schoolgirl E',
    '女子学生Ａ': 'Female Student A',
    '女子学生Ｂ': 'Female Student B',
    '男子生徒Ａ': 'Male Student A',
    '男子生徒Ｂ': 'Male Student B',
    '男子生徒Ｃ': 'Male Student C',
    '男子生徒Ｄ': 'Male Student D',
    '子供Ａ': 'Child A',
    '子供Ｂ': 'Child B',
    '黒服Ａ': 'Bodyguard A',
    '男性Ｃ': 'Man C',
    'サラリーマンＡ': 'Salaryman A',
    'サラリーマンＢ': 'Salaryman B',
    '洋服屋店員Ａ': 'Clothing Store Employee A',
    '洋服屋店員Ｂ': 'Clothing Store Employee B',
}

def sort_func(el):
    ret = 0
    print(el)
    remaining = el.split('/')[1]
    chap = int(remaining[:2])
    ret += chap*10000
    remaining = remaining[2:]
    remaining = remaining.split('_')[-1]
    remaining = remaining.split('.')[0]
    if any(x in remaining for x in ['pi', 'an', 'ze', 'rn']):
        ret += 0.1
        remaining = remaining[2:]
    try:
        ret += int(remaining)
    except:
        ret += int(remaining[:-1]) + 0.5
    print(ret)
    return ret

def get_fnames():
    ret = []
    for root, dir, file in os.walk('txt_scripts_jp'):
        for fname in file:
            ret.append(os.path.join(root, fname))
    return ret

def create_translation_csv(outname=''):
    total_lines = []
    fnames = get_fnames()
    fnames = sorted(fnames, key=sort_func)
    for fname in fnames:
        with open(fname) as f:
            scriptline = f.readline()
            while scriptline:
                scriptline = f.readline()
                m = re.search(r'.*?>([^a-zA-Z].*)', scriptline)
                # print(m.group(1))
                if m is not None:
                    # print(scriptline)
                    # print(m.group(1))
                    jp_line = m.group(1)
                    if jp_line not in name_dict.keys() and '#FFFFFF' not in jp_line:  # TODO: Fix
                        total_lines.append((jp_line, fname))
                # if 'ruby' in scriptline:
                #     next_line = f.readline()
                #     endruby = f.readline()
                #     next_next_line = f.readline()
                #     scriptline = next_line[:-3] + next_next_line[1:]
                # m = re.search(r'^"(.*)",$', scriptline)
                # try:
                #     total_lines.append(m.group(1))
                # except:
                #     continue
    # unique_set = set()
    # unique_add = unique_set.add
    # unique_lines = [x for x in total_lines if not (x in unique_set or unique_add(x))]
    # print('Total number of lines: {}, Number of unique lines: {}'.format(len(total_lines), len(unique_lines)))
    print('Total number of lines: {}'.format(len(total_lines)))

    with open(outname, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        for line, fname in total_lines:
            # print(line)
            csvwriter.writerow([line, line, fname])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--make_csv', help='File to save empty translation csv', default='',
                        type=str)
    parser.add_argument('--make_translation_scripts', help='use translation.csv to rewrite scripts',
                        action='store_true', default=False)
    args = parser.parse_args()

    print('Arguments:\n{}\n'.format(' '.join(sys.argv[1:])))

    print('Config:')
    pprint.pprint(vars(args), depth=2, width=50)

    if args.make_csv:
        create_translation_csv(outname=args.make_csv)
    if args.make_translation_scripts:
        create_translation_scripts()
    # print_names()
