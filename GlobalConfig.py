



ConfigDict={}

f1= open('/Users/zhoupj/Documents/svncode/flwm/config.txt', 'r')
lst = f1.readlines()
for i in range(0, len(lst)):
    if('#' in lst[i] or lst[i].strip()==''):
        continue;
    lst[i] = lst[i].strip('\n')
    sp=lst[i].split('=');
    ConfigDict[sp[0]]=sp[1]
    #dict[sp[0].strip()]=dict[sp[1].strip()]


if(__name__=='__main__'):
    print(ConfigDict)
