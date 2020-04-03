import os, platform, ez, shutil

def check(src, dst, removeFile = False, removeFolder = False):
    src_list = os.listdir(src)
    dst_list = os.listdir(dst)
    for item in src_list:
        src_item = os.path.join(src, item)
        dst_item = os.path.join(dst, item)
        if os.path.isdir(src_item):
            if item in dst_list:
                check(src_item, dst_item, removeFile, removeFolder)
            else:
                shutil.copytree(src_item, dst_item)
                print(f'{src_item} is copied.')
        else:
            if item in dst_list:
                src_time = os.path.getmtime(src_item)
                dst_time = os.path.getmtime(dst_item)
                if src_time > dst_time:
                    shutil.copy2(src_item, dst_item)
                    print(f'{dst_item} is updated.')
##                elif src_time < dst_time:
##                    print(f'{src_item} is outdated.')
            else:
                shutil.copy2(src_item, dst)
                print(f'{src_item} is copied.')
    for item in set(dst_list) - set(src_list):
        path = os.path.join(dst, item)
        if os.path.isdir(path):
            if removeFolder:
                shutil.rmtree(path)
                print(f'{path} is deleted.')
            else:
                print(f'{path} doesn\'t exists in source.')
        else:
            print(removeFile)
            if removeFile:
                os.remove(path)
                print(f'{path} is deleted.')
            else:
                print(f'{path} doesn\'t exists in source')

if __name__ == '__main__':
##    ez.cddt()
    check(r'C:\Users\Seaky\AppData\Local\Programs\Python\Python38\Python Files', \
          r'E:\Python\Python Files',
          True,
          False)
