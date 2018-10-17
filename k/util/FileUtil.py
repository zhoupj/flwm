import os
class FileUtil:
    @staticmethod
    def list_all_files(rootdir,suffix):
        _files = []
        list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
        for f in list:
            path = os.path.join(rootdir,f)
            if os.path.isdir(path):
                _files.extend(FileUtil.list_all_files(path))
            elif os.path.isfile(path):
                if(path.endswith(suffix)):
                    _files.append(path)
        return _files