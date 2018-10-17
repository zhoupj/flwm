
class SortUtil:
    @staticmethod
    #1-100排名,返回第一个的排名，升序排名
    def rank(serial,num=100,index='last'):
        rl=SortUtil.rank_list(serial,num);
        if(index=='first'):
            return rl[0];
        else:
            return rl[-1];

    # 1-100排名
    #list 生序排名，返回list
    def rank_list(serial, num=100):
        serial_dup = serial.drop_duplicates(keep='first');
        dedup_count=serial_dup.shape[0];
        base = dedup_count / num;
        rank_list=[]
        dict = {};
        rs = serial_dup.rank();
        if (base<1):
            '''
            # 归一化排序
            min = serial_dup.min();
            max = serial_dup.max();
            rank_list= serial_dup.map(lambda x:(x-min)/(max-min)*100)
            '''
            #扩大倍数
            rank_list = rs.map(lambda x: int(x*num/dedup_count));

        else:

            rank_list = rs.map(lambda x:int((x+base-1)/base));

        rank_list=rank_list.values;#转换为list
        if(serial.shape[0]==dedup_count):
            return rank_list;

        for (val,rk) in zip(serial_dup.values,rank_list):
            dict[val]=int(rk);

        src_rank_list=[];
        for val in serial.values:
            src_rank_list.append(dict[val])

        return src_rank_list;

if (__name__ == '__main__'):
    import pandas as pd;
    df=pd.DataFrame([[100,8],[4,2],[3,5],[9,6],[0,4],[5,39],[36,98],[6,23],[9,3],[23,2]],columns=['a','b']);
    print(df)
    df=df['a'];
    print(SortUtil.rank(df, num=20))
    print(SortUtil.rank_list(df,num=20))