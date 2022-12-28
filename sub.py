#!/usr/bin/env python3
# coding:utf-8
# SPDX-FileCopyrightText: YAZAWA Kenichi (2022)
# SPDX-License-Identifier: MIT License

### Chrome でエクスポートしたブックマークの HTML ファイルから特定の ADD_DATE を持つブックマークリストを出力

# スクレイピング用のモジュール
from bs4 import BeautifulSoup

# 基本モジュール
import time
import sys

ADDRESS = "./url/url.html"
ADD_DATE = "1672184864"

UI = False

# アドレスの BeautifulSoup を返す
def get_soup(address, ui = True):
    with open(address) as f:
        # BeautifulSoup オブジェクトの作成
        soup = BeautifulSoup(f.read(), 'lxml')
        return soup
    print("ファイルが存在しません", file = sys.stderr)
    sys.exit(0)

# 特定のクラス _class を持つタグが持つ要素内にある anchor の href を取得
def get_link_urls(soup, _class, tag = None, ui = True):
    elements = soup.find_all("a", add_date = _class)
    hrefs = []

    # _class を持つタグが一つのページに複数あった場合は両方の <a> タグに対して処理する
    # _class を持つタグ内に <a> タグが一つであること前提（複数の場合は一番上が取得される）
    for element in elements:
        anchor = element
        hrefs.append(str(anchor['href']))
    # リストが返る
    # 理想的には figure class=figure_class はページ内に一つなので、リストじゃなくて文字列として返しても良い
    return hrefs

if __name__ == '__main__':
    address = ADDRESS
    page_address = address
    # メインページの HTML を取得
    soup = get_soup(page_address, UI)   # [open] https://hogehoge...
    # 次のページの URL を取得
    urls = get_link_urls(soup, ADD_DATE, "a", UI)    # [append] https://piyopiyo...

    for v in urls:
        print(v)

