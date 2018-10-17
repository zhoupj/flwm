import  re;

class StrUtil:

    @staticmethod
    def convert_to_dict(str,sp1='\n',sp2=': '):
        dt={}
        for line in str.split(sp1):
            if (line.find(sp2) > 0):
                arr = line.split(sp2, 1);
                dt[arr[0]] = arr[1];
        return dt;

    @staticmethod
    def parse_field(value):
        if (value == '--'):
            return None;
        if (u'万' in value):
            return float(re.sub(u'万', '', value));
        if (u'亿' in value):
            return float(re.sub(u'亿', '', value)) * 10000;
        if ('%' in value):
            return re.sub('%','',value);
        return value;

if(__name__=='__main__'):
    s='''
a: 2
b: sdfdfdfdfdf
    '''
    print(StrUtil.convert_to_dict(s));
    print(StrUtil.parse_field('14.3%'));
    print(StrUtil.parse_field('--'));
    print(StrUtil.parse_field('16万'));