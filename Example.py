#encoding=utf-8
import pandas as pd
import json
from app.common.AppException import AppException;
import  os
import numpy as np;

df=pd.DataFrame(data={'Num':[1,2,3],'char':['a','我','c']})
print(df.columns.values)
print(df)
b=(df.to_json(orient='records'));
print(b)
list=json.loads(b,encoding='utf-8');


js={
    'code':'123',
    'num':5,
    'data':None
}


print(json.dumps(['a','我','c'],ensure_ascii=False))
b=json.dumps(js,ensure_ascii=False);
print(b);
dict=json.loads(b)
print(dict)
dict['data']=json.loads(df.to_json(orient='records'))[0]
print(dict)
print(json.dumps((dict),ensure_ascii=False))

df=None;
df={}
df=''
print(df == None)
print(df is None)
a=[1]
if(a):
    print('ddd')

b={}
if(b):
    print('ddddddd')

try:
    e=['a','b','c']
    raise AppException(e);
except AppException as b:
    print(b.args[0])

print('%s|%s'%('a','b'))

print(df)
if  os.path.exists('a.txt'):
    os.remove('a.txt')


a=' ';
b={};
c=[]
d=None
e=()
f=0.0

if(a):
    print ('a');
if(b):
    print ('b');
if(c):
    print ('c');
if(d):
    print ('d')
if(e):
    print ('e');
if(f):
    print ('f');