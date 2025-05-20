import os
import sys
import pymysql
import warnings
import pandas as pd
from pathlib import Path

def getinfo(fc_id):
    try :
        connection = pymysql.connect(host="192.168.9.100", user="gxd_pipeline", password="gw!2341234", database="gxd")
    except Exception as e:
        sys.exit({e})

    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        db_tbl = pd.read_sql(SelectData(fc_id), connection)

    return db_tbl

def SelectData(fc_id):
    query = f"""
    SELECT tesh.run_id, concat(tesh.equip_side, tesh.fc_id) AS sub_name, gp.PRJ_TYPE, ghl.ANAL_STATUS, gp.SAMPLE_ID, gp.PATIENT_NO, gp.DIAGNOSIS_NAME, gp.AGE, gp.GENDER, gqs.INDEX1_SEQUENCE, gqs.INDEX2_SEQUENCE
    FROM gxd.tb_expr_seq_header tesh
    INNER JOIN gxd.gc_qc_sample gqs
    ON tesh.run_id = gqs.run_id
    INNER JOIN gxd.gc_project gp
    ON gqs.SAMPLE_ID = gp.SAMPLE_ID
    INNER JOIN gxd.gc_history_log ghl
    ON gqs.SAMPLE_ID = ghl.SAMPLE_ID
    AND ghl.idx = (SELECT MAX(idx) FROM gc_history_log WHERE SAMPLE_ID = gqs.SAMPLE_ID)
    WHERE tesh.fc_id = '{fc_id}'
    """
    return query

def fcDir_table(df, novaseqDir: Path):

    df = df[['sub_name','PRJ_TYPE']].drop_duplicates()
    df['seqDir'] = None

    for i, item in df.iterrows() :
        fcDir = SearchDir(item['sub_name'], Path(novaseqDir + '/' + item['PRJ_TYPE']))
        df.loc[i,'seqDir'] = fcDir

    df = df.dropna(subset=['seqDir'])

    return df

def SearchDir(batchID, novaseqDir : Path):
    fcDirs = [fcDir for fcDir in novaseqDir.iterdir() if fcDir.name.endswith(batchID)]
    fcDirs.sort()
    if len(fcDirs) != 1: return None

    return os.path.basename(fcDirs[-1])

def getbatch(sample, anal_dir):
    try :
        connection = pymysql.connect(host="192.168.9.100", user="gxd_pipeline", password="gw!2341234", database="gxd")
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            tbl = pd.read_sql(subname_query(sample), connection)

        subname = tbl.sub_name[0]
        anal_type = tbl.PRJ_TYPE[0]
        if anal_type == 'EWES' : anal_type = 'eWES'
        anal_dir = Path(os.path.join(anal_dir, anal_type))
        fcDirs = [fcDir for fcDir in anal_dir.iterdir() if fcDir.name.endswith(subname)]
        if len(fcDirs) != 1: return None, None
        fcDirs.sort()
        return os.path.basename(fcDirs[-1]), anal_type

    except Exception as e:
        return None, None

def subname_query(sample):
    query = f"""
    SELECT concat(tesh.equip_side, tesh.fc_id) AS sub_name, gp.PRJ_TYPE
    FROM gxd.tb_expr_seq_header tesh
    INNER JOIN gxd.gc_qc_sample gqs
    ON tesh.run_id = gqs.run_id
    INNER JOIN gxd.gc_project gp
    ON gqs.SAMPLE_ID = gp.SAMPLE_ID
    INNER JOIN gxd.gc_history_log ghl
    ON gqs.SAMPLE_ID = ghl.SAMPLE_ID
    AND ghl.idx = (SELECT MAX(idx) FROM gc_history_log WHERE SAMPLE_ID = gqs.SAMPLE_ID)
    WHERE ghl.SAMPLE_ID = '{sample}'
    """
    return query

def init(msg):
    print(msg)
    sys.exit()


