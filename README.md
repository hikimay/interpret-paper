# interpret-paper

論文のURLまたはローカルPDFを指定すると，日本語の詳細解説HTMLを生成するツール．
[Claude Code](https://claude.ai/code) のスラッシュコマンドとして動作します．

## 必要なもの

- [Claude Code](https://claude.ai/code)（Claude へのアクセス権が必要）
- [uv](https://docs.astral.sh/uv/)（Python パッケージ管理）

## セットアップ

```bash
git clone https://github.com/<your-username>/interpret-paper.git
cd interpret-paper
uv sync
```

その後，Claude Code でこのディレクトリを開くと `/interpret` コマンドが自動的に登録されます．

## 使い方

Claude Code のチャット入力欄で `/interpret` と入力すると候補として表示されます．

```
/interpret https://arxiv.org/abs/1706.03762
/interpret papers/adam.pdf
/interpret --select
```

自然言語でも同様に動作します：

```
この論文を解説して: https://arxiv.org/abs/1706.03762
```

arXiv URL は abs ページ（`arxiv.org/abs/XXXX`）を指定してください．HTML版 → PDF の順に自動で取得を試みます．

## 出力

`output/` に HTML ファイルが生成されます．ブラウザで開くだけで数式がレンダリングされます（MathJax，インターネット接続が必要）．

## スラッシュコマンドの仕組み

`.claude/commands/interpret.md` が `/interpret` コマンドの実体です．
Claude Code はプロジェクト内の `.claude/commands/*.md` を自動的にスラッシュコマンドとして登録するため，追加の設定作業は不要です．

## ディレクトリ構成

```
interpret-paper/
├── CLAUDE.md                      # Claude への指示（対象読者・スタイル）
├── pyproject.toml                 # uv 依存関係
├── .claude/
│   ├── commands/
│   │   └── interpret.md           # /interpret スラッシュコマンド
│   └── skills/
│       └── interpret.md           # スキル定義（詳細な手順）
├── templates/document.html        # HTML テンプレート
├── src/pdf_extract.py             # ローカルPDF 構造抽出（PyMuPDF）
├── papers/                        # PDF を置く場所
└── output/                        # 生成 HTML の出力先
```
