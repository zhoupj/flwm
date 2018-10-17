
class Pipeline:

    @staticmethod
    def execute(pre,algs:[],code,df,start_date,to_mysql=True):

        tuple = pre.process(df, start_date);
        if(not tuple[0]):
            return False;

        start=tuple[1];

        for alg in algs:
           succ=alg.run(code,df,start,to_mysql);
           if(not succ):
               return succ;

        return True;

