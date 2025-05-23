# worksheet マニュアル
DRY工程作業で使用するワークシートの新規作成、シートの追加、解析の進捗確認

| command      | 概要                                                |
|:-------------|:---------------------------------------------------|
|create, CR    |ワークシートの新規作成                                |
|check, CH     |解析の進捗確認                                       |
|addition, ADD |ワークシートに解析情報を記載したシートを追加            |
|remove, RM    |解析結果の編集(Summaryファイルの行削除)とrerun.shの作成 |
|reset, RE     |DBに登録された解析結果を削除しanalysis statusを変更する |

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
\<OUTDIR\>にワークシートを作成する。同名のファイルがある場合は上書きするかどうか選択する。\
\<DIRECTORY\>に解析フォルダが作成されてから実行すること。
```
worksheet create -fc <flowcellid>
worksheet CR -fc <flowcellid>
```
### オプションの詳細
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
| option          | 概要           |default         |
|:----------------|:---------------|:---------------|
|--flowcellid/-fc |バッチ固有のID。OncoStationに掲載されている9桁の半角英数字   |None |
|--directory/-d   |解析フォルダの親ディレクトリへのパス  |/data1/data/result    |
|--project_type/-t|解析種別。bath,eWES,WTSから選択する。 |both                  |
|--outdir/-o      |ワークシート出力先ディレクトリへのパス|/data1/work/workSheet |

## 2\. 解析の進捗確認
rawdataに格納されているSampleSheetの内容と、DBに登録されている検体情報が一致することを確認する。\
analysis statusを調べて解析の進捗を表示する。\
report.jsonとreport.pdfが作成されていることを確認する。\
\<LINKDIR\>に作成済みreport.pdfのシンボリックリンクを作成する。
```
worksheet check -fc <flowcellid>
worksheet CH -fc <flowcellid>
```
### オプションの詳細
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
| option          | 概要           |default         |
|:----------------|:---------------|:---------------|
|--flowcellid/-fc |バッチ固有のID。OncoStationに掲載されている9桁の半角英数字 |None |
|--directory/-d   |解析フォルダの親ディレクトリへのパス |/data1/data/result      |
|--project_type/-t|解析種別。bath,eWES,WTSから選択する。|both                    |
|--linkDir/-l     |PDFレポートのリンク先ディレクトリへのパス|/data1/work/report  |
|--novadir/-n     |NGSデータ転送先フォルダ              |/data1/gxduser/novaseqx |

## 3\. シートの追加
作成済のワークシートにQC情報や、Summaryフォルダに格納された summarized.\*.tsv からレポートに掲載される変異を検査項目ごとにまとめたシートを追加する。\
解析途中の検体があった場合は、操作の継続を聞かれるので選択する。\
**継続する場合は、解析中検体の情報は記載されない**ので、全検体の解析が終了した後に再度実行すること。
```
worksheet addition -fc <flowcellid>
worksheet ADD -fc <flowcellid>
```
### オプションの詳細
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
| option          | 概要           |default         |
|:----------------|:---------------|:---------------|
|--flowcellid/-fc |バッチ固有のID。OncoStationに掲載されている9桁の半角英数字  |None |
|--directory/-d   |解析フォルダの親ディレクトリへのパス  |/data1/data/result   |
|--project_type/-t|解析種別。bath,eWES,WTSから選択する。 |both                 |
|--outdir/-o      |ワークシート出力先ディレクトリへのパス|/data1/work/workSheet|

## 4\. 解析結果の削除
指定された SampleID について、解析フォルダに格納されているsummaryファイルの不要な行を削除する。\
対話型プログラムなので、表示される内容に応じて編集する内容を入力する。\
解析フォルダ内データの書き換えを行うので **gxd_pipeline ユーザーで実行すること。**
```
worksheet remove --sample SAMPLE
worksheet RM -s <sampleid>
```
### オプションの詳細
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
|--sample/-s       |sample ID       |None            |
|--analysis_dir/-d |解析フォルダの親ディレクトリへのパス |/data1/data/result |

### 削除できる項目
|test_type |item                       |指定方法        
|:---------|:--------------------------|:---------------------------------------------------|
|eWES      |SNV (SNV & InDel)          |gene,HGVSc,HGVSp (HGVSpがハイフン "-" の場合は空欄) |
|eWES      |CNV (Copy Number Variants) |gene1,gene2,... (カンマ区切りで複数指定可)          |
|WTS       |FS (Fusion)                |gene_1,gene_2,chr1:position1,chr2:position2         |
|WTS       |AS (Alternative Splicing)  |[EGFR,MET,AR]  (カンマ区切りで複数指定可)           |

- Genomic Signatures(MSI/TMB), SNV/InDel with Insufficient Depth は未対応。
- CNV は Intermediate の遺伝子も含めて指定可。

## 5\. データベースのリセット
指定された SampleID について、データベースに登録された解析結果を削除し、解析フォルダにPDF/JSONが存在する場合はリネームする。\
--status オプションで解析ステータスを変更する。 100:解析前, 101:解析中, 102:解析完了 \
指定しない場合は解析ステータスは変更しない。\
**100を指定した場合はcronによる再解析が行われる。**
```
worksheet reset --sample <sampleid> (--roll_back)
worksheet RE -s <sampleid> (--roll_back)
```
### オプションの詳細
```
$ worksheet reset -h
version: v3.0.0
usage: worksheet.py reset [-h] --sample SAMPLE [--status {100,101,102,None}] [--analysis_dir ANALYSIS_DIR]

optional arguments:
  -h, --help            show this help message and exit
  --sample SAMPLE, -s SAMPLE
                        sample id (default: None)
  --status {100,101,102,None}, -t {100,101,102,None}
                        Specify the analysis status. If not changed, not specified. (default: None)
  --analysis_dir ANALYSIS_DIR, -d ANALYSIS_DIR
                        parent analytical directory (default: /data1/data/result)
```
| option           | 概要           |default         |
|:-----------------|:---------------|:---------------|
|--sample/-s       |sample ID       |None            |
|--status/-t       |analysis status を指定する。100:解析前, 101:解析中, 102:解析完了, None(オプションなし):変更しない |None |
|--analysis_dir/-d |解析フォルダの親ディレクトリへのパス |/data1/data/result |

