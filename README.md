# worksheet ツール
CAP検査（eWES/WTS）DRY工程作業で使用するワークシートの新規作成、シートの追加、解析の進捗確認を行う。
指定された flowcell ID または sample ID を用いてデータベースを検索して検体情報を取得するため、データベースに登録がない検体に対しては実行できません。\
**このツールは正式な検証を経ていません。** 不具合等が生じた場合は適宜修正するか、手作業で必要なデータの確認・修正等を行い、作業手順書に記入してください。\
**データベースの設計内容が不明なため、データベース検索時に想定外の動作を行う可能性があります。**

| command              | 概要                                                 |
|:---------------------|:-----------------------------------------------------|
|[create, CR](#CR)     |ワークシートの新規作成                                  |
|[check, CH](#CH)      |解析の進捗確認とPipelineで作成されたPDFレポートのリンクを作成する |
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
## 0\. DRY工程の手順
<details>
  <summary> 
    More Details
  </summary>
  
  1. [ワークシートの作成](#CR)\
      → /data1/work/workSheet に \<batch_folder\>.[eWES/WTS].xlsx が作成される
  2. 解析の[進捗を確認](#CH)\
      → /data1/work/report/[eWES/WTS]/\<batch_folder\>/PL/ の下にPipelineで作成されたPDFレポートのリンクが作成される
  3. ワークシートにqc_infoと解析結果の[シートを追加](#ADD)する
  4. ネガコンで変異が検出されなかったことを確認する
  5. ポジコンでワークシートに記載されている変異が検出されていることを確認する\
      該当する変異がレポートに記載されていない場合はGMに報告のうえ、以下の途中ファイルを確認して、記載されていればその旨を作業書に記載する\
     【eWES】/data1/data/result/eWES/\<batch_folder\>/\<ポジコンのSampleID\>/SNV/somatic/\<ポジコンのSampleID\>.target.snv.marked.tsv \
     【WTS】 /data1/data/result/WTS/\<batch_folder\>/\<ポジコンのSampleID\>/Fusion/Metafusion/final.n2.cluster.CANCER_FUSIONS \
     上記ファイルにも記載がない場合はGMに指示を仰ぐ
  6. **[工程外手順]** [monitoring preFilter](https://github.com/mkaba-gxd/monitoring?tab=readme-ov-file#7-prefilter) コマンドでフィルター前データの一覧を作成する\
      → /data1/work/monitoring/preFilter/\<batch_folder\> の下に [eWES/WTS].*.xlsx が作成される
  7. **[工程外手順]** レビュー資料作成手順.pptx に従ってフィルター前データの一覧に情報を追記し、共有フォルダの以下の場所に格納した後、GMに完了報告を行う。(ファイル作成時の日時でサブフォルダを作成する)\
     \\\192.168.11.19\cap\移行済データ\変異確認ファイル\\[YYYYMMDD]\ 
  8. **[工程外手順]** [monitoring aggregate](https://github.com/mkaba-gxd/monitoring?tab=readme-ov-file#10aggregate) コマンドでBox用集計データを作成する。\
    → /data1/work/monitoring/aggregate/[timestamp].xlsx が作成されるので、共有サーバーの以下の場所に格納する\
       \\\192.168.11.19\cap\移行済データ\変異確認ファイル\01_Box\
  9. **[工程外手順]** [monitoring intermediate](https://github.com/mkaba-gxd/monitoring?tab=readme-ov-file#9intermediate) コマンドでSNV＆InDelの中間データ一覧を作成する \
      → /data1/work/monitoring/intermediate/[timestamp].3tools.xlsx が作成されるので、共有サーバーの以下の場所に格納する\
       \\\192.168.11.19\cap\移行済データ\変異確認ファイル\00_3tools\
  10. ワークシートとqc_infoシートを印刷してTRFとともにファイルにまとめ、GMに渡す
  11. レビュー終了後、GMからレポート修正の指示があった場合は以下の手順でレポート修正を行う\
     11-1. [解析結果の編集](#RM) ※ 解析完了時から当該作業時までにPipelineに変更があった場合は rerun.sh を作成する\
     11-2. [解析結果の削除](#RE) ※ cronでrerunする場合はstatusを100、rerun.shを手動実行する場合は statusを101に指定する\
     11-3. cronで解析が再実行されるのを待つ、もしくは rerun.sh を手動で実行する\
     11-4. レポート修正の完了をGMに報告する
  12. GMからレポートのアップロード完了の連絡が来たら、OncoStationで作成されたPDFレポートの[リンクを作成](#LNK)する\
       → /data1/work/report/[eWES/WTS]/\<batch_folder\>/OST/ の下にリンクが作成される
  13. OncoStationで作成されたPDFレポートを印刷する（Oncostationスタンプ,2in1,白黒両面印刷）
  14. [server_backup up](https://github.com/mkaba-gxd/server_backup#1-データのバックアップアップロード) コマンドでバックアップサーバーへのデータバックアップを実施する
  15. [aws_tool up](https://github.com/mkaba-gxd/aws?tab=readme-ov-file#1-アップロード) コマンドでAWSへのデータバックアップを実施する
  16. ワークシートの工程欄にすべてチェックが入っていることを確認し、終了日時を記載する
  17. ワークシート,qc_info,TRF,PDFレポートをまとめて検査結果報告台帳にファイリングする
  18. **[工程外手順]** NGSから転送された生データをバックアップサーバー(/data2/backup/rawdata/)へ手動でrsync転送する ※所有者がrootのためsudoで実行
  19. **[工程外手順]** /data1/data/NovaseqX/ に出力されている mergeされたfastq.gzをバックアップサーバー(/data2/backup/NovaseqX/)へ手動でrsync転送する
  20. **[工程外手順]** [send_to_itms](https://github.com/mkaba-gxd/send_to_itms) コマンドでiTMSに送付するデータを /media/usb/cap にコピーし、IT管理者に報告する

工程15については当該バッチの全検体が解析完了した時点、工程18についてはNGSデータが転送完了した時点、工程19に関しては当該バッチの全検体の解析がスタートした時点で転送する元データが作成済となるため、実行してもよい。

</details>

<a id="CR"></a>
## 1\. ワークシートの作成
\<OUTDIR\>にワークシートを作成する。同名のファイルがある場合は上書きするかどうか選択する。\
シーケンスが開始されてから(=\<NOVADIR\>に解析フォルダが作成されてから)実行すること。
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
usage: worksheet.py create [-h] --flowcellid FLOWCELLID [--project_type {both,WTS,eWES}]
                           [--novadir NOVADIR] [--outdir OUTDIR]

optional arguments:
  -h, --help            show this help message and exit
  --flowcellid FLOWCELLID, -fc FLOWCELLID
                        flowcell id (default: None)
  --project_type {both,WTS,eWES}, -t {both,WTS,eWES}
                        project type (default: both)
  --novadir NOVADIR, -n NOVADIR
                        novaseq directory (default: /data1/gxduser/novaseqx)
  --outdir OUTDIR, -o OUTDIR
                        output directory path (default: /data1/work/workSheet)

version: v3.1.0
usage: worksheet.py create [-h] --flowcellid FLOWCELLID [--directory DIRECTORY] 
                           [--project_type {both,WTS,eWES}] [--outdir OUTDIR]
```
| option           |required | 概要           |default         |
|:-----------------|:-------:|:---------------|:---------------|
|--flowcellid/-fc  |True     |バッチ固有のID。OncoStationに掲載されている9桁の半角英数字   |None |
|--project_type/-t |False    |解析種別。both,eWES,WTSから選択する |both                    |
|--novadir/-n      |False    |NGSデータ転送先フォルダ             |/data1/gxduser/novaseqx |
|--outdir/-o       |False    |ワークシート出力先ディレクトリへのパス|/data1/work/workSheet |

</details>

<details>
  <summary> 
    手作業で行う場合
  </summary>

- templete フォルダに作業書のひな形が格納されているので、/data1/work/workSheet/ にコピーして加工する。
- sample_info シートについては、BDeaver などでデータベースに接続し、テーブル gxd.tb_expr_seq_header, gxd.gc_qc_sample, gxd.gc_project, gxd.gc_history_log から flowcell ID に紐づいている検体情報を抽出して作成する。
- すべての項目について抽出することが難しい場合は SAMPLE_ID,PATIENT_NO,CTRL の情報だけ記載する。
</details>

<a id="CH"></a>
## 2\. 解析の進捗確認
- データベースに登録されている検体情報とNGSデータフォルダに格納されているSampleSheet.csvの内容が合致しているかを確認する
- データベースのANAL_STATUSの値を基に解析の進捗を報告する（100:registered, 101:in progress, 102:finished, 104:reanalysis）
- report.json が作成されている検体数と、未作成の検体のSample IDを表示する
- report.pdf が作成されている検体数を表示する
- Pipelineで作成されたreport.pdfのシンボリックリンクを作成する
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
usage: worksheet.py check [-h] --flowcellid FLOWCELLID [--directory DIRECTORY] [--project_type {both,WTS,eWES}]
                          [--novadir NOVADIR] [--linkDir LINKDIR]

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
|--directory/-d    |False    |解析フォルダの親ディレクトリへのパス  |/data1/data/result      |
|--project_type/-t |False    |解析種別。both,eWES,WTSから選択する  |both                    |
|--novadir/-n      |False    |NGSデータ転送先フォルダ              |/data1/gxduser/novaseqx |
|--linkDir/-l      |False    |PDFレポートのリンク先ディレクトリへのパス |/data1/work/report |
</details>

<details>
  <summary> 
    手作業で行う場合
  </summary>

### SampleSheetとDB登録内容が一致しているかを確認する
① サンプルシート（通常は /data1/gxduser/novaseqx/[batch]/SampleSheet.csv に格納）の [BCLConvert_Data] 項目の情報を抽出する。\
② BDeaver などでデータベースに接続し、テーブル gxd.gc_project, gxd.gc_history_log, gxd.tb_expr_seq_header, gxd.gc_qc_sample から flowcell ID に紐づいている Sample_ID, Index, Index2 を抽出する。\
①と②のSample_ID, Index, Index2 が過不足なく一致することを確認する。

### 全サンプルの解析が終了し、report.jsonとreport.pdf が作成されていることを確認する
BDeaver などでデータベースに接続し、テーブル gxd.gc_project, gxd.gc_history_log, gxd.tb_expr_seq_header, gxd.gc_qc_sample から flowcell ID に紐づいている検体の ANAL_STATUS がすべて102であることを確認する。\
以下のコマンドで作成済の *.report.json と *.report.pdf 一覧を確認する。
```
ll /data1/data/result/[eWES/WTS]/[batch]/*/Summary/*.report.json
ll /data1/data/result/[eWES/WTS]/[batch]/*/Summary/*.report.pdf
```

### Pipelineで作成されたpdfレポートのシンボリックリンクを作成する
```
mkdir -p /data1/work/report/[eWES/WTS]/[batch]/PL 
for file in `ls /data1/data/result/[eWES/WTS]/[batch]/*/Summary/*.report.pdf`; do
ln -s $file /data1/work/report/[eWES/WTS]/[batch]/PL/
done 
```

</details>

<a id="ADD"></a>
## 3\. シートの追加
作成済のワークシートに以下の情報を項目別にまとめたシートを追加する。
- QC情報（OncoStationに掲載される項目。WETのQCも含む）
- レポートに記載されている解析結果（Summaryフォルダに格納された summarized.\*.tsv から収集）

ワークシート未作成の場合はエラー終了する。
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
usage: worksheet.py addition [-h] --flowcellid FLOWCELLID [--directory DIRECTORY] 
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
|--project_type/-t |False    |解析種別。both,eWES,WTSから選択する   |both                  |
|--outdir/-o       |False    |ワークシート出力先ディレクトリへのパス|/data1/work/workSheet |

</details>

解析途中の検体があった場合は、操作の継続を聞かれるので選択する。\
**継続する場合は、解析中の検体情報は記載されない**ので、全検体の解析が終了した後に再度実行してQC情報が確認できるようにしておく。\
なお、再実行時した場合は work_sheet, sample_info 以外のシートは上書きされる。

<details>
  <summary> 
    手作業で行う場合
  </summary>

### ワークシートにqc_infoシートを追加する
BDeaver などでデータベースに接続し、テーブル gxd.gc_project, gxd.gc_history_log, gxd.tb_expr_seq_header, gxd.gc_qc_sample から flowcell ID に紐づいている検体情報を抽出してqc_infoシートを作成する。\
または、OncoStationにアクセスし、各検体の Sample Detail ページに記載されているQC情報をまとめた一覧を qc_infoシートに記載する。

### 検査コメントが必要な検体数を記載する
qc_infoシートの内容を確認し、ワークシート項目7の「検査コメントが必要な検体数」に値を入力する

</details>

<a id="RM"></a>
## 4\. 解析結果の編集（削除）
指定された sample ID について、解析フォルダに格納されているsummaryファイルの不要な行を削除する。\
**この機能だけではデータベースの登録内容は変更されません（＝OSTレポートも変更されません）。** [5.データベースのリセット](#RE) で当該検体の変異情報をデータベースから削除し、手作業またはcronの自動実行を利用して report_json 工程を行い、データベースへ検査結果を登録すること。\
解析フォルダ内データの書き換えを行うので **gxd_pipeline ユーザーで実行すること。** 
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
[手順はこちら](https://github.com/mkaba-gxd/special-case/blob/main/README.md#case6-解析結果の修正とレポートの再作成手作業)
</details>

<details>
  <summary> 
    手作業で行う場合
  </summary>

修正内容によって以下のファイルを編集する。（オリジナルファイルは名前を変更して残しておく）
|解析種別  |修正項目                   |修正対象ファイル      |修正方法             |
|:--------|:--------------------------|:-------------------|:-------------------|
|eWES     |SNV & InDel                |/data1/data/result/eWES/[batch]/[sampleID]/Summary/[sampleID].summarized.snv.target.tsv |該当行削除 |
|eWES     |Copy Number Variants       |/data1/data/result/eWES/[batch]/[sampleID]/Summary/[sampleID].summarized.cnv.exome.tsv  |該当行削除 |
|WTS      |Fusion                     |/data1/data/result/WTS/[batch]/[sampleID]/Summary/[sampleID].summarized.fusion.tsv      |該当行削除 |
|WTS      |Alternative Splicing       |/data1/data/result/WTS/[batch]/[sampleID]/Summary/[sampleID].summarized.splice.tsv      |該当行の2カラム目以降の値を空白に変更 |

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

<details>
  <summary> 
    手作業で行う場合
  </summary>
  
この工程は手作業でできなくもないですが、DBやSQLがよくわからない場合は無暗に行わず、開発チームまたはITチームに問い合わせてください。
- 以下のファイルについて、ファイル名を変更する。\
/data1/data/result/[eWES/WTS]/[batch]/[sampleID]/Summary/[sampleID].report.json ⇒ [sampleID].report.[timestamp].json \
/data1/data/result/[eWES/WTS]/[batch]/[sampleID]/Summary/[sampleID].report.pdf ⇒ [sampleID].report.[timestamp].pdf 
- BDeaver などでデータベースに接続し、当該検体の変異情報をすべて削除する。※修正した変異以外も削除すること

|解析種別 |修正対象テーブル    |
|:--------|:-------------------|
|eWES     |gc_alter_snv, gc_snv_indeterminate, gc_alter_cnv, gc_alter_msi, del_alt_tmb |
|WTS      |gc_alter_splice, gc_alter_sv, gc_alter_express |
- BDeaver などでデータベースに接続し、テーブル gc_qc_bi に登録済の当該検体のQC情報をすべて削除する
- BDeaver などでデータベースに接続し、修正対象の検体について、テーブル gxd.gc_history_log, gc_qc_sample の ANAL_STATUS の値を102から 100 または 101 に変更する。\
※ ANAL_STATUSを100にした場合は10分以内にcronによる解析再実行が行われる。101にした場合は手作業で report_json 工程を実行する。\
※ データベースの書き換えについては、**間違った場合のリカバリーが難しい**ため、ダブルチェックを実施する等、細心の注意を払うこと。
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
usage: worksheet.py link [-h] --flowcellid FLOWCELLID [--directory DIRECTORY]
                         [--project_type {both,WTS,eWES}] [--linkDir LINKDIR]

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

<details>
  <summary> 
    手作業で行う場合
  </summary>
  
ツールの修正が難しい場合は OncoStation でPDFレポートをダウンロードして印刷するだけで良いです。\
① /data1/work/report/[eWES/WTS]/[batch]/OST を作成する。\
② BDeaver などでデータベースに接続し、テーブル gxd.gc_project, gxd.gc_history_log, gxd.tb_expr_seq_header, gxd.gc_qc_sample から flowcell ID に紐づいている検体情報を抽出して各検体の REPORT_URL を取得する。\
③ /data1/OST/reports/[sample ID]/ の直下にある REPORT_URL と同じファイル名のpdfのシンボリックリンクを①で作成したディレクトリに作成する。
</details>



