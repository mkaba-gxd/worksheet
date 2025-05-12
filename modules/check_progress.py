import os
import sys
import glob
import pandas as pd
from pathlib import Path
from io import StringIO
from .commom import *

def search_analysis_dir(batch, novaseqDir: Path):
    fcDirs = [fcDir for fcDir in novaseqDir.iterdir() if fcDir.name.endswith(batch)]
    fcDirs.sort()
    if len(fcDirs) != 1: return None
    return fcDirs[-1]

def ss_check(ss_file:Path, df):
    df_ss = load_ss(ss_file)
    df_merge = pd.merge(df_ss, df, left_on=['Sample_ID','Index','Index2'], right_on=['SAMPLE_ID','INDEX1_SEQUENCE','INDEX2_SEQUENCE'], how='right')
    df_only = df_merge[df_merge['Sample_ID'].isna()]
    if df_only.shape[0] == 0:
        return None
    else :
        return df_only['SAMPLE_ID'].unique()

def load_ss(ss_file):
    with open(ss_file, 'r') as file :
        lines = file.readlines()
    # Identify the location where [BCLConvert_Data] appears.
    start_index = None
    for i, line in enumerate(lines):
        if line.strip() == "[BCLConvert_Data]":
            start_index = i
            break

    if start_index is not None :
        start_index += 1
    else :
        return None

    data_lines = []
    for line in lines[start_index:]:
        if not line.strip():
            break
        data_lines.append(line.strip())

    # Convert to DataFrame
    data_str = "\n".join(data_lines)
    df = pd.read_csv(StringIO(data_str), index_col=None)
    df = df[["Sample_ID","Index","Index2"]].drop_duplicates()

    return df

def subtotal_status (df):
    for idx in df.groupby('ANAL_STATUS').count().index :
        if idx == '100' :
            print ('registered: ' + str(df.groupby('ANAL_STATUS').get_group('100').shape[0]) + 'samples')
        elif idx == '101' :
            print ('in progress: ' + str(df.groupby('ANAL_STATUS').get_group('101').shape[0]) + 'samples')
            print (df[df['ANAL_STATUS']=='101'][['run_id','sub_name','PRJ_TYPE','SAMPLE_ID','ANAL_STATUS']].to_string(index=False))
        elif idx == '102' :
            print ('finished: ' + str(df.groupby('ANAL_STATUS').get_group('102').shape[0]) + 'samples')
        elif idx == '104' :
            print ('reanalysis: ' + str(df.groupby('ANAL_STATUS').get_group('104').shape[0]) + 'samples')

def check_files(df, analDir:Path, type):
    FILES = glob.glob(str(analDir) + '/*/Summary/*.report.' + type)
    SAMPLES = [ p.split("/")[-1].split('.')[0] for p in FILES ]
    COMP = list(set(df['SAMPLE_ID']) - set(SAMPLES))
    if len(COMP) > 0:
        print(type.upper() + ' not yet created:' + ','.join(COMP))
        return False
    else:
        print (type.upper() + ' all created')
        return True

def create_link(df, analDir:Path, linkDir:Path):
    FILES = glob.glob(str(analDir) + '/*/Summary/*.report.pdf')
    d = dict(zip([ p.split("/")[-1].split('.')[0] for p in FILES ], FILES))
    FAIL = list()
    for sample in df['SAMPLE_ID'] :
        if os.path.isfile(d[sample]):
            if os.path.islink(str(linkDir) + '/' + sample + '.pdf') :
                os.remove(str(linkDir) + '/' + sample + '.pdf')
            elif os.path.isfile(str(linkDir) + '/' + sample + '.pdf') :
                os.remove(str(linkDir) + '/' + sample + '.pdf')
            os.symlink(d[sample], str(linkDir) + '/' + sample + '.pdf')
        else:
            FAIL.append(sample)

    if len(FAIL) > 0 :
        print ('Could not create symbolic link: ' + ','.join(FAIL))

def check_progress(args):

    flowcellid = args.flowcellid
    directory = args.directory
    project_type = args.project_type
    linkDir = args.linkDir
    novadir = args.novadir

    df_info = getinfo(flowcellid)
    if df_info.shape[0] == 0 : init('no applicable specimens.')

    df_info['PRJ_TYPE'] = df_info['PRJ_TYPE'].str.replace('EWES',"eWES")
    if project_type == "both" :
        df_info = df_info[ df_info['PRJ_TYPE'].isin(['eWES','WTS']) ]
    else :
        df_info = df_info[ df_info['PRJ_TYPE']==project_type]
    if df_info.shape[0] == 0 : init('no applicable specimens')

    for pj_type in df_info['PRJ_TYPE'].unique():

        print ('---' + pj_type + '---')

        df_prj = df_info[df_info['PRJ_TYPE']==pj_type].reset_index()
        batch = df_prj['sub_name'][0]
        anal_dir = search_analysis_dir(batch, Path(directory + '/' + pj_type))
        if anal_dir is None:
            print('Analysis folder not created.')
            continue

        ss_file = os.path.join(novadir, os.path.basename(anal_dir), 'SampleSheet.csv')

        if not os.path.isfile(ss_file) :
            print("Sample sheet file does not exist: " + ss_file)
            continue
        print ("SampleSheet: " + str(ss_file))

        differential = ss_check(ss_file, df_prj)            # Check the contents of the sample sheet
        if not differential is None :
            print ("Registration Error: " + ','.join(differential))
            continue
        else :
            print("SampleSheet and DB registration matched.")

        print("analysis dir: " + str(anal_dir))

        subtotal_status(df_prj)

        df_prj = df_prj[df_prj['ANAL_STATUS']=='102']
        if df_prj.shape[0] == 0 : continue
        flag = check_files(df_prj, anal_dir, 'json')
        flag = check_files(df_prj, anal_dir, 'pdf')

        if flag :
            linkDir_add = linkDir + '/' + pj_type + '/' + os.path.basename(anal_dir)
            os.makedirs(linkDir_add, exist_ok=True)
            create_link(df_prj, anal_dir, Path(linkDir_add))


