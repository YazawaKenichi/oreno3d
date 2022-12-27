# Request によるウェブスクレイピング
## urllib
### 概要
Python に標準で用意されている

### response = request.urlopen(ADDRESS)
`ADDRESS` にはアクセスするアドレスを文字列で指定する。

帰ってくる `response` にはレスポンスの情報を管理するオブジェクトが入る。

#### body = request.urlopen(ADDRESS).read()

### data = body.decode(ENCODING)
`ENCODING` に文字コードを渡すことで `data` にはデコードされた情報が返ってくる。

## chardet

```
pip install chardet
```

### dict = chardet.detect(BODY)

日本語を取り扱う場合は　Chardet ライブラリを使う。

`chardet.detect` は引数の文字コードなどの情報を検出するもの。

辞書型で返される。

`encoding` キーに文字コードが格納される。

例えば返される辞書の内容はこんな感じ

``` Python
{'encoding': 'ascii', 'confidence': 1.0, 'language': ''}
```
## BeautifulSoup ( bs4 )

### インストール
```
pip install beautifulsoup4
```

### BeautifulSoup のインポート
``` Python
from bs4 import BeautifulSoup
```

### BeautifulSoup オブジェクトを作成

``` Python
soup = BeautifulSoup(DATA, PARSER)
```

`DATA` には `body.decode(cs['encoding'])` したデータを入れる。

`PARSER` にはいくつか種類がある。

|パーサー|説明
|:--:|:--:
|`html.parser`|Python 標準の HTML パーサー
|`lxml`|別途インストールが必要だが高速

### 要素を絞り込んでいく

``` Python
soup = BeautifulSoup(DATA, PARSER)
soup.body.main.section
```

とすることで HTML 本文から `body / main / section` の部分を取得できる。

複数ある場合は思ったとおりの取得できないので、この方法で取得できるのは `div` タグの直上くらいまでになると思う。

#### 子ノードや親ノードの一覧を取り出す




