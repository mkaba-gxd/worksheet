import os
import sys
import shutil
import subprocess
import pandas as pd
from pathlib import Path
from .commom import *

def prompt_choice(prompt, choices):
    while True:
        ans = input(prompt).strip().lower()
        if ans in choices:
            return ans

def generate_backup_path(file_path):
    base, ext = os.path.splitext(file_path)
    counter = 1
    backup_path = f"{base}.BK{ext}"
    while os.path.exists(backup_path):
        backup_path = f"{base}.BK_{counter}{ext}"
        counter += 1
    return backup_path

def backup_and_write_file(original_path, df):
    backup_path = generate_backup_path(original_path)
    shutil.move(original_path, backup_path)
    df.to_csv(original_path, sep='\t', index=False)
    return backup_path

def confirm_diff_and_report(original, backup, removed_count):
    try:
        result = subprocess.run(['diff', backup, original], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        diff_lines = [line for line in result.stdout.splitlines() if line.startswith('<')]
        print(f"\n[DIFF] Deleted {len(diff_lines)} lines. Expected: {removed_count} lines removed.")
    except Exception as e:
        print(f"Could not run diff: {e}")

def handle_snv(file_path):

    data = pd.read_csv(file_path, sep='\t', dtype=str, keep_default_na=False, na_values=[])
    deleted_rows = 0

    while True:
        ans = input("What mutations to delete?[gene,HGVSc,HGVSp]: ").strip().split(',')
        if len(ans) != 3:
            choice = prompt_choice("Invalid input. Retry? (yes[Y]/no[N]): ", ['yes', 'y', 'no', 'n'])
            if choice in ['no', 'n']:
                break
            else:
                continue
        gene, hgvsc, hgvsp = [x.strip() for x in ans]
        match = data[
            (data['SYMBOL'] == gene) &
            (data['HGVSc'].str.endswith(hgvsc)) &
            (data['HGVSp'].str.endswith(hgvsp))
        ]

        if match.empty:
            print("No applicable data.")
            choice = prompt_choice("Retry or quit? (retry[R]/quit[Q]): ", ['retry', 'r', 'quit', 'q'])
            if choice in ['quit', 'q']:
                break
            else:
                continue

        print(match[['CHROM','POS','AF','SYMBOL','HGVSc','HGVSp','Clinvar_CLNSIG','ONCOKB_ONCOGENICITY']])
        confirm = prompt_choice("Do you want to remove these? (yes[Y]/no[N]): ", ['yes', 'y', 'no', 'n'])

        if confirm in ['yes', 'y']:
            data = data.drop(match.index)
            deleted_rows += match.shape[0]

        choice = prompt_choice("Continue or quit? (continue[C]/quit[Q]): ", ['continue', 'c', 'quit', 'q'])
        if choice in ['quit', 'q']:
            break

    if deleted_rows > 0:
        backup = backup_and_write_file(file_path, data)
        confirm_diff_and_report(file_path, backup, deleted_rows)

def handle_cnv(file_path):

    data = pd.read_csv(file_path, sep='\t', dtype=str, keep_default_na=False, na_values=[])
    deleted_rows = 0

    while True:
        gene = input("What Copy Number to delete?[gene]: ").strip()
        match = data[data['Gene_name'] == gene]

        if match.empty:
            print("No applicable data.")
            choice = prompt_choice("Retry or quit? (retry[R]/quit[Q]): ", ['retry', 'r', 'quit', 'q'])
            if choice in ['quit', 'q']:
                break
            else:
                continue

        print(match[['Gene_name','CHROM','gene.mean.CN']])
        confirm = prompt_choice("Do you want to remove these? (yes[Y]/no[N]): ", ['yes', 'y', 'no', 'n'])

        if confirm in ['yes', 'y']:
            data = data.drop(match.index)
            deleted_rows += match.shape[0]

        choice = prompt_choice("Continue or quit? (continue[C]/quit[Q]): ", ['continue', 'c', 'quit', 'q'])
        if choice in ['quit', 'q']:
            break

    if deleted_rows > 0:
        backup = backup_and_write_file(file_path, data)
        confirm_diff_and_report(file_path, backup, deleted_rows)

def handle_fusion(file_path):

    data = pd.read_csv(file_path, sep='\t', dtype=str, keep_default_na=False, na_values=[])
    deleted_rows = 0

    while True:
        ans = input("What fusions to delete?[gene_1,gene_2,breakpoint_1(chr:position),breakpoint_2(chr:position)]. ").strip().split(',')
        if len(ans) != 4:
            choice = prompt_choice("Invalid input. Retry? (yes[Y]/no[N]): ", ['yes', 'y', 'no', 'n'])
            if choice in ['no', 'n']:
                break
            else :
                continue

        gene_1, gene_2, bk_1, bk_2 = [x.strip() for x in ans]
        bk_chr_1, bk_pos_1 = [ x.strip() for x in bk_1.split(':') ]
        bk_chr_2, bk_pos_2 = [ x.strip() for x in bk_2.split(':') ]
        match = data[
            (data['gene1'] == gene_1) &
            (data['gene2'] == gene_2) &
            (data['chr1'] == bk_chr_1) &
            (data['chr2'] == bk_chr_2) &
            (data['breakpoint_1'] == bk_pos_1) &
            (data['breakpoint_2'] == bk_pos_2)
        ]

        if match.empty:
            print("No applicable data.")
            choice = prompt_choice("Retry or quit? (retry[R]/quit[Q]): ", ['retry', 'r', 'quit', 'q'])
            if choice in ['quit', 'q']:
                break
            else:
                continue

        print(match[['gene1','gene2','chr1','breakpoint_1','chr2','breakpoint_2','max_split_cnt','max_span_cnt']])
        confirm = prompt_choice("Do you want to remove these? (yes[Y]/no[N]): ", ['yes', 'y', 'no', 'n'])

        if confirm in ['yes', 'y']:
            data = data.drop(match.index)
            deleted_rows += match.shape[0]

        choice = prompt_choice("Continue or quit? (continue[C]/quit[Q]): ", ['continue', 'c', 'quit', 'q'])
        if choice in ['quit', 'q']:
            break

    if deleted_rows > 0:
        backup = backup_and_write_file(file_path, data)
        confirm_diff_and_report(file_path, backup, deleted_rows)

def handle_splice(file_path):

    data = pd.read_csv(file_path, sep='\t', dtype=str, keep_default_na=False, na_values=[])
    deleted_rows = 0

    data = data.dropna(subset=['ONCOGENICITY'])
    if data.shape[0] == 0 :
        print('No Alternative Splicing detected.')
        return

    del_cols = data.columns.to_list()
    del_cols.remove('spliceName')

    while True:

        ans = input("What splices to delete?[EGFR,MET,AR]: ").strip().split(',')

        diff = list(set(ans) - set(['EGFR','MET','AR']))
        if len(diff) > 0 :
            print("Invalid input. " + ','.join(diff) + ' is not included in the inspection.')
            continue

        delete_id = []
        if 'EGFR' in ans : delete_id.append('EGFR vIII')
        if 'MET' in ans : delete_id.append('MET exon 14 skipping')
        if 'MET' in ans : delete_id.append('AR-V7')

        if len(diff) > 0 :
            print("Invalid input. " + ','.join(diff) + ' is not included in the inspection.')
            continue
        elif len(delete_id) == 0 :
            print("Invalid input. Check input values: " + ','.join(ans))
            continue

        match = data[ data['spliceName'].isin(delete_id) ]
        print(match[['spliceName','discordant_mates','canonical_reads','ratio','tpm_total','tpm_variant']])
        confirm = prompt_choice("Do you want to remove these? (yes[Y]/no[N]): ", ['yes', 'y', 'no', 'n'])
        if confirm in ['yes', 'y']:
            data[ match.index, del_cols ] = ''
            deleted_rows += match.shape[0]

        choice = prompt_choice("Continue or quit? (continue[C]/quit[Q]): ", ['continue', 'c', 'quit', 'q'])
        if choice in ['quit', 'q']:
            break

    if deleted_rows > 0:
        backup = backup_and_write_file(file_path, data)
        confirm_diff_and_report(file_path, backup, deleted_rows)

def remove_ewes(sample, smDir):

    FAIL_S = os.path.join(smDir, sample + '.summarized.snv.target.tsv')
    FAIL_C = os.path.join(smDir, sample + '.summarized.cnv.exome.tsv')

    if not os.path.isfile(FAIL_S):
        init("SNV file does not exist: {FAIL_S}")
    if not os.path.isfile(FAIL_C):
        init(f"CNV file does not exist: {FAIL_C}")

    while True:
        target = input("Which item(s) would you like to modify? [SNV/CNV/quit[Q]]: ").strip().lower()
        if target == 'snv':
            handle_snv(FAIL_S)
            break
        elif target == 'cnv':
            handle_cnv(FAIL_C)
            break
        elif target in ['quit', 'q']:
            break
        else:
            print("Invalid input. Please enter 'SNV' or 'CNV' or 'quit(Q)'.")


def remove_wts(sample, smDir):

    FAIL_F = os.path.join(smDir, sample + '.summarized.fusion.tsv')
    FAIL_A = os.path.join(smDir, sample + '.summarized.splice.tsv')

    if not os.path.isfile(FAIL_F):
        init("fusion file does not exist: {FAIL_F}")
    if not os.path.isfile(FAIL_A):
        init("alternative splicing file does not exist: {FAIL_A}")

    while True:
        target = input("Which item(s) would you like to modify? [FS/AS/quit[Q]]: ").strip().lower()
        if target == 'fs':
            handle_fusion(FAIL_F)
            break
        elif target == 'as':
            handle_splice(FAIL_A)
            break
        elif target in ['quit', 'q']:
            break
        else:
            print("Invalid input. Please enter 'FS' or 'AS' or 'quit(Q)'.")


def remove_data(args):

    sample = args.sample
    anal_dir = args.analysis_dir

    subDir, anal_type = getbatch(sample, anal_dir)
    smDir = os.path.join(anal_dir, anal_type, subDir, sample, 'Summary')

    if subDir is None :
        init('No registration in database')
    if not os.path.isdir(smDir) :
        init('Summary folder not created')

    if anal_type == 'eWES' :
        remove_ewes(sample, smDir)
    elif anal_type == 'WTS' :
        remove_wts(sample, smDir)


