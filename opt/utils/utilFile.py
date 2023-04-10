import os
import shutil

#保存先のフォルダが存在しなければ作成しファイルコピーをする
def file_copy(copy_from,copy_to):
    if os.path.exists(os.path.dirname(copy_to)):
        os.makedirs(copy_to)
    shutil.copyfile(copy_from,copy_to)

def make_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)