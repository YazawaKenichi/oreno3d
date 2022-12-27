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

`selenium` を使用しないため、コンソールのみでのスクレイピングが可能

CLI での使用に限られたサーバーのような環境でスクレイピングでき、ユーザの環境を極力選ばない構造

ユーザごとに保存先のディレクトリが用意されるので後からまとめ直す必要が無い

投稿ごとに保存先のディレクトリが用意されるので後からまとめ直す必要が無い

ファイルにアーティストの URL を記述すればそこから読み出して実行するのでユーザは URL をかき集めればいいだけ

## 動作環境
- OS : Ubuntu 20.04
- Python : 3.8.10
    - pip : 20.0.2
        - chardet : 3.0.4
        - NumPy : 1.19.3
        - BeautifulSoup : 4.8.2
        - urllib : 不明

## 必要な準備
- [ ] BeautifulSoup 4 のインストール

- [ ] `lxml` パーサーのインストール

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

# LICENSE
- このソフトウェアは、3 条項 BSD ライセンスの下、再頒布および使用が許可されます。
- (C) 2022 YAZAWA Kenichi