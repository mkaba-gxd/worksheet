import os
import glob
import pandas as pd
from pathlib import Path
from io import StringIO
from .commom import *


def run_report(args):

    flowcellid = args.flowcellid
    directory = args.directory
    project_type = args.project_type
    linkDir = args.linkDir
    repDir = '/data1/OST/reports'

    df_info = getinfo(flowcellid)
    if df_info.shape[0] == 0 : init('no applicable specimens.')

    df_info['PRJ_TYPE'] = df_info['PRJ_TYPE'].str.replace('EWES',"eWES")
    if project_type == "both" :
        df_info = df_info[ df_info['PRJ_TYPE'].isin(['eWES','WTS']) ]
    else :
        df_info = df_info[ df_info['PRJ_TYPE']==project_type]
    if df_info.shape[0] == 0 : init('no applicable specimens')

    for pj_type in df_info['PRJ_TYPE'].unique():

        df_prj = df_info[df_info['PRJ_TYPE']==pj_type]
        df_prj = df_prj[df_prj['REPORT_URL'].notna()].reset_index()
        if df_prj.shape[0] == 0 :
            print(pj_type + ': No samples have been reported on.')
            continue

        batch = df_prj['sub_name'][0]
        anal_dir = SearchDir(batch, Path(directory + '/' + pj_type))
        if anal_dir is None:
            print(pj_type + ': Analysis folder not created.')
            continue

        linkDir_add = linkDir + '/' + pj_type + '/' + os.path.basename(anal_dir)
        os.makedirs(linkDir_add, exist_ok=True)
        for i, item in df_prj.iterrows() :
            rawRepo = os.path.join(repDir, item['REPORT_URL'])
            lnRepo = os.path.join(linkDir_add, os.path.basename(item['REPORT_URL']))

            if not os.path.isfile(rawRepo):
                print('Could not create symbolic link: ' + os.path.basename(item['REPORT_URL']))
                continue

            if os.path.islink(lnRepo) or os.path.isfile(lnRepo) :
                os.remove(lnRepo)

            os.symlink(rawRepo, lnRepo)          

    
