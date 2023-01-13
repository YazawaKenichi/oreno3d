# oreno3d
## 概要
[oreno3d](https://oreno3d.com) でアップロードされている動画をスクレイピングするスクリプト

## サイトの条件
- `ecchi.iwara.tv` の URL が クラス `video-figure` の `a` タグにあること
- `video-figure` 以外のタグを持っていないこと
- `video-figure` を持つタグの要素の一番はじめの `a` タグが目的の `href` を持っていること
- 動画本体が `vjs-tech` クラスを持つ `video` タグの `src` 属性に記述されていること
- タイトルが `title` クラスを持つ ` h1` タグの要素に記述されていること

## 特徴
投稿動画の URL を `oreno3d.com` の方で入力すれば動画をダウンロードしてくれて、ユーザがちまちま動画を保存しなくて済む

ファイルに投稿動画の URL を記述すればそこから読み出して実行するのでユーザは URL をかき集めればいいだけ

## 動作環境
- OS : Ubuntu 20.04
- Python : 3.8.10
    - pip : 20.0.2
        - BeautifulSoup : 4.8.2
        - Selenium : 4.1.0
        - urllib : 不明
- Chromium : 107.0.5304.87
    - Chrome-Driver : 107.0.5304.62

## 必要な準備
- [ ] BeautifulSoup 4 モジュールのインストール

- [ ] Selenium モジュールのインストール

- [ ] Chromium ブラウザのインストール

- [ ] Chrome Driver の取得

- [ ] `lxml` パーサーのインストール

### Chromium, Chrome-Driver
1. Chromium をインストールする
    ```
    sudo apt install -y chromium-browser
    ```

1. どうにかして Chromium のバージョンを知る
    どうやって？

1. Chromium のバージョンに合った chrome-driver の zip をダウンロードする
    バージョンや OS が違う場合は[こ↑ こ↓ ](https://chromedriver.chromium.org/downloads)から探して適宜ダウンロード
    ```
    wget https://chromedriver.storage.googleapis.com/107.0.5304.62/chromedriver_linux64.zip
    ```

1. zip を解凍する
    ```
    unzip chromedriver_linux64.zip
    ```
    すると chromedriver という実行ファイルが出てくる

1. chromedriver を PATH の通ったディレクトリに入れる
    ```
    sudo mv chromedriver /usr/local/bin/
    ```

#### 注意
Chrome-Driver のバージョンと Chromium のバージョンは対応関係が厳密なのでバージョン選びをミスるとエラーを吐かれるので注意

Chromium が 107 だったら Chrome-Driver も 107 を選ぶと良い

## 使用方法

1. このリポジトリを適当な場所にクローン
    ```
    git clone https://github.com/yazawakenichi/oreno3d
    ```
1. `url/url` に特定の投稿の `URL` アドレスを指定

    `url` ファイルには可能な限り重複した URL を記述しないこと

    記述した場合、二度も同じ動画を保存しようとするため時間がかかる

    重複回避の方法として以下の方法を提示する

    ```
    sort url | uniq > tmp && mv tmp url
    ```

    ただし、これを利用する場合は空白行を入れてはならないことに注意

1. `main.py` を実行
    ```
    ./main.py
    ```

1. `Chromium` がひとりでに動き出して裏でどんどんダウンロードしていくので気長に待つ

# 参考
- [Python で画像・動画をスクレイピングして自動ダウンロードする - ミナピピンの研究室](https://tkstock.site/2022/01/19/python-requests-mp4-jpg-movie-image-write-download/)
- [requests でのスクレイピング時に 403 エラーが返された場合の解決策 - ミナピピンの研究室](https://tkstock.site/2021/07/14/python-requests-ec%E3%82%B5%E3%82%A4%E3%83%88-%E3%82%B9%E3%82%AF%E3%83%AC%E3%82%A4%E3%83%94%E3%83%B3%E3%82%B0-403-%E3%82%A8%E3%83%A9%E3%83%BC/#i)
- [【 Python で Web スクレイピング その 4 】HTML ソースの取得と解析 - インターステラ株式会社 技術ブログ](https://blog.interstellar.co.jp/2019/01/28/python-scraping-4/)
- [【 Python 】ChromeDriver のエラーまとめ【 selenium 】- すしりんぐ blog](https://sushiringblog.com/chromedriver-error)
- [selenium で chromedriver のパスが通らない - teratail](https://teratail.com/questions/321709)
- [【 Python 】Selenium を使ってアクセスしたページをリロード（更新）する方法 - あずみ .NET](http://a-zumi.net/python-selenium-refresh/)
- [python 『 a bytes-like object is required, not 'Response' 』について - teratail](https://teratail.com/questions/336382)
- [Python でファイルの読み込み、書き込み（作成・追記） - note.nkmk.me](https://note.nkmk.me/python-file-io-open-with/#:~:text=%E3%81%AE%E8%BF%BD%E8%A8%98%E3%83%BB%E6%8C%BF%E5%85%A5-,%E6%9C%AB%E5%B0%BE%E3%81%AB%E8%BF%BD%E8%A8%98%3A%20mode%3D'a',%E3%81%AE%E6%9C%AB%E5%B0%BE%E3%81%AB%E8%BF%BD%E8%A8%98%E3%81%A7%E3%81%8D%E3%82%8B%E3%80%82)

# LICENSE
- このソフトウェアは、MIT ライセンスの下、再頒布および使用が許可されます。
- (C) 2022 YAZAWA Kenichi

