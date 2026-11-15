# 1. Python とは・準備

## この章でわかること

- Python の特徴と、何に使えるか
- Ubuntu と VS Code で Python を書いて動かす準備（仮想環境）
- エラーの読み方

## Python とは

| 特徴 | 説明 |
| --- | --- |
| 読みやすい | 文の終わりの `;` や `{ }` がなく、字下げ（インデント）でまとまりを表す |
| すぐ動く | コンパイルせずに、書いたものをそのまま動かせる（インタプリタ） |
| ライブラリが多い | データ分析（NumPy・pandas）、グラフ（matplotlib）、機械学習（scikit-learn・PyTorch）、ラズパイの制御など |

その代わり、C++ より動きは遅くなります。重い計算は、中身が C や C++ で書かれたライブラリ（NumPy など）にまかせます。

この教科書のあとに、「機械学習の教科書」「統計の教科書」に進めます。C++ とのちがいは、「C++ の教科書」の付録A にまとめています。

## 準備（Ubuntu・VS Code）

### Python と仮想環境

Ubuntu には、はじめから `python3` が入っています。

```bash
python3 --version
sudo apt install python3-venv python3-pip
```

ライブラリは、フォルダごとの**仮想環境**（venv）に入れます。今の Ubuntu では、仮想環境の外で `pip install` すると `externally-managed-environment` というエラーになります（システムの Python をこわさないため）。

```bash
mkdir -p ~/apps/py-study
cd ~/apps/py-study
python3 -m venv .venv            # .venv というフォルダに仮想環境を作る
source .venv/bin/activate        # 仮想環境に入る（行の頭に (.venv) が付く）
pip install numpy pandas matplotlib
deactivate                       # 仮想環境から出る
```

仮想環境に入っている間は、`python` と `pip` がこの仮想環境のものになります。

### VS Code

1. `code .` で、フォルダを VS Code で開く
2. 拡張機能で「Python」（Microsoft）を入れる
3. **Ctrl + Shift + P** →「Python: Select Interpreter」→ `.venv` のものを選ぶ。これで VS Code が仮想環境を使う
4. `hello.py` を作って、次の1行を書いて保存する

```python
print("こんにちは、Python！")
```

5. 右上の ▶ を押すか、ターミナル（**Ctrl + `**）で実行する

```bash
python hello.py
```

```text
こんにちは、Python！
```

### 対話モード

ターミナルで `python`（仮想環境の外では `python3`）とだけ打つと、1行ずつ試せる**対話モード**になります。

```text
>>> 1 + 2
3
>>> exit()
```

### Jupyter ノートブック

コードと結果・グラフを交互に並べて書ける `.ipynb` のファイルです。VS Code で「Jupyter」拡張機能を入れ、`pip install ipykernel` をしてから、`.ipynb` のファイルを作ると使えます。データ分析で試しながら進めるのに向いています。

## エラーの読み方

```text
Traceback (most recent call last):
  File "/home/user/apps/py-study/hello.py", line 3, in <module>
    print(total / count)
          ~~~~~~^~~~~~~
ZeroDivisionError: division by zero
```

- **一番下の行**がエラーの種類と理由（ここでは「0 で割った」）
- その上が、エラーが起きた**ファイルと行**（3 行目）
- 関数の中で起きたときは、呼んだ順に上から並ぶ。自分のファイルの、一番下の行から見る

よくあるエラーは6章にまとめています。

## まとめ

- Python は読みやすく、すぐ動き、データ分析のライブラリが多い
- ライブラリは仮想環境（`python3 -m venv .venv` → `source .venv/bin/activate` → `pip install`）に入れる
- VS Code では「Python: Select Interpreter」で `.venv` を選ぶ
- エラーは一番下の行から読む

## 練習問題

```quiz
Q: 仮想環境 `.venv` を作るコマンドは `python3 -m` のあとに何と書きますか。
A: venv .venv | venv
E: `python3 -m venv .venv` → `source .venv/bin/activate` → `pip install` の順です。

Q: 仮想環境を使い始める（有効にする）コマンドは `source` のあとに何と書きますか。
A: .venv/bin/activate
E: 有効になると、プロンプトの頭に `(.venv)` が付きます。

Q: ライブラリを入れるコマンドは何ですか（例: `??? install numpy`）。
A: pip | pip3
E: 仮想環境を有効にしてから `pip install` します。

Q: Python のエラーの表示は、上と下のどちらの行から読みますか。
A: 下 | 一番下 | いちばん下 | 下から
E: 一番下の行に、エラーの種類と理由が書いてあります。
```
