import os
import re
import sys
import time
from datetime import datetime


def ReversePuctuation(file, newfile):
    f = open(file, 'r', encoding="ISO-8859-1")
    nf = open(newfile, 'w', encoding="ISO-8859-1")

    for line in f:
        if len(line) > 2:
            nf.write(FixOneLine(line[:-1]) + line[-1])
        else:
            nf.write(line)
    f.close()
    nf.close()


def reverse_clousre(s):
    if s == '(':
        return ')'
    if s == ')':
        return '('
    return s
def FixOneLine(s):
    if s.startswith('-') and s.endswith('-'):
        s = s.replace('- ', '')
        s = s.replace(' -', '')
    s = s.replace('<i>', '')
    s = s.replace('</i>', '')
    if s.startswith('-') and s.endswith('-'):
        s = s.replace('- ', '')
        s = s.replace(' -', '')

    StartSpecialChars = '.,:;''?()-?!+=*&$^%#@~`" /'
    EndSpecialChars = '(-*~`" /'
    Prefix = ''
    Suffix = ''

    while (len(s) > 0 and s[0] in StartSpecialChars):
        result = reverse_clousre(s[0])
        Prefix += result
        s = s[1:]

    while (len(s) > 0 and s[-1] in EndSpecialChars):
        result = reverse_clousre(s[-1])
        Suffix += result
        s = s[:-1]


    if Prefix == ' -':
        Prefix = '- '
    if Suffix == ' -':
        Suffix = '- '

    return Suffix + s + Prefix


def get_all_ext(path, ext):
    files = []
    for r, d, f in os.walk(path):
        for file in f:
            full_file_path = os.path.join(r, file)
            if 'forced.forced' in file:
                os.remove(full_file_path)
                continue
            if file.endswith(ext) and not file.endswith('.en.srt') and not file.endswith('.eng.srt') and not file.endswith('.forced.srt') and not os.path.exists( ".".join(re.split('[.]', full_file_path)[:-1]) + ".forced.srt"):
                files.append(os.path.join(r, file))
    return files


def Main():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("{} : Start scan: {}".format(dt_string, sys.argv[1]))
    root_dir = sys.argv[1]
    if (not root_dir):
        print('Usage: Select root dir')
        return

    file_list = get_all_ext(root_dir, ".srt")
    print("Found " + str(len(file_list)) + " files. Starting to convert")

    for file in file_list:
        print('Reverse SRT file {} started'.format(file))
        new_file = ".".join(re.split('[.]', file)[:-1]) + ".forced.srt"
        try:
            ReversePuctuation(file, new_file)
            print('Reverse SRT file {} success'.format(file))
        except Exception as e:
            os.remove(new_file)
            print('Reverse SRT file {} failed'.format(file))
            print(e)


if __name__ == '__main__':
    Main()
