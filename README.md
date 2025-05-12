# worksheet マニュアル
DRY工程作業で使用するワークシートの新規作成、シートの追加、解析の進捗確認

## 0\. 準備
エイリアスを作成する（初回のみ）。\
~/bin フォルダを作成し、以下のコマンドを記載したテキストファイル worksheet を作成しておく。
```
singularity exec --disable-cache --bind /data1 /data1/labTools/labTools.sif python /data1/labTools/worksheet/latest/worksheet.py $@
```
helpページの表示を行い、エイリアスの設定を確認する。
```
worksheet -h
usage: worksheet.py [-h] {create,CR,check,CH,addition,ADD} ...

Multi-command script

positional arguments:
  {create,CR,check,CH,addition,ADD}
    create (CR)         create worksheet
    check (CH)          check progress
    addition (ADD)      additional worksheet

optional arguments:
  -h, --help            show this help message and exit
```

## 1\. ワークシートの作成
```
worksheet create -fc <flowcellid>
worksheet CR -fc <flowcellid>
```
オプションの詳細
```
$ worksheet create -h
usage: worksheet.py create [-h] --flowcellid FLOWCELLID [--directory DIRECTORY] [--project_type {both,WTS,eWES}] [--outdir OUTDIR]

optional arguments:
  -h, --help            show this help message and exit
  --flowcellid FLOWCELLID, -fc FLOWCELLID
                        flowcell id (default: None)
  --directory DIRECTORY, -d DIRECTORY
                        parent analytical directory (default: /data1/data/result)
  --project_type {both,WTS,eWES}, -t {both,WTS,eWES}
                        project type (default: both)
  --outdir OUTDIR, -o OUTDIR
                        output directory path (default: /data1/work/workSheet)
```

## 2\. 解析の進捗を確認
```
worksheet check -fc <flowcellid>
worksheet CH -fc <flowcellid>
```
オプションの詳細
```
$ worksheet check -h
usage: worksheet.py check [-h] --flowcellid FLOWCELLID [--directory DIRECTORY] [--project_type {both,WTS,eWES}] [--linkDir LINKDIR] [--novadir NOVADIR]

optional arguments:
  -h, --help            show this help message and exit
  --flowcellid FLOWCELLID, -fc FLOWCELLID
                        flowcell id (default: None)
  --directory DIRECTORY, -d DIRECTORY
                        parent analytical directory (default: /data1/data/result)
  --project_type {both,WTS,eWES}, -t {both,WTS,eWES}
                        project type (default: both)
  --linkDir LINKDIR, -l LINKDIR
                        Linked directory of report files (default: /data1/work/report)
  --novadir NOVADIR, -n NOVADIR
                        novaseq directory (default: /data1/gxduser/novaseqx)
```

## 3\. シートの追加
```
worksheet addition -fc <flowcellid>
worksheet ADD -fc <flowcellid>
```
オプションの詳細
```
$ worksheet addition -h
usage: worksheet.py addition [-h] --flowcellid FLOWCELLID [--directory DIRECTORY] [--project_type {both,WTS,eWES}] [--outdir OUTDIR]

optional arguments:
  -h, --help            show this help message and exit
  --flowcellid FLOWCELLID, -fc FLOWCELLID
                        flowcell id (default: None)
  --directory DIRECTORY, -d DIRECTORY
                        parent analytical directory (default: /data1/data/result)
  --project_type {both,WTS,eWES}, -t {both,WTS,eWES}
                        project type (default: both)
  --outdir OUTDIR, -o OUTDIR
                        output directory path (default: /data1/work/workSheet)
```
