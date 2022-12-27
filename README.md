# kemono
## 概要
[oreno3d](https://oreno3d.com) でアップロードされている動画をスクレイピングするスクリプト

** まだ開発中 **

** [kemono ( YazawaKenichi 's Repository ) - GitHub](https://github.com/yazawakenichi/kemono) からまるごとコピーして改造して作成 **

## サイトの条件
- 投稿記事の URL が クラス `post-card post-card--preview` の `article` タグにあること
- article タグの子要素に `a` タグがあり、その `href` が投稿記事の URL であること
- 次のページの URL が クラス `next` の `a` タグ `href` にあること
- アーティストの名前が `itemprop` が `name` の `span` タグの要素にあること
- 投稿記事中の画像が クラス `fileThumb image-link` の `a` タグ にあること
- その `a` タグが `img` タグをただ一つだけ持つこと
- `img` タグに `src` が設定されていて、これが投稿された画像であること

## 特徴
アーティストの URL を入力すれば画像を取り出してくれて、ユーザがちまちま画像を保存しなくて済む

ユーザごとに保存先のディレクトリが用意されるので後からまとめ直す必要が無い

投稿ごとに保存先のディレクトリが用意されるので後からまとめ直す必要が無い

ファイルにアーティストの URL を記述すればそこから読み出して実行するのでユーザは URL をかき集めればいいだけ

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
    wget https://chromedriver.storage.googleapis.com/index.html?path=107.0.5304.62/
    ```

1. zip を解凍する
    ```
    unzip chromedriver_linux64.zip
    ```
    すると chromedriver という実行ファイルが出てくる

1. chromedriver を PATH の通ったディレクトリに入れる
    ```
    mv chrome-driver /usr/local/bin/
    ```

#### 注意
Chrome-Driver のバージョンと Chromium のバージョンは対応関係が厳密なのでバージョン選びをミスるとエラーを吐かれるので注意

Chromium が 107 だったら Chrome-Driver も 107 を選ぶと良い

## 使用方法

1. このリポジトリを適当な場所にクローン
    ```
    git clone https://github.com/yazawakenichi/kemono
    ```
1. `url` に特定のユーザの `URL` アドレスを指定

    ここで、パラメータ指定 `?` を入れないこと！

    入れた場合はそのページからのスクレイピングになり、アーティストが投稿した全ての画像をスクレイピングできるわけではなくなってしまう！

    `url` ファイルには可能な限り重複した URL を記述しないこと

    記述した場合、二度も同じ画像を保存しようとするため時間がかかる

    重複回避の方法として以下の方法を提示する

    ```
    sort url | uniq > tmp && mv tmp url
    ```

    ただし、これを利用する場合は空白行を入れてはならないことに注意

1. `main.py` を実行
    ```
    ./main.py
    ```

# 参考
- [Python で画像・動画をスクレイピングして自動ダウンロードする - ミナピピンの研究室](https://tkstock.site/2022/01/19/python-requests-mp4-jpg-movie-image-write-download/)
- [requests でのスクレイピング時に 403 エラーが返された場合の解決策 - ミナピピンの研究室](https://tkstock.site/2021/07/14/python-requests-ec%E3%82%B5%E3%82%A4%E3%83%88-%E3%82%B9%E3%82%AF%E3%83%AC%E3%82%A4%E3%83%94%E3%83%B3%E3%82%B0-403-%E3%82%A8%E3%83%A9%E3%83%BC/#i)
- [【 Python で Web スクレイピング その 4 】HTML ソースの取得と解析 - インターステラ株式会社 技術ブログ](https://blog.interstellar.co.jp/2019/01/28/python-scraping-4/)
- [【 Python 】ChromeDriver のエラーまとめ【 selenium 】- すしりんぐ blog](https://sushiringblog.com/chromedriver-error)
- [selenium で chromedriver のパスが通らない - teratail](https://teratail.com/questions/321709)
- [【 Python 】Selenium を使ってアクセスしたページをリロード（更新）する方法 - あずみ .NET](http://a-zumi.net/python-selenium-refresh/)
- [python 『 a bytes-like object is required, not 'Response' 』について - teratail](https://teratail.com/questions/336382)

# LICENSE
- このソフトウェアは、3 条項 BSD ライセンスの下、再頒布および使用が許可されます。
- (C) 2022 YAZAWA Kenichi

