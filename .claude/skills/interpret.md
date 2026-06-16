# interpret — 論文解説スキル

論文のURLまたはローカルPDFパスを受け取り、日本語の詳細解説HTMLを `output/` に生成して保存する。

## 起動パターン

```
/interpret <URL>
/interpret <PDFパス>
/interpret --select          # papers/ から選択
```

自然言語での依頼（「この論文を解説して」「解説して:」）でも同様に動作する。

---

## ステップ 1 — 入力解析

- `--select` の場合: `papers/` ディレクトリ内のPDFファイル一覧を表示し，ユーザーに選択させる
- `--detail <level>` が含まれる場合: level を記録する（`low` / `medium` / `high`，デフォルト: `medium`）
- URLの場合: arXiv かどうかを判定（`arxiv.org` を含む）
- ファイルパスの場合: ローカルPDFとして処理

---

## ステップ 2 — コンテンツ取得

### arXiv URL の場合

arXiv ID（`2301.12345` 形式）を抽出し、以下の順に試みる:

1. **ar5iv HTML版**: `https://ar5iv.org/abs/{ID}` を WebFetch
2. **arXiv 公式HTML版**: `https://arxiv.org/html/{ID}` を WebFetch
3. **PDF**: `https://arxiv.org/pdf/{ID}` を WebFetch（テキストのみ抽出）

取得できた時点でそのコンテンツを使う。

### その他URLの場合

WebFetch でそのままアクセスする。PDF URLなら直接取得してテキスト抽出を試みる。

### ローカルPDFの場合

```bash
uv run python src/pdf_extract.py <path>
```

を実行し、JSONとして出力される構造（`title`, `authors`, `sections`）を使用する。

---

## ステップ 3 — 論文構造の把握

取得したコンテンツから以下を識別する:

- 論文タイトル・著者・掲載会議/ジャーナル・年
- Abstract
- 各セクション（Introduction, Related Work, Method, Experiments, Conclusion, Appendix 等）
- セクション内の定理・定義・補題・系・命題・仮定・注意
- アルゴリズム
- 実験結果の重要な数値・表

---

## ステップ 4 — 解説生成

以下のガイドラインで**日本語**の解説を書く:

**対象読者**: 最適化・機械学習分野の大学院生
- 勾配降下法、SGD、ニューラルネット、確率論の基礎は既知とみなす
- 論文固有の手法・証明のアイデア・実験設定を重点的に解説する

**スタイル**:
- 各セクションを `<h2>` で見出しを付ける
- 数式は LaTeX 記法をそのまま使用（例: `$\nabla f(x)$`, `$$\text{...}$$`）
- 定理・定義・補題等は専用HTMLブロックで再現し，その意義と証明のアイデアを説明する
- アルゴリズムは専用ブロックで再現し，各ステップの意味を解説する
- 「～です。～ます。」調で書く
- 重要な洞察や論文の独自性は明示的に指摘する

**解説の粒度**（ステップ1で記録した detail level に従う）:

- **low**: 各セクション 1〜3 段落で要約．定理・定義は HTMLブロックで列挙するが説明は最小限．証明は省略してよい．アルゴリズムは概要のみ．
- **medium**（デフォルト）: 各セクションを段落で解説．全ての重要な定理・定義・補題を HTMLブロックで再現し，意義と証明のアイデアを 2〜4 段落で説明．アルゴリズムは全ステップを説明．
- **high**: 各セクションを最大限に詳細解説．証明を可能な限り展開し，数式変形のステップを丁寧に追う．背景・動機・他手法との比較・直観的説明・具体例も含める．定理ごとに 4 段落以上を目安とする．

**構成**（このHTMLの順序で生成）:

```
1. 概要（論文の貢献を3–5点の箇条書き）
2. Abstract の解説
3. Introduction の解説
4. 各セクションの解説（セクション順に）
5. まとめ（論文の位置づけ・今後の課題）
```

---

## ステップ 5 — HTML生成と保存

1. `templates/document.html` を読み込む
2. 以下のプレースホルダを置換する:

   | プレースホルダ | 内容 |
   |---|---|
   | `{{TITLE}}` | 論文タイトル |
   | `{{AUTHORS}}` | 著者名（カンマ区切り） |
   | `{{VENUE}}` | 会議/ジャーナル名と年（例: NeurIPS 2023） |
   | `{{ORIGINAL_URL}}` | 元のURL（またはローカルパス） |
   | `{{DATE}}` | 今日の日付（YYYY-MM-DD） |
   | `{{CONTENT}}` | 生成した解説HTML（ステップ4の内容） |

3. 出力ファイルパスを決定:
   - arXiv ID がある場合: `output/{ID}.html`
   - それ以外: `output/{タイトルをスラッグ化}.html`（例: `output/attention-is-all-you-need.html`）

4. 完成したHTMLを上記パスに書き込む

5. 完了したら出力ファイルのパスをユーザーに報告する

---

## HTML 要素の書き方（ステップ4で生成するコンテンツ内）

詳細は CLAUDE.md の「HTML 要素リファレンス」を参照。

### ブロック要素の概要

```html
<!-- 定理 -->
<div class="block theorem" id="thm-2-1">
  <div class="block-header">定理 2.1（名称）</div>
  <div class="block-body">内容</div>
</div>

<!-- 証明 -->
<div class="proof">
  <span class="proof-label">証明.</span>
  本文 <span class="qed">□</span>
</div>

<!-- アルゴリズム -->
<div class="algorithm" id="alg-1">
  <div class="algorithm-header">Algorithm 1: 名称</div>
  <div class="algorithm-body">
    <div class="alg-line"><span class="line-num">1:</span><span class="alg-io">Input:</span> ...</div>
    <div class="alg-line"><span class="line-num">2:</span><span class="alg-kw">for</span> ... <span class="alg-kw">do</span></div>
    <div class="alg-line"><span class="line-num">3:</span>&nbsp;&nbsp;&nbsp;&nbsp;...</div>
    <div class="alg-line"><span class="line-num">4:</span><span class="alg-kw">end for</span></div>
  </div>
</div>
```

クラス: `theorem` / `definition` / `lemma` / `corollary` / `proposition` / `remark` / `assumption`
