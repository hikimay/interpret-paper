# interpret-paper

論文のURLまたはローカルPDFを指定すると，日本語の詳細解説HTMLを生成するツール．

## セットアップ

[uv](https://docs.astral.sh/uv/) が必要です．

```bash
uv sync
```

## 使い方

このプロジェクトディレクトリで Claude Code を開き，チャットから依頼します．

### URL を指定する

```
この論文を解説して: https://arxiv.org/abs/1706.03762
/interpret https://arxiv.org/abs/2301.12345
```

arXiv URL の場合，HTML版 → PDF の順に自動で取得を試みます．

### ローカル PDF を指定する

```
/interpret papers/adam.pdf
```

`papers/` に PDF を置いてから指定してください．

### papers/ から選択する

```
/interpret --select
```

## 出力

`output/` に HTML ファイルが生成されます．ブラウザで開くだけで数式がレンダリングされます（MathJax，インターネット接続が必要）．
