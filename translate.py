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
    '片貝': 'Katagai',
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
    '井上理事': 'Director Inoue',
    '丘沢': 'Okazawa',  # TODO: Who is this even? Check if name is correct
    'ヤス': 'Yasu', 
    '村田': 'Murata',
    '坂本': 'Sakamoto',
    '麗華': 'Reika',
    '御桜父親': "Rin's Father",
    '御桜母親': "Rin's Mother",
    '東浪見': 'Put name here later',  # TODO
    '一宮': 'Put name here later',  # TODO
    '中里': 'Put name here later',  # TODO
    'おやっさん': 'Put name here later',  # TODO
    '宇綱': 'Put name here later',  # TODO
    '末竹': 'Put name here later',  # TODO
    '一同': 'Everyone',
    '中年': 'Middle-aged Man',
    '老人': 'Old Man',
    '店主': 'Shopkeeper',
    '店員': 'Employee',
    '管財人': 'Executor',
    '女性店主': 'Female Shopkeeper',
    '生徒会長': 'Student Council President',
    '副会長': 'Student Council Vice President',
    '男': 'Man',
    '少女': 'Girl',
    '校長': 'Principal',
    '教頭': 'Vice Principal',
    '直哉＆吹': 'Naoya and Sui',
    '教師': 'Teacher',
    '報道陣': 'Press',
    '看護婦': 'Nurse',
    '神父': 'Priest',
    '管理人': 'Caretaker',
    '男司会者': 'Male MC',
    '女司会者': 'Female MC',
    '司会者': 'MC',
    '女弁護士': 'Female Lawyer',
    '女子校生': 'Schoolgirl',
    '女子校生達': 'Schoolgirls',
    '女子一同': 'All of the Girls',
    '男子一同': 'All of the Boys',
    'バイトの子': 'Part-Time Employee',
    '関係者': 'Concerned Party',
    'おっさんＡ': 'Old Guy A',
    'おっさんＢ': 'Old Guy B',
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
    '黒服Ｂ': 'Bodyguard B',
    '黒服Ａ＆黒服Ｂ': 'Bodyguard A and Bodyguard B',
    '男性Ｃ': 'Man C',
    'サラリーマンＡ': 'Salaryman A',
    'サラリーマンＢ': 'Salaryman B',
    '洋服屋店員Ａ': 'Clothing Store Employee A',
    '洋服屋店員Ｂ': 'Clothing Store Employee B',
    '関係者Ａ': 'Concerned Party A',
    '関係者Ｂ': 'Concerned Party B',
    '記者Ａ': 'Reporter A',
    '記者Ｂ': 'Reporter B',
    '記者Ｃ': 'Reporter C',
    '生徒Ａ': 'Student A',
    '生徒Ｂ': 'Student B', # Maybe no student B
    '生徒Ｃ': 'Student C',
}

def sort_func(el):
    ret = 0
    print(el)
    remaining = el.split('/')[1]
    chap = int(remaining[:2])
    ret += chap*10000
    remaining = remaining[2:]
    if 'picapica' in remaining:
        ret += 1000
    if 'olympia' in remaining:
        ret += 2000
    if 'zypressen' in remaining:
        ret += 3000
    if 'marchen' in remaining:
        ret += 4000
    if 'andoe' in remaining:
        ret += 5000
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
            speaker = 'Self'
            while scriptline:
                scriptline = f.readline()
                m = re.search(r'.*?>([^a-zA-Z].*)', scriptline)
                if m is not None:
                    jp_line = m.group(1)
                    if jp_line in name_dict.keys():
                        speaker = name_dict[jp_line]
                    if jp_line not in name_dict.keys() and '#FFFFFF' not in jp_line and '6sakura' not in jp_line:  # TODO: Fix
                        total_lines.append((jp_line, speaker, fname))
                        speaker = 'Self'
    print('Total number of lines: {}'.format(len(total_lines)))

    with open(outname, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        for line, speaker, fname in total_lines:
            csvwriter.writerow([line, line, fname, speaker])

def create_translation_scripts():
    translation = []
    with open('translation.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            translation.append((row[0], row[1]))

    fnames = get_fnames()
    fnames = sorted(fnames, key=sort_func)
    en_files = []
    idx = 0
    for fname in fnames:
        outname = os.path.join('txt_scripts_en', fname.split('/')[1].split('.')[0] + '.txt')
        with open(outname, 'w') as en_f:
            with open(fname, 'r') as jp_f:
                jp_scriptline = jp_f.readline()
                en_f.write(jp_scriptline)
                while jp_scriptline:
                    jp_scriptline = jp_f.readline()
                    # if 'ruby' in jp_scriptline:
                    #     next_line = jp_f.readline()
                    #     endruby = jp_f.readline()
                    #     next_next_line = jp_f.readline()
                    #     jp_scriptline = next_line[:-3] + next_next_line[1:]
                    # if 'name' in jp_scriptline and '？？？' not in jp_scriptline:
                    #     m = re.search(r'^name={name="(.*)"},$', jp_scriptline)
                    #     name = m.group(1)
                    #     eng_line = 'name={{name="{}"}},\n'.format(name_dict[name])
                    #     en_f.write(eng_line)
                    #     continue
                    # m = re.search(r'^"(.*)",$', jp_scriptline)
                    m = re.search(r'(.*?>)([^a-zA-Z].*)', jp_scriptline)
                    # if m.group(2) is not None:
                    if m is not None:
                        jp_line = m.group(2)
                        if jp_line not in name_dict.keys() and '#FFFFFF' not in jp_line and '6sakura' not in jp_line:  # TODO: Fix
                            check_jp_line, new_eng_line = translation[idx]
                            new_eng_line = '{}: {}'.format(str(idx + 1), new_eng_line)  # For debugging
                            idx += 1
                            try:
                                assert jp_line == check_jp_line
                            except:
                                print(check_jp_line)
                                print(jp_line)
                                1/0
                            eng_line = '{}{}\n'.format(m.group(1), new_eng_line)
                            en_f.write(eng_line)
                        if jp_line in name_dict.keys():
                            eng_line = '{}{}\n'.format(m.group(1), name_dict[m.group(2)])
                            en_f.write(eng_line)
                    else:
                        en_f.write(jp_scriptline)

                    # try:
                    #     eng_line = '"{}",\n'.format(translation[m.group(1)])
                    #     en_f.write(eng_line)
                    #     # print('Replaced {} with {}'.format(scriptline, eng_line))
                    # except AttributeError:
                    #     en_f.write(jp_scriptline)


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
