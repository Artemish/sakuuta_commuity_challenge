import os
import sys
import re
import argparse
import pprint
import csv

name_dict = {
}

def sort_func(el):
    ret = 0
    remaining = el.split('/')[1]
    chap = int(remaining[:2])
    ret += chap*10000
    remaining = remaining[2:]
    remaining = remaining.split('_')[-1]
    remaining = remaining.split('.')[0]
    try:

    1/0


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
    print(fnames)
    1/0
    for fname in fnames:
        with open(os.path.join('script', fname)) as f:
            scriptline = f.readline()
            while scriptline:
                scriptline = f.readline()
                if 'ruby' in scriptline:
                    next_line = f.readline()
                    endruby = f.readline()
                    next_next_line = f.readline()
                    scriptline = next_line[:-3] + next_next_line[1:]
                m = re.search(r'^"(.*)",$', scriptline)
                try:
                    total_lines.append(m.group(1))
                except:
                    continue
    unique_set = set()
    unique_add = unique_set.add
    unique_lines = [x for x in total_lines if not (x in unique_set or unique_add(x))]
    print('Total number of lines: {}, Number of unique lines: {}'.format(len(total_lines), len(unique_lines)))

    with open(outname, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        for line in unique_lines:
            # print(line)
            csvwriter.writerow([line, line])

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
