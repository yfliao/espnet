import os, sys
import argparse
import csv
import re

def parse_opts():
    parser = argparse.ArgumentParser(
        description='Strips unhelpful, from LM viewpoint, strings from PG texts',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-utt', '--taiwanese-utt-file', action='append',
                        help='Split chinese word to char which use for writting the output text')

    parser.add_argument('in_text', type=str, help='Input text file')
    parser.add_argument('taiwanese_tab', type=str, help='Input taiwanese table file')
    parser.add_argument('out_text', type=str, help='Filtered output text file')
    opts = parser.parse_args()
    return opts

def check_english(check_str):
    check = False
    for ch in check_str:
        if (ch >= u'\u0041' and ch <= u'\u005A') or \
            (ch >= u'\u0061' and ch <= u'\u007A') or ch == "'":
            check = True
        else:
            return False
    if check:
        return True

def check_full_english(check_str):
    check = False
    for w in check_str.split():
        if check_english(w):
            check = True
        else:
            return False
    if check:
        return True

def check_contain_chinese(check_str):
    check = False
    RE_HANS = re.compile(
        r'^(?:['
        r'\u3100-\u312f'           # Bopomofo
        r'\u3400-\u4dbf'           # CJK Ext.A:[3400-4DBF]
        r'\u4e00-\u9fff'           # CJK baise:[4E00-9FFF]
        r'\uf900-\ufaff'           # CJK Comp:[F900-FAFF]
        r'\U00020000-\U0002A6DF'   # CJK Ext.B:[20000-2A6DF]
        r'\U0002A703-\U0002B73F'   # CJK Ext.C:[2A700-2B73F]
        r'\U0002B740-\U0002B81D'   # CJK Ext.D:[2B740-2B81D]
        r'\U0002F80A-\U0002FA1F'   # CJK Comp:[2F800-2FA1F]
        r'])+$'
    )
    for ch in check_str:
        if RE_HANS.match(ch):
            check = True
        else:
            return False
    if check:
        return True

def read_csv(path):
    table = []
    with open(path, newline='') as csvfile:
        rows = csv.reader(csvfile)
        rows = list(rows)
        con = rows[0][2:]
        table.extend(con)
        for row in rows[2:]:
            table.extend([ row[0]+_n for _n in con ])
    return table

def check_taiwanese(check_str, table):
    tone_list = [u"ā", u"á", u"ǎ", u"à", u"â", u"a̍", \
                 u"ē", u"é", u"ě", u"è", u"ê", u"e̍", \
                 u"ō", u"ó", u"ǒ", u"ò", u"ô", u"o̍", u"ő", \
                 u"ī", u"í", u"ǐ", u"ì", u"î", u"i̍", \
                 u"ū", u"ú", u"ǔ", u"ù", u"û", u"u̍", \
                       u"ń", u"ň", u"ǹ", u"n̍", \
                 u"m̄", u"ḿ", u"m̀", u"m̍"]
    # tone_list = [u"ā", u"á", u"ǎ", u"à", u"â", \
    #              u"ē", u"é", u"ě", u"è", \
    #              u"ō", u"ó", u"ǒ", u"ò", u"ô", u"ő", \
    #              u"ī", u"í", u"ǐ", u"ì", u"i", u"î", \
    #              u"ū", u"ú", u"ǔ", u"ù", u"ü", u"ǖ", u"ǘ", u"ǚ" ,u"ǜ", u"û", \
    #              u"ń", u"ň", u"ǹ", \
    #              u"m̄", u"ḿ", u"m̀", \
    #              u"ê", u"ê̄", u"ế", u"ê̌", u"ề"]
    if len(check_str.split()) == 2:
        check = False
        for _str in check_str.split():
            if not ( any( [ _ in tone_list for _ in _str] ) or _str in table or check_contain_chinese(_str) ):
                return False
        return True
    else:
        return any([ _ in tone_list for _ in check_str] ) or check_str in table

if __name__ == '__main__':
    opts = parse_opts()

    tai_id = []
    if opts.taiwanese_utt_file:
        for f in opts.taiwanese_utt_file:
            with open(f, "r") as rf:
                tai_id.extend([ l.split()[0] for l in rf.readlines() ])

    data = []
    table = read_csv(opts.taiwanese_tab)
    with open(opts.in_text, "r", encoding="utf-8") as rf:
        for l in rf.readlines():
            if len(l.split()) > 1:
                u = l.split(maxsplit=1)[0]

                # taiwanese mode
                taiwanese_mode = False
                if opts.taiwanese_utt_file:
                    if u in tai_id:
                        taiwanese_mode = True

                t = ""
                switchcode = ""
                b_w = ""
                try:
                    for w in l.split(maxsplit=1)[1].split():
                        if len(t) == 0:
                            if taiwanese_mode:
                                if check_taiwanese(w, table) or check_contain_chinese(w):
                                    t += "[TW] @{} ".format(w)
                                    switchcode = "tw"
                                else:
                                    t += "[EN] {} ".format(w)
                                    switchcode = "en"
                            else:
                                if check_contain_chinese(w):
                                    t += "[CHT] {} ".format(w)
                                    switchcode = "cht"
                                else:
                                    t += "[EN] {} ".format(w)
                                    switchcode = "en"
                        else:
                            if taiwanese_mode:
                                if switchcode == "tw":
                                    if check_taiwanese("{} {}".format(b_w, w), table):
                                        t += " @{} ".format(w)
                                    else:
                                        t += "[EN] {} ".format(w)
                                        switchcode = "en"
                                else:
                                    if check_full_english(b_w+w) and not check_taiwanese("{} {}".format(b_w, w), table):
                                        t += " {} ".format(w)
                                    else:
                                        t += "[TW] @{} ".format(w)
                                        switchcode = "tw"
                            else:
                                if switchcode == "cht":
                                    if check_contain_chinese(b_w+w):
                                        t += " {} ".format(w)
                                    else:
                                        t += "[EN] {} ".format(w)
                                        switchcode = "en"
                                else:
                                    if check_full_english(b_w+w):
                                        t += " {} ".format(w)
                                    else:
                                        t += "[CHT] {} ".format(w)
                                        switchcode = "cht"
                            #print(b_w+w, switchcode)
                        b_w = w
                    data.append("{} {}\n".format(u, " ".join(_t for _t in t.split()).strip()))
                except Exception as e:
                    print(u, e)

    with open(opts.out_text, "w", encoding="utf-8") as wf:
        wf.writelines(data)
