import pathlib
from pathlib import Path
import re
import shutil
import sys

def customize_file(file):
    return translate(pathlib.PurePath(file).stem)+pathlib.PurePath(file).suffix


def delete_empty(list_dir_del):
    for dir_del in list_dir_del:
        try:
            Path(dir_del).rmdir()
        except OSError:
           continue


def input_folder():
    while True:
        folder = input(
            'Введите папку для разбора(парсинга): или "ex" для выхода из программы:-->')
        if folder == 'ex':
            exit()
        elif pathlib.Path(folder).exists():
            return folder
            break
        else:
            print("Неправильно! Попробуй ещё ")
            
            
def parsing(parce_folder):

    list_dir = []
    list_files = []
    list_dir.append(parce_folder)
    list_dir_del = []

    while list_dir:
        work_dir = list_dir[0]
        list_files.extend(parse_folder(Path(work_dir))[0])
        list_dir.extend(parse_folder(Path(work_dir))[1])
        use_dir = list_dir.pop(0)
        list_dir_del.append(use_dir)
    list_dir_del.pop(0)
    return list_files, list_dir_del


def parse_folder(path):
    not_touch = ('video', 'audio', 'archives', 'images', 'documents')
    files = []
    folders = []
    real_folders = []
    p = Path(path)

    for i in path.iterdir():
        if i.is_dir() and not i.name in not_touch:
            folders.append(i.name)

        elif i.is_file:
            files.append(str(path)+'/'+i.name)

    for folder in folders:

        real_folders.append(str(path)+'/'+folder)

    return files, real_folders


def sort_list_files(list_files):
    no_id = []
    exp = {('audio', "wav", "mp3", "ogg", "amr"): [], ('images', 'jpeg', 'png', 'jpg', 'svg'): [], ('documents', 'doc', 'docx', 'txt',
                                                                                                    'pdf', 'xls', 'xlsx', 'pptx', 'ppt'): [], ('video', 'avi', 'mp4', 'mov', 'mkv'): [], ('archives', 'zip', 'gz', 'tar'): []}
    work_list = list_files.copy()

    for elem in work_list:
        expansion = elem.split('.')[-1]
        
        for key, val in exp.items():
            if expansion in key:
                val.append(elem)

                list_files.remove(elem)
    return exp


def transfer(sort_files, parce_folder):
    for dir, files in sort_files.items():
        p = Path(parce_folder).joinpath(dir[0])
        pathlib.Path(p).mkdir(parents=True, exist_ok=True)

        for file in files:
            shutil.move(file, str(p)+'/' + customize_file(file))


def translate(name):
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                   "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

    TRANS = {}
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()

    return re.sub(r'\W', '_', name.translate(TRANS))


def unpack(arc):
    if any(arc.iterdir()):
        archive_list = parse_folder(arc)
        for file in archive_list[0]:
            try:
                arch_path = str(pathlib.Path(file).parent) + \
                    '/'+pathlib.PurePath(file).stem
                shutil.unpack_archive(file, arch_path)
            except shutil.ReadError:
                pass








def main():
    try:
        if pathlib.Path(sys.argv[1]).exists():
            parce_folder=sys.argv[1]
    
        else:
            print('!!!!No such folder!!!!')
            exit()
    except IndexError:
        print("Please, add folder!!!!!")  
        exit()  
   
    sorted = parce_folder # можно отдельно указать,например: +/sorted
    list_files, list_dir_del = parsing(parce_folder) # распарcинг папки

    sort_files=sort_list_files(list_files) # сортировка файлов по типам

    transfer(sort_files, parce_folder) # сортировка файлов по новым папкам

    arc=Path(sorted).joinpath('archives')
    unpack(arc) #  обработка архивов-разархивирование
    
    delete_empty(list_dir_del) # удаление пустых папок
  
if __name__== '__main__':
    main()











    
    
    
    
    

    

    

    
