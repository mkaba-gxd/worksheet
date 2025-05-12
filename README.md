# worksheet マニュアル
DRY工程で使用する worksheet ツールの使用方法

## 0\. 準備
エイリアスを作成する。\
~/bin フォルダを作成し、以下のコマンドを記載したテキストファイル worksheet を作成しておく。
```
singularity exec --disable-cache --bind /data1 /data1/labTools/labTools.sif python /data1/labTools/worksheet/latest/worksheet.py $@
```

## 1\. ワークシートの作成
```
worksheet create -fc <flowcellid>
worksheet CR -fc <flowcellid>
```

## 2\. 解析の進捗を確認
```
worksheet check -fc <flowcellid>
worksheet CH -fc <flowcellid>
```

## 3\. シートの追加
```
worksheet addition -fc <flowcellid>
worksheet ADD -fc <flowcellid>
```
