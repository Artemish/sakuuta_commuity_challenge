import os
import sys
import re
import argparse
import pprint
import csv

name_dict = {
}


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
