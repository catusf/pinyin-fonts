# -*- coding: utf-8 -*-
#!/usr/bin/env python

# time python3 src/main.py

import os
import subprocess
import shell
import sys
import orjson
import argparse
import font as ft
import path as p
import config
import make_template_jsons
import retrieve_latin_alphabet
import path

def parse_args(args):
    parser = argparse.ArgumentParser(
        description="Select font name to generate (catus/tigris/leo/onca)")
    parser.add_argument('-t', '--style', choices=['catus','tigris', 'leo', 'onca'], default='leo')
    return parser.parse_args(args)
# Display the configurations
import pprint
def main(args=None):
    options = parse_args(args)
    style = options.style
    meta = config.font_configs[style]
    # if options.style == "han_serif":
    
    pprint.pprint(meta)

    FONT_FOR_MAIN   = os.path.normpath(os.path.join(path.DIR_FONT, meta['main_font_path']))
    FONT_FOR_PINYIN = os.path.normpath(os.path.join(path.DIR_FONT, meta['pinyin_font_path']))
    OUTPUT_FONT     = os.path.join(p.DIR_OUTPUT, meta["output_font"])
    FONT_NAME       = meta['font_name']
    
    # font (otf/ttf)を編集可能な json にダンプする
    make_template_jsons.make_template(FONT_FOR_MAIN)
    retrieve_latin_alphabet.make_alphabet_glyf_json(FONT_FOR_PINYIN)
    print("finished dumping font")

    # 編集可能ファイルである json の出力名を指定する
    ALPHABET_FOR_PINYIN_JSON = os.path.join(p.DIR_TEMP, "alphabet4pinyin.json")
    TAMPLATE_MAIN_JSON       = os.path.join(p.DIR_TEMP, "template_main.json")
    TAMPLATE_GLYF_JSON       = os.path.join(p.DIR_TEMP, "template_glyf.json")

    # 読み込む多音字の辞書データ
    PATTERN_ONE_TXT          = os.path.join(p.DIR_OUTPUT, "duoyinzi_pattern_one.txt")
    PATTERN_TWO_JSON         = os.path.join(p.DIR_OUTPUT, "duoyinzi_pattern_two.json")
    EXCEPTION_PATTERN_JSON   = os.path.join(p.DIR_OUTPUT, "duoyinzi_exceptional_pattern.json")

    font = ft.Font( TAMPLATE_MAIN_JSON, TAMPLATE_GLYF_JSON, ALPHABET_FOR_PINYIN_JSON, \
                    PATTERN_ONE_TXT, PATTERN_TWO_JSON, EXCEPTION_PATTERN_JSON, style )
    # glyf に追加するpinyin の種類は、mapping_table に準拠する
    font.build(FONT_NAME, OUTPUT_FONT)
    
if __name__ == "__main__":
    sys.exit(main())