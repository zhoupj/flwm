from k.util.DbCreator import DbCreator;
from k.manager.Kmanager import KManager;
from k.manager.FinManager import FinManager;
from k.puller.SharePuller import  SharePuller;


sp=SharePuller();
sp.pull();


dc=DbCreator()
dc.init_create_table();

KManager.pull_data('2011-01-01');
KManager.count_kpi('2011-01-01');

FinManager.pull_data();
FinManager.count_kpi();

