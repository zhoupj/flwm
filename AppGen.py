from k.util.DbCreator import DbCreator;
from k.manager.Kmanager import KManager;
from k.manager.FinManager import FinManager;
from k.puller.SharePuller import SharePuller;
import sys, getopt
import datetime;
from app.service.ArticleService import AS;

def main(argv):
    gen_art = False;

    try:
        opts, args = getopt.getopt(argv, "hg", [])
    except getopt.GetoptError:
        print('AppGen.py -g')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('-g 生成文章数据')
            sys.exit()
        elif opt == '-g':
            gen_art=True;


    if(gen_art):
        AS.add_test_date();

    print('finish OK')

if __name__ == "__main__":
    main(sys.argv[1:])
