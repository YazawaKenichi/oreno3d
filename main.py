#!/usr/bin/env python3
# coding:utf-8
# SPDX-FileCopyrightText: YAZAWA Kenichi (2022)
# SPDX-License-Identifier: BSD 3-Clause "New" or "Revised" License

# スクレイピング用のモジュール
# urllib は標準で用意されている
import urllib
from urllib import request
import requests
from bs4 import BeautifulSoup

# 基本モジュール
import os
import time
import sys

# 画像変換
import cv2

# 動的サイト捜査
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# import chromedriver_binary

DOMAIN = 'http://oreno3d.com'
FIGURE_CLASS = 'video-figure'
VIDEO_CLASS = "vjs-tech"

COUNT = 5
DOWNLOAD_DIR = './downloads/'
URL_LIST_FILE = "./url/url"
UI = True

# 引数を解析する
def get_args(ui = True):
    usage = "Usage: %prog"
    parser = OptionParser(usage = usage)
    if ui:
        optdict, args = parser.parse_args()
        print(optdict)
    return parser.parse_args()

def get_address_from_file(url_list_file):
    with open(url_list_file) as f:
        lines = []
        for line in f:
            lines.append(line)
    return lines

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

def download_img(url, filename, ui = True):
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
        download_img(url, filename, ui)

def download_video(url, filename, ui = True):
    try:
        response = requests.get(url)
        with open(filename, mode = 'wb') as local_file:
            if ui :
                print("[writting] " + url + " to " + filename)
            local_file.write(response.content)
            if ui :
                print("[written] " + url + " to " + filename)
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        if ui :
            print("\x1b[31m" + url + " : Time Out!" + "\x1b[0m", file = sys.stderr)
        time.sleep(0.5)
        download_video(url, filename, ui)

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
    # リクエストヘッダを記述
    headers = { "User-Agent" : "Mozilla/5.0" }
    try:
        # レスポンスの情報を管理するオブジェクトを返す
        # このオブジェクトからメソッドを呼び出して必要な情報を取り出す
        response = requests.get(url = address, headers = headers)
        time.sleep(0.5)
        # 取得した文字列をまとめて取り出す
        body = response.text
        if ui:
            print("[open] " + address)
        data = body
        # BeautifulSoup オブジェクトの作成
        soup = BeautifulSoup(data, 'lxml')
        return soup
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        if ui :
            print("\x1b[31m" + address + " : Time Out!" + "\x1b[0m", file = sys.stderr)
        time.sleep(0.5)
        get_soup(address, ui)

# 特定のクラス _class を持つタグが持つ要素内にある anchor の href を取得
def get_link_urls(soup, _class, ui = True):
    # class 名は一つしか指定されていないことが前提（複数の場合は _class をリストにする必要がある）
    elements = soup.find_all(class_ = _class)
    hrefs = []

    # _class を持つタグが一つのページに複数あった場合は両方の <a> タグに対して処理する
    # _class を持つタグ内に <a> タグが一つであること前提（複数の場合は一番上が取得される）
    for element in elements:
        anchor = element.find('a')
        hrefs.append(str(anchor['href']))
        if ui :
            print("[append] " + str(anchor['href']))
    # リストが返る
    # 理想的には figure class=figure_class はページ内に一つなので、リストじゃなくて文字列として返しても良い
    return hrefs

class Browser:
    def __init__(self, bin_loc = "/usr/bin/chromium-browser", ui = True):
        self.selenium_init(bin_loc, ui)

    # ブラウザを動かすためのクラスを作成する
    def selenium_init(self, bin_loc = "/usr/bin/chromium-browser", ui = True):
        # options = Options()
        # options.add_argument("--headless")
        # options.binary_location = bin_loc
        self.driver = webdriver.Chrome()

    # URL で指定したサイトの HTML を全て読み込ませてから取得する
    def get_soup(self, url, delay = 5, ui = True):
        # ブラウザでページを開く
        self.driver.get(url)
        # ブラウザでページが開ききるのを待つ
        time.sleep(delay)
        # HTML ソースを取得
        html = self.driver.page_source
        # bs4 型に作成
        soup = BeautifulSoup(html, "lxml")
        if ui:
            print("[open] " + url)
        return soup

    def reload(self, num = "", ui = True):
        self.driver.refresh()
        if ui:
            string = "Reflesh " + str(num)
            print("[Processing] " + string)

""" ここから特有 """

# 動画本体の URL の取得
def get_video_src(soup, video_class, ui = True):
    # ページ内に同じクラスが複数合った場合一番上が入る
    video = soup.find("video", class_ = video_class)
    src = video["src"]
    if ui:
        print("[append] " + src)
    # 文字列を返す
    return src

# 投稿のタイトルを取得
def get_post_title(suop, ui = True):
    h1 = soup.find("h1", class_ = "title")
    title = h1.text
    if ui:
        print("[append] : " + title)
    return title

if __name__ == '__main__':
    browser = Browser(ui = UI)
    addresses = get_address_from_file(URL_LIST_FILE)
    for address in addresses:
        page_address = address
        nextpage = True
        # メインページの HTML を取得
        soup = get_soup(page_address, UI)   # [open] https://hogehoge...
        # 次のページの URL を取得
        urls = get_link_urls(soup, FIGURE_CLASS, UI)    # [append] https://piyopiyo...
        # リストが返ってきてしまう
        # どうせ一つしか無いので文字列型に変換
        url = str(urls[0])
        for index in range(COUNT):
            # 次のページの HTML を取得
            soup = browser.get_soup(url, ui = UI)
            try:
                # 動画の URL を取得
                src = get_video_src(soup, VIDEO_CLASS, UI)
                break;
            except:
                browser.reload(index + 1)
            if index >= COUNT:
                print("[error] " + "Can not access the video " + url, file = sys.stderr)
                sys.exit(1)
        # 返される URL は文字が抜けてるので URL として正しい文字列に再生成
        src = "https:" + str(src)
        # タイトルの取得とファイル名の生成
        title = DOWNLOAD_DIR + get_post_title(url) + ".mp4"
        # 動画を取得
        download_video(src, title, UI)


