from app.common.Result import Result
class AppException(BaseException):
     def __init__(self, tuple): # real signature unknown
        lst=tuple[0]
        if(lst):
            print(lst);
            self.code=lst[0];
            self.err=lst[1];
            self.info=lst;
        else:
            self.code='none';
            self.err='noe';
            self.info=Result.UKNOWN
