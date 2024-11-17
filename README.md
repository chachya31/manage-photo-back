# manage-photo

## 目次


### 起動手順
- Python 仮想環境構築
  - Terminal を開く
  - 下記コマンドを実行して、それぞれの仮想環境を作成する
  ```bash
  python -m venv venv 
  source venv/Scripts/activate
  ```
- 起動
  ```
  cd src
  uvicorn main:app --reload
  ```
