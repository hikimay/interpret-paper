# interpret-paper

論文（arXiv URL、その他URL、ローカルPDF）を受け取り、日本語の詳細解説HTMLを生成するプロジェクト。

## 使い方

チャットで自然に依頼するか、`/interpret` スキルを呼び出す：

```
この論文を解説して: https://arxiv.org/abs/1706.03762
/interpret https://arxiv.org/abs/1706.03762
/interpret papers/adam.pdf
/interpret --select        # papers/ から対話的に選択
```

## 対象読者と解説スタイル

- 最適化・機械学習分野の大学院生を想定
- 勾配降下法・確率的最適化・ニューラルネット等の基礎知識は既知とみなす
- 論文固有の手法・定理・アルゴリズム・証明のアイデアを中心に解説する
- 冗長な説明は避け、重要な点を簡潔・正確に書く
- 数式は LaTeX 記法をそのまま使用（MathJax でレンダリングされる）

## URL 処理の優先順位

1. **arXiv** (`arxiv.org/abs/XXXX` or `arxiv.org/pdf/XXXX`)
   1. `https://ar5iv.org/abs/XXXX` — HTML版（数式精度が高い）
   2. `https://arxiv.org/html/XXXX` — arXiv 公式HTML版
   3. `https://arxiv.org/pdf/XXXX` — PDFフォールバック
2. **その他のURL** (OpenReview / PMLR / 直接PDFリンク等) — WebFetch でそのまま取得
3. **ローカルPDF** — `uv run python src/pdf_extract.py <path>` で抽出しJSON取得

## ファイル構成

| パス | 役割 |
|---|---|
| `templates/document.html` | HTMLテンプレート（プレースホルダ付き） |
| `src/pdf_extract.py` | ローカルPDF構造抽出スクリプト |
| `papers/` | ローカルPDF置き場 |
| `output/` | 生成HTML置き場 |
| `pyproject.toml` | uv パッケージ管理 |

出力ファイル名: arXiv IDが使える場合は `output/2301.12345.html`、それ以外はタイトルをスラッグ化した名前。

## HTML 要素リファレンス

テンプレートのプレースホルダ: `{{TITLE}}` `{{AUTHORS}}` `{{VENUE}}` `{{ORIGINAL_URL}}` `{{DATE}}` `{{CONTENT}}`

### 定理・定義・補題・系・命題・注意・仮定

```html
<div class="block theorem" id="thm-2-1">
  <div class="block-header">定理 2.1（収束定理）</div>
  <div class="block-body">
    仮定 A1–A3 のもとで、$\eta_t = O(1/\sqrt{t})$ とすると、
    $$\min_{t \leq T} \mathbb{E}[\|\nabla f(x_t)\|^2] = O(1/\sqrt{T})$$
    が成立する。
  </div>
</div>
```

クラス名: `theorem` / `definition` / `lemma` / `corollary` / `proposition` / `remark` / `assumption`

### 証明

```html
<div class="proof">
  <span class="proof-label">証明.</span>
  Lipschitz 連続性から ...
  <span class="qed">□</span>
</div>
```

### アルゴリズム

```html
<div class="algorithm" id="alg-1">
  <div class="algorithm-header">Algorithm 1: SGD with Momentum</div>
  <div class="algorithm-body">
    <div class="alg-line"><span class="line-num">1:</span><span class="alg-io">Input:</span> 初期点 $x_0$、学習率 $\eta$</div>
    <div class="alg-line"><span class="line-num">2:</span><span class="alg-kw">for</span> $t = 0, \ldots, T-1$ <span class="alg-kw">do</span></div>
    <div class="alg-line"><span class="line-num">3:</span>&nbsp;&nbsp;&nbsp;&nbsp;$x_{t+1} \leftarrow x_t - \eta \nabla f(x_t)$ &nbsp;<span class="alg-comment">// 更新</span></div>
    <div class="alg-line"><span class="line-num">4:</span><span class="alg-kw">end for</span></div>
  </div>
</div>
```

キーワードクラス: `alg-kw`（for/while/if/else/return）、`alg-io`（Input/Output）、`alg-comment`（コメント）、`alg-fn`（関数名）
