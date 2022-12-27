#!/usr/bin/env python3
# coding:utf-8
# SPDX-FileCopyrightText: YAZAWA Kenichi (2022)
# SPDX-License-Identifier: BSD 3-Clause "New" or "Revised" License

# urllib は標準で用意されている
# そのうちの request の利用
import urllib
from urllib import request
# pip install chardet
import chardet
from bs4 import BeautifulSoup
import numpy as np
import os
import cv2
import time

DOMAIN = 'http://kemono.party'
ARTICLE_CLASS = 'post-card post-card--preview'
ANCHOR_CLASS = ['fileThumb', 'image-link']
DOWNLOAD_DIR = './downloads'
URL_LIST_FILE = "./url/url"

def convertor(download_dir, ui = True):
    image_names = os.listdir(download_dir)
    image_names.sort()
    for index in image_names:
        filename = download_dir + "/" + str(index)
        cv2.imwrite(filename, cv2.imread(filename))
        if ui :
            print("[convert]" + filename)

def mkdir(dirname, ui = True):
    if not os.path.exists(dirname):
        os.makedirs(dirname)
        if ui:
            print("mkdir -r " + dirname)

def download_file(url, filename, ui = True):
    try:
        with request.urlopen(url) as web_file:
            time.sleep(0.5)
            data = web_file.read()
            with open(filename, mode = 'wb') as local_file:
                local_file.write(data)
        if ui :
            print("[write]" + url)
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        if ui :
            print("\x1b[31m" + url + " : Time Out!" + "\x1b[0m", file = sys.stderr)
        time.sleep(0.5)
        download_file(url, filename, ui)

# この関数使ってない
# body / main / section / dev の持つクラスのリストを返す
def get_class(soup):
    class_array = []
    # html 中の body / main / section 内のタグを一覧を順次取得する
    section = soup.body.main.section
    # section 内の子要素を辞書型で取り出す
    for in_section in section.children:
        # これがないとエラる（なんで？）> None と !None が交互に格納されているのが原因（ print(in_section.name) したらわかった）
        if(in_section.name != None):
            # 対象のクラス名は 'card-list card-list--legacy' となっていて、間にスペースが入ってしまっている。
            # これのせいで、辞書の key の中にリストが入るってしまう。
            class_array.append(in_section['class'])
    return class_array

# アドレスの BeautifulSoup を返す
def get_soup(address, ui = True):
    try:
        # レスポンスの情報を管理するオブジェクトを返す
        # このオブジェクトからメソッドを呼び出して必要な情報を取り出す
        with request.urlopen(address) as response:
            time.sleep(0.5)
            # 取得した文字列をまとめて取り出す
            body = response.read()
            if ui:
                print("[open] " + address)
            try:
                # 文字コードの取得
                cs = chardet.detect(body)   # {'encoding': 'ascii', 'confidence': 1.0, 'language': ''}
                data = body.decode(cs['encoding'])
                # BeautifulSoup オブジェクトの作成
                soup = BeautifulSoup(data, 'lxml')
                return soup
            except UnicodeDecodeError:
                data = body
                # BeautifulSoup オブジェクトの作成
                soup = BeautifulSoup(data, 'lxml')
                return soup
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        if ui :
            print("\x1b[31m" + address + " : Time Out!" + "\x1b[0m", file = sys.stderr)
        time.sleep(0.5)
        get_soup(address, ui)

# アーティスト名の取得
def get_artist_name(soup, ui = True):
    spans = soup.find_all("span", itemprop = "name")
    for span in spans:
        if ui:
            print("artist : " + span.text)
        return span.text

# 投稿記事の URL の取得
def get_post_urls(soup, article_class, ui = True):
    # なんかいろいろ大変なことしてたけどこれやれば一発だった...
    # article には ARTICLE_CLASS クラスの内容物が入る
    # 複数ある場合は配列になる
    articles = soup.find_all(class_ = article_class)
    hrefs = []

    # ARTICLE_CLASS に一致する配列を順次取り出す
    for article in articles:
        # article の子要素を順次取り出す
        for in_article in article.children:
            if(in_article.name != None):
                # タグの名前が 'a' だった場合
                if(in_article.name == 'a'):
                    hrefs.append(str(in_article['href']))
                    if ui :
                        print("[append] " + str(in_article['href']))
    return hrefs

def get_post_title(suop, ui = True):
    h1 = soup.find(class_ = "post__title")
    span = h1.find("span")
    title = span.text
    if ui:
        print("post title : " + title)
    return title

# 画像 URL の取得
def get_image_urls(soup, anchor_class, ui = True):
    anchors = soup.find_all(class_ = anchor_class[0])
    hrefs = []

    for anchor in anchors:
        img = anchor.find('img')
        hrefs.append(str(img['src']))
        if ui :
            print("[append] " + str(img['src']))
    return hrefs

# 次のページの URL の取得
def get_next_page_url(soup):
    anchors = soup.find_all(class_="next")
    if anchors is None:
        return None
    else:
        try:
            return anchors[0]
        except IndexError as e:
            return None

def get_address_from_file(url_list_file):
    with open(url_list_file) as f:
        lines = []
        for line in f:
            lines.append(line)
    return lines

if __name__ == '__main__':
    addresses = get_address_from_file(URL_LIST_FILE)
    for address in addresses:
        page_address = address
        nextpage = True
        post_urls = []
        artist_name = ""
        # 次のページがあるときはループし続ける
        while nextpage:
            # アーティストページの HTML を取得
            soup_artist_one_page = get_soup(page_address)
            # 投稿の URL をリストで取得
            post_urls.extend([DOMAIN + post_url for post_url in get_post_urls(soup_artist_one_page, ARTICLE_CLASS)])
            # 次のページの有無と次のページがある場合はその URL
            next_page_anchor = get_next_page_url(soup_artist_one_page)
            # 次のページがある場合
            if next_page_anchor is None:
                # アーティストの名前を取得
                artist_name = get_artist_name(soup_artist_one_page)
                nextpage = False
            else:
                page_address = DOMAIN + str(next_page_anchor['href'])

        artist_image_urls = {}
        for url in post_urls:
            soup = get_soup(url)
            post_title = get_post_title(soup)
            image_urls = get_image_urls(soup, ANCHOR_CLASS)
            artist_image_urls[post_title] = [DOMAIN + image_url for image_url in image_urls]

        title_and_urls = artist_image_urls

        for title_key in title_and_urls.keys():
            download_dir = DOWNLOAD_DIR + "/" + artist_name + "/" + title_key
            mkdir(download_dir)
            for index, url in enumerate(title_and_urls[title_key]):
                download_file(url, download_dir + "/" + str(index).zfill(6) + ".png")
                time.sleep(0.5)

            convertor(download_dir)



