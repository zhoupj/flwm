import  datetime;


FORMAT='%Y-%m-%d';
class DateUtil:

    @staticmethod
    def getLongFormat(dt:datetime):
        return  dt.strftime('%Y-%m-%d %H:%M:%S');
    @staticmethod
    def getShortFromat(dt:datetime):
        return dt.strftime(FORMAT);
    @staticmethod
    def getNewFormat(dt:datetime):
        return dt.strftime('%Y%m%d%H%M%S');


    @staticmethod
    def getDateSeq(start:str):

        seq=[];
        now=datetime.datetime.now()
        s=datetime.datetime.strptime(start,FORMAT);
        ds = (now - s).days;

        while (ds >= 0):
            seq.append(s.strftime(FORMAT))
            s = s + datetime.timedelta(days=1);
            ds = (now - s).days;

        return seq;

    @staticmethod
    def getNextDay(dt:str):
        s = datetime.datetime.strptime(dt, FORMAT);
        s =s+datetime.timedelta(days=1)
        return s.strftime(FORMAT);

    @staticmethod
    def getLastDay(dt: str):
        s = datetime.datetime.strptime(dt, FORMAT);
        s = s - datetime.timedelta(days=1)
        return s.strftime(FORMAT);

    @staticmethod
    def getLastMonthForShort(dt: str):
        year=dt[0:4];
        month=dt[5:7];
        month=int(month)-1;
        if(month==0):
            year=int(year)-1;
            month=12;

        month='0'+str(month) if month<10 else str(month)
        year=str(year);
        return year+'-'+month;

    @staticmethod
    def getYear(dt:str):
        if(dt==None):
            return 0;
        return int(dt[0:4]);

    @staticmethod
    def getSeason(dt:str):
        if(dt==None):
            return 0;
        after_part=dt[5:];
        if (after_part >='01-01' and after_part <= '03-31'):
            return 1;
        if(after_part > '03-31' and  after_part <= '06-30'):
            return 2;
        if (after_part > '06-30' and after_part <= '09-30'):
            return 3;
        if (after_part > '09-30' and after_part <= '12-31'):
            return 4;
        return 0;

if (__name__ == '__main__'):
    print(DateUtil.getDateSeq('2018-10-11'))
    print(DateUtil.getDateSeq('2018-10-15'))
    print(DateUtil.getNextDay('2018-09-01'))
    print(DateUtil.getYear('2018-09-01'))
    print(DateUtil.getSeason('2018-08-30'))
    print(DateUtil.getLongFormat(datetime.datetime.now()))
    print(DateUtil.getLastMonthForShort('2018-01-01'))
    print(DateUtil.getLastMonthForShort('2018-05-31'))
    print(DateUtil.getLastMonthForShort('2018-05-01'))
    print(DateUtil.getLastMonthForShort('2018-12-31'))