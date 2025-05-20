import os
import sys
import argparse
from pathlib import Path
from modules import *

VERSION = "v3.0.0"

def run_create(args):
    create_worksheet(args)

def run_check(args):
    check_progress(args)

def run_add(args):
    additional_worksheet(args)

def run_remove(args):
    remove_data(args)

def run_reset(args):
    reset_db(args)

def main():

    if '--help' in sys.argv or '-h' in sys.argv:
        print(f"version: {VERSION}")

    parser = argparse.ArgumentParser(
        description="Created and added worksheet and checked processes."
    )
    parser.add_argument('--version','-v', action='version', version=f'%(prog)s {VERSION}')
    subparsers = parser.add_subparsers(dest="command", required=True)

    # create worksheet
    parser_cr = subparsers.add_parser("create", aliases=['CR'], help="create worksheet", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_cr.add_argument("--flowcellid","-fc", required=True, help="flowcell id")
    parser_cr.add_argument("--directory","-d", required=False, help="parent analytical directory", default="/data1/data/result")
    parser_cr.add_argument("--project_type","-t", required=False, help="project type", default="both", choices=["both","WTS","eWES"])
    parser_cr.add_argument("--outdir","-o", required=False, help="output directory path", default="/data1/work/workSheet")
    parser_cr.set_defaults(func=run_create)

    # check analysis
    parser_ch = subparsers.add_parser("check", aliases=['CH'], help="check progress", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_ch.add_argument("--flowcellid","-fc", required=True, help="flowcell id")
    parser_ch.add_argument("--directory","-d", required=False, help="parent analytical directory", default="/data1/data/result")
    parser_ch.add_argument("--project_type","-t", required=False, help="project type", default="both", choices=["both","WTS","eWES"])
    parser_ch.add_argument("--linkDir","-l", required=False, help="Linked directory of report files", default="/data1/work/report")
    parser_ch.add_argument("--novadir","-n", required=False, help="novaseq directory", default="/data1/gxduser/novaseqx")
    parser_ch.set_defaults(func=run_check)

    # additional worksheet
    parser_ad = subparsers.add_parser("addition", aliases=['ADD'], help="additional worksheet", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_ad.add_argument("--flowcellid","-fc", required=True, help="flowcell id")
    parser_ad.add_argument("--directory","-d", required=False, help="parent analytical directory", default="/data1/data/result")
    parser_ad.add_argument("--project_type","-t", required=False, help="project type", default="both", choices=["both","WTS","eWES"])
    parser_ad.add_argument("--outdir","-o", required=False, help="output directory path", default="/data1/work/workSheet")
    parser_ad.set_defaults(func=run_add)

    # Edit (delete) the analysis results.
    parser_rm = subparsers.add_parser("remove", aliases=['RM'], help="delete the analysis results", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_rm.add_argument("--sample","-s", required=True, help="sample id")
#    parser_rm.add_argument("--item","-i", required=True, help="Item to be edited", choices=["SNV","FS","AS"])
    parser_rm.add_argument("--analysis_dir","-d", required=False, help="parent analytical directory", default="/data1/data/result")
    parser_rm.set_defaults(func=run_remove)

    # reset database
    parser_re = subparsers.add_parser("reset", aliases=['RE'], help="reset database", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_re.add_argument("--sample","-s", required=True, help="sample id")
    parser_re.add_argument("--roll_back","-r", required=False, help='Set the status to 101 (Analysis in progress). If not specified, set the status to 100 (ready for analysis).', action='store_false')
    parser_re.add_argument("--analysis_dir","-d", required=False, help="parent analytical directory", default="/data1/data/result")
    parser_re.set_defaults(func=run_reset)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":

    main()


