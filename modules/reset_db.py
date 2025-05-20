import os
import sys
import pymysql
import warnings
import datetime
import pandas as pd
from pathlib import Path
from .commom import *

def reset_ewes(sample, flag):
    try :
        connection = pymysql.connect(host="192.168.9.100", user="gxd_pipeline", password="gw!2341234", database="gxd")
        connection.autocommit(False)
        try:
            with connection.cursor() as cursor:
                cursor.execute(del_alt_snv(sample))
                cursor.execute(del_snv_indeterminate(sample))
                cursor.execute(del_alt_cnv(sample))
                cursor.execute(del_alt_msi(sample))
                cursor.execute(del_alt_tmb(sample))
                cursor.execute(del_qc(sample))
                if flag:
                    cursor.execute(upd_history_1(sample, '100'))
                    cursor.execute(upd_history_2(sample, '100'))
                    print('update status:100')
                else :
                    cursor.execute(upd_history_1(sample, '101'))
                    cursor.execute(upd_history_2(sample, '101'))
                    print('update status:101')
                connection.commit()

        except pymysql.MySQLError as e:
            print(f"database error: {e}")
            connection.rollback()
        except Exception as e:
            print(f"unexpected error: {e}")
            connection.rollback()
        finally:
            connection.close()
            print('Complete database update')

    except pymysql.MySQLError as e:
        print(f"connection error: {e}")
    except Exception as e:
        print(f"unexpected error: {e}")

def reset_wts(sample, flag):
    try :
        connection = pymysql.connect(host="192.168.9.100", user="gxd_pipeline", password="gw!2341234", database="gxd")
        connection.autocommit(False)
        try:
            with connection.cursor() as cursor:
                cursor.execute(del_alt_splice(sample))
                cursor.execute(del_alt_sv(sample))
                cursor.execute(del_alt_express(sample))
                cursor.execute(del_qc(sample))
                if flag :
                    cursor.execute(upd_history_1(sample, '100'))
                    cursor.execute(upd_history_2(sample, '100'))
                    print('update status:100')
                else :
                    cursor.execute(upd_history_1(sample, '101'))
                    cursor.execute(upd_history_2(sample, '101'))
                    print('update status:101')
                connection.commit()
        except pymysql.MySQLError as e:
            print(f"database error: {e}")
            connection.rollback()
        except Exception as e:
            print(f"unexpected error: {e}")
            connection.rollback()

        finally:
            connection.close()
            print('Complete database update')

    except pymysql.MySQLError as e:
        print(f"connection error: {e}")
    except Exception as e:
        print(f"unexpected error: {e}")


def del_alt_snv(sample):
    query = f'''
    delete from gc_alter_snv
    WHERE SAMPLE_ID = '{sample}'
    AND idx = (SELECT MAX(ghl_inner.idx) FROM gc_history_log ghl_inner WHERE ghl_inner.SAMPLE_ID = '{sample}')
    '''
    return query

def del_snv_indeterminate(sample):
    query = f'''
    delete from gc_snv_indeterminate
    WHERE SAMPLE_ID = '{sample}'
    AND idx = (SELECT MAX(ghl_inner.idx) FROM gc_history_log ghl_inner WHERE ghl_inner.SAMPLE_ID = '{sample}')
    '''
    return query

def del_alt_cnv(sample):
    query = f'''
    delete from gc_alter_cnv
    WHERE SAMPLE_ID = '{sample}'
    AND idx = (SELECT MAX(ghl_inner.idx) FROM gc_history_log ghl_inner WHERE ghl_inner.SAMPLE_ID = '{sample}')
    '''
    return query

def del_alt_msi(sample):
    query = f'''
    delete from gc_alter_msi
    WHERE SAMPLE_ID = '{sample}'
    AND idx = (SELECT MAX(ghl_inner.idx) FROM gc_history_log ghl_inner WHERE ghl_inner.SAMPLE_ID = '{sample}')
    '''
    return query

def del_alt_tmb(sample):
    query = f'''
    delete from gc_alter_tmb
    WHERE SAMPLE_ID = '{sample}'
    AND idx = (SELECT MAX(ghl_inner.idx) FROM gc_history_log ghl_inner WHERE ghl_inner.SAMPLE_ID = '{sample}')
    '''
    return query

def del_qc(sample):
    query = f'''
    delete from gc_qc_bi
    WHERE SAMPLE_ID = '{sample}'
    AND idx = (SELECT MAX(ghl_inner.idx) FROM gc_history_log ghl_inner WHERE ghl_inner.SAMPLE_ID = '{sample}')
    '''
    return query

def upd_history_1(sample, status_num:str):
    query = f'''
    UPDATE gc_history_log ghl
    SET ghl.ANAL_STATUS = '{status_num}'
    WHERE ghl.SAMPLE_ID = '{sample}'
    AND ghl.idx = (SELECT MAX(ghl_inner.idx) FROM gc_history_log ghl_inner WHERE ghl_inner.SAMPLE_ID = '{sample}')
    '''
    return query

def upd_history_2(sample, status_num:str):
    query = f'''
    UPDATE gc_qc_sample gqs
    SET gqs.ANAL_STATUS = '{status_num}'
    WHERE gqs.SAMPLE_ID = '{sample}'
    '''
    return query

def del_alt_splice(sample):
    query = f'''
    delete from gc_alter_splice
    WHERE SAMPLE_ID = '{sample}'
    AND idx = (SELECT MAX(ghl_inner.idx) FROM gc_history_log ghl_inner WHERE ghl_inner.SAMPLE_ID = '{sample}')
    '''
    return query

def del_alt_sv(sample):
    query = f'''
    delete from gc_alter_sv
    WHERE SAMPLE_ID = '{sample}'
    AND idx = (SELECT MAX(ghl_inner.idx) FROM gc_history_log ghl_inner WHERE ghl_inner.SAMPLE_ID = '{sample}')
    '''
    return query

def del_alt_express(sample):
    query = f'''
    delete from gc_alter_express
    WHERE SAMPLE_ID = '{sample}'
    AND idx = (SELECT MAX(ghl_inner.idx) FROM gc_history_log ghl_inner WHERE ghl_inner.SAMPLE_ID = '{sample}')
    '''
    return query


def reset_db(args):

    sample = args.sample
    anal_dir = args.analysis_dir
    status = args.roll_back

    subDir, anal_type = getbatch(sample, anal_dir)
    if subDir is None :
        print('No registration in database')
        sys.exit()

    pdf = os.path.join(anal_dir, anal_type, subDir, sample, 'Summary', sample+'.report.pdf')
    json = os.path.join(anal_dir, anal_type, subDir, sample, 'Summary', sample+'.report.json')

    if os.path.isfile(pdf) :
        mtime = datetime.datetime.fromtimestamp(os.path.getmtime(pdf)).strftime('%m%d%H%M')
        os.rename( pdf, os.path.join(anal_dir, anal_type, subDir, sample, 'Summary', sample + '.' + mtime +'.report.pdf') )

    if os.path.isfile(json) :
        mtime = datetime.datetime.fromtimestamp(os.path.getmtime(json)).strftime('%m%d%H%M')
        os.rename( json, os.path.join(anal_dir, anal_type, subDir, sample, 'Summary', sample + '.' + mtime +'.report.json') )

    if anal_type == 'eWES' :
        reset_ewes(sample, status)
    elif anal_type == 'WTS' :
        reset_wts(sample, status)


