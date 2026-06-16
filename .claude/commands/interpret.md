以下の論文を解説してください: $ARGUMENTS

CLAUDE.md の指示と `.claude/skills/interpret.md` の手順に従って処理してください。

`$ARGUMENTS` に `--detail <level>` が含まれる場合，その粒度で解説を生成してください。
指定がない場合は `medium` をデフォルトとします。

- `--detail low` : 各セクションを簡潔に要約（1〜3 段落程度）
- `--detail medium` : 各セクションを丁寧に解説．定理・証明のアイデア・アルゴリズムの各ステップを説明
- `--detail high` : 各セクションを最大限に詳細解説．証明の展開・数式変形のステップ・背景・他手法との比較を含む
