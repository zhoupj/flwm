import sys, getopt
import datetime;
import pandas as pd;
import  numpy as np;
import os;


K_RETRY={
  'pd':[],
  'ph':[],
  'ks':[],
  'km':[]
}

def print_help():
    print('python Kmain.py <options>[as follows]')
    print(''' 
        -c 创建db
        --pl 拉列表
        --pk 拉k线数据（包括港资数据）
        --ph 仅拉取港资数据
        --pf 拉财务数据
        -f 计算财务数据指标
        -k 计算k线数据指标
        -s <date> 开始拉k线数据和计算k线数据指标日期，格式:2011-01-01,
        --kc 开始拉k线数据和计算k线数据指标code
        -r 重试线数据和计算k线数失败的，
                ''')


def main(argv):
    create_db = False;
    pull_list = False;
    pull_k_data = False;
    pull_k_h_data = False;
    pull_f_data = False;
    kpi_k = False;
    kpi_f = False;
    retry = False;
    start_date = datetime.datetime.now().strftime('%Y-%m-%d');
    start_code=None;

    try:
        opts, args = getopt.getopt(argv, "hcfkrs:", ["pl", "pk","ph" 'pf', 'kc='])
    except getopt.GetoptError:

        print_help();
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print_help()
            sys.exit()
        elif opt == '-c':
            create_db = True;
        elif opt == '--pl':
            pull_list = True;
        elif opt == '--pk':
            pull_k_data = True;
        elif opt=='--ph':
            pull_k_h_data=True;
        elif opt == '--pf':
            pull_f_data = True;
        elif opt == '-k':
            kpi_k = True;
        elif opt == '-f':
            kpi_f = True;
        elif opt in ("-s", "--sdate"):
            start_date = arg
        elif opt == '-r':
            retry = True;
        elif opt=='--kc':
            start_code=arg;

    from k.util.DbCreator import DbCreator;
    from k.manager.Kmanager import KManager;
    from k.manager.FinManager import FinManager;
    from k.puller.SharePuller import SharePuller;
    from GlobalConfig import ConfigDict;

    if (retry):

        df=pd.DataFrame();
        if os.path.exists(ConfigDict['k_fail_log']):
            df = pd.read_csv(ConfigDict['k_fail_log'], index_col=0,dtype={'code':np.str,'type':np.str});
            print(df)
            if os.path.exists(ConfigDict['k_fail_log'] + '.pre'):
                 os.remove(ConfigDict['k_fail_log'] + '.pre')
            os.rename(ConfigDict['k_fail_log'],ConfigDict['k_fail_log'] + '.pre')
            new_df = pd.DataFrame(data=None, columns=['type', 'code']);
            new_df.to_csv(ConfigDict['k_fail_log'], mode='w')

        for i in range(df.shape[0]):
            if (df.loc[i, 'type'] == 'pd'):
                K_RETRY['pd'].append(df.loc[i, 'code']);
            elif (df.loc[i, 'type'] == 'ph'):
                K_RETRY['ph'].append(df.loc[i, 'code']);
            elif (df.loc[i, 'type'] == 'ks'):
                K_RETRY['ks'].append(df.loc[i, 'code']);
            elif (df.loc[i, 'type'] == 'km'):
                K_RETRY['km'].append(df.loc[i, 'code']);
        print(K_RETRY)

    if(not os.path.exists(ConfigDict['k_fail_log'])):
        new_df = pd.DataFrame(data=None, columns=['date','type', 'code']);
        new_df.to_csv(ConfigDict['k_fail_log'], mode='w')


    if (create_db):
        dc = DbCreator()
        dc.init_create_table();

    if (pull_list):
        sp = SharePuller();
        sp.pull();

    if (pull_k_data):
        KManager.pull_data(start_date,start_code=start_code,retry=retry,retryDict=K_RETRY);
        KManager.pull_data_hk(start_date,start_code=start_code,retry=retry,retryDict=K_RETRY);
    if(pull_k_h_data):
        KManager.pull_data_hk(start_date, start_code=start_code, retry=retry, retryDict=K_RETRY);
    if (kpi_k):
        KManager.count_kpi(start_date,start_code=start_code,retry=retry,retryDict=K_RETRY);

    if (pull_f_data):
        FinManager.pull_data();
    if (kpi_f):
        FinManager.count_kpi();


    print('finish OK')


if __name__ == "__main__":
    main(sys.argv[1:])
