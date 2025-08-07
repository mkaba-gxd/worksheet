# worksheet ツール
CAP検査（eWES/WTS）DRY工程作業で使用するワークシートの新規作成、シートの追加、解析の進捗確認を行う。
指定されたflowcell IDやsample IDを用いてデータベースで検索し、検体情報を取得するため、データベースに登録がない検体に対しては実行できません。\
**また、データベースの設計内容が不明なため、データベース検索時に想定外の動作を行う可能性があります。**
| command              | 概要                                                     |
|:---------------------|:---------------------------------------------------------|
|[create, CR](#CR)     |ワークシートの新規作成                                    |
|[check, CH](#CH)      |解析の進捗確認                                            |
|[addition, ADD](#ADD) |ワークシートに解析情報を記載したシートを追加              |
|[remove, RM](#RM)     |解析結果の編集（Summaryファイルの行削除）とrerun.shの作成 |
|[reset, RE](#RE)      |データベースに登録済みの解析結果の削除とanalysis statusの変更 |
|[link, LNK](#LNK)     |OncoStationで作成されたPDFレポートのリンクを作成する      |

## エイリアスの作成 ※初回のみ 
~/bin フォルダ直下に以下のコマンドを記載したテキストファイル worksheet を作成し、実行権限を付与する。\
（gxd_pipeline, guest_user ユーザーには実装済み）\
エイリアスを作成しない場合は、singularity でコンテナとスクリプトファイルを指定して実行する。

```
singularity exec --disable-cache --bind /data1 /data1/labTools/labTools.sif python /data1/labTools/worksheet/latest/worksheet.py $@
```
helpページを表示してエイリアスの設定を確認する。以下が表示されればOK。
```
$ worksheet --help
version: v3.1.0
usage: worksheet.py [-h] [--version] {create,CR,check,CH,addition,ADD,remove,RM,reset,RE,link,LNK} ...

Created and added worksheet and checked processes.

positional arguments:
  {create,CR,check,CH,addition,ADD,remove,RM,reset,RE,link,LNK}
    create (CR)         create worksheet
    check (CH)          check progress
    addition (ADD)      additional worksheet
    remove (RM)         delete the analysis results
    reset (RE)          reset database
    link (LNK)          create report.pdf link

optional arguments:
  -h, --help            show this help message and exit
  --version, -v         show program's version number and exit
```

<a id="CR"></a>
## 1\. ワークシートの作成
\<OUTDIR\>にワークシートを作成する。同名のファイルがある場合は上書きするかどうか選択する。\
\<DIRECTORY\>に解析フォルダが作成されてから実行すること。
```
worksheet create --flowcellid <flowcellid>
worksheet CR -fc <flowcellid>
```

<details>
  <summary> 
    More Details
  </summary>

### オプションの詳細
```
$ worksheet create --help
version: v3.1.0
usage: worksheet.py create [-h] --flowcellid FLOWCELLID [--directory DIRECTORY] 
                           [--project_type {both,WTS,eWES}] [--outdir OUTDIR]

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
| option           |required | 概要           |default         |
|:-----------------|:-------:|:---------------|:---------------|
|--flowcellid/-fc  |True     |バッチ固有のID。OncoStationに掲載されている9桁の半角英数字   |None |
|--directory/-d    |False    |解析フォルダの親ディレクトリへのパス  |/data1/data/result    |
|--project_type/-t |False    |解析種別。both,eWES,WTSから選択する  |both                  |
|--outdir/-o       |False    |ワークシート出力先ディレクトリへのパス|/data1/work/workSheet |

</details>

<a id="CH"></a>
## 2\. 解析の進捗確認
- データベースに登録されている検体情報とNGSデータフォルダに格納されているSampleSheet.csvの内容が合致しているかを確認する
- データベースのANAL_STATUSの値を基に解析の進捗を報告する（100:registered, 101:in progress, 102:finished, 104:reanalysis）
- report.json, report.pdfを作成済の検体数と、未作成の検体のSample IDを表示する
- 作成済のreport.pdfのシンボリックリンクを作成する
```
worksheet check --flowcellid <flowcellid>
worksheet CH -fc <flowcellid>
```
<details>
  <summary> 
    More Details
  </summary>
  
### オプションの詳細
```
$ worksheet check --help
version: v3.1.0
usage: worksheet.py check [-h] --flowcellid FLOWCELLID [--directory DIRECTORY] [--project_type {both,WTS,eWES}] [--novadir NOVADIR]
                          [--linkDir LINKDIR]

optional arguments:
  -h, --help            show this help message and exit
  --flowcellid FLOWCELLID, -fc FLOWCELLID
                        flowcell id (default: None)
  --directory DIRECTORY, -d DIRECTORY
                        parent analytical directory (default: /data1/data/result)
  --project_type {both,WTS,eWES}, -t {both,WTS,eWES}
                        project type (default: both)
  --novadir NOVADIR, -n NOVADIR
                        novaseq directory (default: /data1/gxduser/novaseqx)
  --linkDir LINKDIR, -l LINKDIR
                        Linked directory of report files (default: /data1/work/report)
```
| option           |required | 概要           |default         |
|:-----------------|:-------:|:---------------|:---------------|
|--flowcellid/-fc  |True     |バッチ固有のID。OncoStationに掲載されている9桁の半角英数字 |None |
|--directory/-d    |False    |解析フォルダの親ディレクトリへのパス |/data1/data/result      |
|--project_type/-t |False    |解析種別。both,eWES,WTSから選択する  |both                    |
|--novadir/-n      |False    |NGSデータ転送先フォルダ              |/data1/gxduser/novaseqx |
|--linkDir/-l      |False    |PDFレポートのリンク先ディレクトリへのパス |/data1/work/report |

</details>

<a id="ADD"></a>
## 3\. シートの追加
作成済のワークシートに以下の情報を項目別にまとめたシートを追加する。
- QC情報（OncoStationに掲載される項目。WETのQCも含む）
- レポートに記載される解析結果（Summaryフォルダに格納された summarized.\*.tsv から収集）\
  
createコマンドでワークシートを作成してから実行すること。
```
worksheet addition --flowcellid <flowcellid>
worksheet ADD -fc <flowcellid>
```
<details>
  <summary> 
    More Details
  </summary>
  
### オプションの詳細
```
$ worksheet addition --help
version: v3.1.0
usage: worksheet.py addition [-h] --flowcellid FLOWCELLID [--directory DIRECTORY] [--project_type {both,WTS,eWES}]
                             [--outdir OUTDIR]

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
| option           |required | 概要           |default         |
|:-----------------|:-------:|:---------------|:---------------|
|--flowcellid/-fc  |True     |バッチ固有のID。OncoStationに掲載されている9桁の半角英数字   |None |
|--directory/-d    |False    |解析フォルダの親ディレクトリへのパス  |/data1/data/result    |
|--project_type/-t |False    |解析種別。both,eWES,WTSから選択する   |both                  |
|--outdir/-o       |False    |ワークシート出力先ディレクトリへのパス|/data1/work/workSheet |

</details>

解析途中の検体があった場合は、操作の継続を聞かれるので選択する。\
**継続する場合は、解析中の検体情報は記載されない**ので、全検体の解析が終了した後に再度実行してQC情報が確認できるようにしておく。\
なお、再実行時した場合は work_sheet, sample_info 以外のシートは上書きされる。

<a id="RM"></a>
## 4\. 解析結果の編集（削除）
指定された sample ID について、解析フォルダに格納されているsummaryファイルの不要な行を削除する。\
**この機能だけではデータベースの登録内容は変更されません（＝OSTレポートも変更されません）。** [5.データベースのリセット](#RE) で当該検体の変異情報をデータベースから削除し、手作業またはcronの自動実行を利用して report_json 工程を行い、データベースへ変異を登録すること。\
解析フォルダ内データの書き換えを行うので **gxd_pipeline ユーザーで実行すること。** \
```
worksheet remove --sample <sample ID>
worksheet RM -s <sample ID>
```
<details>
  <summary> 
    More Details
  </summary>
  
### オプションの詳細
```
$ worksheet remove --help
version: v3.1.0
usage: worksheet.py remove [-h] --sample SAMPLE [--analysis_dir ANALYSIS_DIR]

optional arguments:
  -h, --help            show this help message and exit
  --sample SAMPLE, -s SAMPLE
                        sample id (default: None)
  --analysis_dir ANALYSIS_DIR, -d ANALYSIS_DIR
                        parent analytical directory (default: /data1/data/result)
```
| option           |required | 概要           |default         |
|:-----------------|:-------:|:---------------|:---------------|
|--sample/-s       |True     |sample ID       |None            |
|--analysis_dir/-d |False    |解析フォルダの親ディレクトリへのパス |/data1/data/result |

### 削除できる項目
|解析種別 |item                       |指定方法        
|:-------|:--------------------------|:-------------------------------------------------|
|eWES    |SNV (SNV & InDel)          |gene,HGVSc,HGVSp (HGVSpがハイフン "-" の場合は空欄) |
|eWES    |CNV (Copy Number Variants) |gene1,gene2,... (カンマ区切りで複数指定可)          |
|WTS     |FS (Fusion)                |gene_1,gene_2,chr1:position1,chr2:position2       |
|WTS     |AS (Alternative Splicing)  |[EGFR,MET,AR] から選択 (カンマ区切りで複数指定可)    |

- Genomic Signatures(MSI/TMB), SNV/InDel with Insufficient Depth は未対応。
- CNV は Intermediate の遺伝子も含めて指定可。

対話型プログラムなので、表示される内容に応じて編集する内容を入力する。\
可能な編集は行削除（変異の削除）のみなので、解析結果内容の一部を修正する場合はsummaryファイルを**手作業で**編集してレポートの再作成を実施する。
[手順はこちら](https://github.com/mkaba-gxd/special-case/blob/main/README.md#case4-解析結果の修正とレポートの再作成手作業)

</details>

<a id="RE"></a>
## 5\. データベースのリセット
指定された SampleID について、データベースに登録された解析結果を削除し、解析フォルダにPDF/JSONが存在する場合はリネームする。\
analysis status が 102 の場合は、手作業で report_json 工程を実行してもデータベース登録エラーとなることに注意。
```
worksheet reset --sample <sampleid> --status [100/101/102]
worksheet RE -s <sampleid> -t [100/101/102]
```
<details>
  <summary> 
    More Details
  </summary>

### オプションの詳細
```
$ worksheet reset --help
version: v3.1.0
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
| option           |required | 概要           |default         |
|:-----------------|:-------:|:---------------|:---------------|
|--sample/-s       |True     |sample ID       |None            |
|--status/-t       |False    |analysis status を指定する。100:解析前, 101:解析中, 102:解析完了, None(オプションなし):変更しない |None |
|--analysis_dir/-d |False    |解析フォルダの親ディレクトリへのパス |/data1/data/result |

指定された SampleID が Comfirm 実行済だった場合、**statusは変更しない**。その他の変更を行うかどうか聞かれるので選択する。\
--status オプションで解析ステータスを変更する。 100:解析前, 101:解析中, 102:解析完了 \
**100を指定した場合はcronによる再解析が行われる。** なお、指定しない場合は解析ステータスを変更しない。

</details>

<a id="LNK"></a>
## 6\. PDFレポートファイルのリンク作成
Comfirm済の検体について、OncoStationで作成されたPDFファイルのシンボリックリンクを作成する。
```
worksheet link --flowcellid <flowcellid>
worksheet LNK -fc <flowcellid>
```
<details>
  <summary>
    More Details
  </summary>

### オプションの詳細
```
$ worksheet link --help
version: v3.1.0
usage: worksheet.py link [-h] --flowcellid FLOWCELLID [--directory DIRECTORY] [--project_type {both,WTS,eWES}] [--linkDir LINKDIR]

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
```
| option           |required | 概要           |default         |
|:-----------------|:-------:|:---------------|:---------------|
|--flowcellid/-fc  |True     |バッチ固有のID。OncoStationに掲載されている9桁の半角英数字   |None |
|--directory/-d    |False    |解析フォルダの親ディレクトリへのパス  |/data1/data/result    |
|--project_type/-t |False    |解析種別。both,eWES,WTSから選択する  |both                   |
|--linkDir/-l      |False    |PDFレポートのリンク先ディレクトリへのパス|/data1/work/report |

</details>



