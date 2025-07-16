# LLM HLE Experiment Environment

## 必要なソフトウェア

- Docker Desktop (Windows/Mac/Linux)
- Git

## 環境構築手順

### 1. リポジトリのクローン
```bash
git clone https://github.com/fregean/llm-hle-experiment.git
cd llm-hle-experiment
```

### 2. 環境変数の設定
```bash
# .env.exampleをコピーして.envファイルを作成
cp .env.example .env

# .envファイルを編集してAPIキーなどを設定
# 例: API_KEY=your_actual_api_key_here

# 設定ファイルをコピー
cp configs/parameters.yml.example configs/parameters.yml
```

プロジェクトルートに`.env`ファイルを作成し、`your_actual_api_key_here`の部分を編集してください。

`configs/parameters.yml`のファイル名と内容を実験用のモデルに合わせて編集してください（例：deepseek_base.yml）。

### 3. Docker環境の起動
```bash
# 初回のみ: コンテナを構築・起動
docker-compose up -d --build

# 2回目以降の起動（既にコンテナを構築済みの場合）: コンテナを起動
docker-compose up -d
```
#### コンテナの起動確認
```bash
docker-compose ps
```

### 4. 使用方法

#### Jupyter Notebookの使用
```bash
# Jupyter Notebookにアクセス
# http://localhost:8888
```

#### Pythonスクリプトの実行
```bash
# コンテナ内でbashを起動
docker-compose exec app bash
# コンテナ内のbashシェルに入ります（root@container_id:/app#）

# 環境の動作テストを実行（初めて使用する際にお試し実行）
python src/check_env.py

# 動作確認後、元のターミナルに戻る
exit
```

### 5. 依存関係の管理

新しいPythonパッケージを`requirements.txt`に追加した後：
```bash
# コンテナを停止
docker-compose down
# 依存関係を反映してコンテナを再構築・起動
docker-compose up -d --build
```

### 6. 環境変数の変更

`.env`ファイルを変更した後：
```bash
# コンテナを停止
docker-compose down
# 環境変数を反映してコンテナを再起動
docker-compose up -d
```

### 7. 停止・削除
```bash
# 停止
docker-compose down

# 完全削除（データも含む）
docker-compose down -v
```

## ディレクトリ構成

```
├── configs/                    # 設定ファイル
│   ├── parameters.yml.example # 設定ファイルテンプレート
│   └── prompts/                # システムプロンプト
│       ├── em_system_prompt.yml # Exact Match用プロンプト
│       └── mc_system_prompt.yml # Multiple Choice用プロンプト
├── data/                       # データファイル (Git管理対象外)
│   └── .gitkeep
├── notebooks/                  # Jupyter Notebook
│   └── .gitkeep
├── outputs/                    # 出力ファイル (Git管理対象外)
│   ├── models/                 # 学習済みモデル
│   │   └── .gitkeep
│   └── results/                # 実験結果
│       └── .gitkeep
├── scripts/                    # スクリプトファイル
│   └── .gitkeep
├── src/                        # ソースコード
│   ├── __init__.py
│   ├── data_loader.py          # データ読み込み・前処理
│   ├── evaluate.py             # モデル評価
│   ├── model_handler.py        # モデル管理・推論
│   ├── check_env.py            # docker環境動作確認
│   └── utils.py                # ユーティリティ関数
├── .env.example                # 環境変数テンプレート
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── docker-compose.gpu.yml      # GPU対応設定
└── requirements.txt
```

## トラブルシューティング

### ポートが使用中の場合
```bash
# 使用中のポートを確認
docker-compose ps

# 異なるポートを使用する場合は docker-compose.yml を編集
```

### ディスク容量不足エラー
```bash
# Dockerのディスク使用量確認
docker system df

# 現在のコンテナで使用中のイメージを確認
docker ps -a

# 段階的クリーンアップ
docker image prune -a -f     # 既存コンテナで使用されていないイメージを削除
docker builder prune -a -f   # ビルドキャッシュを削除
```