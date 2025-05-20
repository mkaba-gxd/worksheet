# worksheet マニュアル
DRY工程作業で使用するワークシートの新規作成、シートの追加、解析の進捗確認

## 0\. 準備
エイリアスを作成する（初回のみ）。\
~/bin フォルダを作成し、以下のコマンドを記載したテキストファイル worksheet を作成しておく。\
エイリアスを作成しない場合は、singularity でコンテナを指定して実行する。
```
singularity exec --disable-cache --bind /data1 /data1/labTools/labTools.sif python /data1/labTools/worksheet/latest/worksheet.py $@
```
helpページを表示してエイリアスの設定を確認する。以下が表示されればOK。
```
$ worksheet --help
version: v3.0.0
usage: worksheet.py [-h] [--version] {create,CR,check,CH,addition,ADD,remove,RM,reset,RE} ...

Created and added worksheet and checked processes.

positional arguments:
  {create,CR,check,CH,addition,ADD,remove,RM,reset,RE}
    create (CR)         create worksheet
    check (CH)          check progress
    addition (ADD)      additional worksheet
    remove (RM)         delete the analysis results
    reset (RE)          reset database

optional arguments:
  -h, --help            show this help message and exit
  --version, -v         show program's version number and exit
```

## 1\. ワークシートの作成
```
worksheet create -fc <flowcellid>
worksheet CR -fc <flowcellid>
```
オプションの詳細
```
$ worksheet create -h
version: v3.0.0
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
| option         | 概要           |default         |
|:---------------|:---------------|:---------------|
|--flowcellid/-fc |バッチ固有のID。OncoStationに掲載されている9桁の半角英数字 |None|
|--directory/-d   |解析フォルダの親ディレクトリへのパス|/data1/data/result|
|--project_type/-t|解析種別。bath,eWES,WTSから選択する。|both|
|--outdir/-o      |ワークシート出力先ディレクトリへのパス|/data1/work/workSheet|

## 2\. 解析の進捗を確認
```
worksheet check -fc <flowcellid>
worksheet CH -fc <flowcellid>
```
オプションの詳細
```
$ worksheet check -h
version: v3.0.0
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
| option         | 概要           |default         |
|:---------------|:---------------|:---------------|
|--flowcellid/-fc |バッチ固有のID。OncoStationに掲載されている9桁の半角英数字 |None|
|--directory/-d   |解析フォルダの親ディレクトリへのパス|/data1/data/result|
|--project_type/-t|解析種別。bath,eWES,WTSから選択する。|both|
|--linkDir/-l     |PDFレポートのリンク先ディレクトリへのパス|/data1/work/report|
|--novadir/-n     |NGSデータ転送先フォルダ|/data1/gxduser/novaseqx|

## 3\. シートの追加
```
worksheet addition -fc <flowcellid>
worksheet ADD -fc <flowcellid>
```
オプションの詳細
```
$ worksheet addition -h
version: v3.0.0
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
| option         | 概要           |default         |
|:---------------|:---------------|:---------------|
|--flowcellid/-fc |バッチ固有のID。OncoStationに掲載されている9桁の半角英数字 |None|
|--directory/-d   |解析フォルダの親ディレクトリへのパス|/data1/data/result|
|--project_type/-t|解析種別。bath,eWES,WTSから選択する。|both|
|--outdir/-o      |ワークシート出力先ディレクトリへのパス|/data1/work/workSheet|

## 4\. 解析結果の削除
指定された SampleID について、解析フォルダに格納されているsummaryファイルの不要な行を削除する。
```
worksheet remove --sample SAMPLE
worksheet RM -s <sampleid>
```
オプションの詳細
```
$ worksheet remove -h
version: v3.0.0
usage: worksheet.py remove [-h] --sample SAMPLE [--analysis_dir ANALYSIS_DIR]

optional arguments:
  -h, --help            show this help message and exit
  --sample SAMPLE, -s SAMPLE
                        sample id (default: None)
  --analysis_dir ANALYSIS_DIR, -d ANALYSIS_DIR
                        parent analytical directory (default: /data1/data/result)
```
| option           | 概要           |default         |
|:-----------------|:---------------|:---------------|
|--sample/-s       |sample ID       |None |
|--analysis_dir/-d |解析フォルダの親ディレクトリへのパス|/data1/data/result|

## 5\. データベースのリセット
指定された SampleID について、データベースに登録された解析結果を削除し、解析フォルダにPDF/JSONが存在する場合はリネームする。\
--roll_back オプションで解析ステータスを101(解析中)に変更する。\
指定がない場合は100(解析前)に変更するのでcronによる再解析が行われる。
```
worksheet reset --sample <sampleid> (--roll_back)
worksheet RE -s <sampleid> (--roll_back)
```
オプションの詳細
```
$ worksheet reset -h
version: v3.0.0
usage: worksheet.py reset [-h] --sample SAMPLE [--roll_back] [--analysis_dir ANALYSIS_DIR]

optional arguments:
  -h, --help            show this help message and exit
  --sample SAMPLE, -s SAMPLE
                        sample id (default: None)
  --roll_back, -r       Set the status to 101 (Analysis in progress). If not specified, set the status to 100 (ready for analysis).
  --analysis_dir ANALYSIS_DIR, -d ANALYSIS_DIR
                        parent analytical directory (default: /data1/data/result)
```
| option           | 概要           |default         |
|:-----------------|:---------------|:---------------|
|--sample/-s       |sample ID       |None |
|--roll_back/-r    |analysis statusを「解析中」にセットする|解析前|
|--analysis_dir/-d |解析フォルダの親ディレクトリへのパス|/data1/data/result|

