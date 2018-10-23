from k.util.DbCreator import DbCreator;
from k.manager.Kmanager import KManager;
from k.manager.FinManager import FinManager;
from k.puller.SharePuller import SharePuller;
import sys, getopt
import datetime;


def main(argv):
    create_db = False;
    pull_list = False;
    pull_k_data = False;
    pull_f_data = False;
    kpi_k = False;
    kpi_f = False;
    start_date = datetime.datetime.now().strftime('%Y-%m-%d');

    try:
        opts, args = getopt.getopt(argv, "hcfks:", ["pl", "pk", 'pf', 'sdate='])
    except getopt.GetoptError:
        print('Kmain.py -c --pl --pk --pf -f -k -s <date> --sdate=<date>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('Kmain.py -c --pl --pk --pf -f -k -s <date> --sdate=<date>')
            sys.exit()
        elif opt == '-c':
            create_db = True;
        elif opt == '--pl':
            pull_list = True;
        elif opt == '--pk':
            pull_k_data = True;
        elif opt == '--pf':
            pull_f_data = True;
        elif opt == '-k':
            kpi_k = True;
        elif opt == '-f':
            kpi_f = True;
        elif opt in ("-s", "--sdate"):
            start_date = arg

    if (create_db):
        dc = DbCreator()
        dc.init_create_table();

    if (pull_list):
        sp = SharePuller();
        sp.pull();

    if (pull_k_data):
        KManager.pull_data(start_date);
    if (kpi_k):
        KManager.count_kpi(start_date);

    if (pull_f_data):
        FinManager.pull_data();
    if (kpi_f):
        FinManager.count_kpi();

    print('finish OK')

if __name__ == "__main__":
    main(sys.argv[1:])
