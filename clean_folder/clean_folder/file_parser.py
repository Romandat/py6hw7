import sys
from pathlib import Path

JPEG_IMAGES = []
JPG_IMAGES = []
PNG_IMAGES = []
SVG_IMAGES = []

AVI_VIDEOS = []
MP4_VIDEOS = []
MOV_VIDEOS = []
MKV_VIDEOS = []

DOC_FILES = []
DOCX_FILES = []
TXT_FILES = []
PDF_FILES = []
XLSX_FILES = []
PPTX_FILES = []

MP3_AUDIO = []
OGG_AUDIO = []
WAV_AUDIO = []
AMR_AUDIO = []

OTHER = []
ARCHIVES = []

REGISTER_EXTENSIONS = {
    'JPEG': JPEG_IMAGES,
    'PNG': PNG_IMAGES,
    'JPG': JPG_IMAGES,
    'SVG': SVG_IMAGES,
    'AVI': AVI_VIDEOS,
    'MP4': MP4_VIDEOS,
    'MOV': MOV_VIDEOS,
    'MKV': MKV_VIDEOS,
    'DOC': DOC_FILES,
    'DOCX': DOCX_FILES,
    'TXT': TXT_FILES,
    'PDF': PDF_FILES,
    'XLSX': XLSX_FILES,
    'PPTX': PPTX_FILES,
    'MP3': MP3_AUDIO,
    'OGG': OGG_AUDIO,
    'WAV': WAV_AUDIO,
    'AMR': AMR_AUDIO,
    'ZIP': ARCHIVES,
    'GZ': ARCHIVES,
    'TAR': ARCHIVES
}

FOLDERS = []
EXTENSIONS = set()
UNKNOWN = set()


def get_extension(filename: str) -> str:
    # превращаем расширение файла в название папки .jpg -> JPG
    return Path(filename).suffix[1:].upper()


def scan(folder: Path) -> None:
    for item in folder.iterdir():
        # Если это папка то добавляем ее с список FOLDERS и преходим к следующему элементу папки
        if item.is_dir():
            # проверяем, чтобы папка не была той в которую мы складываем уже файлы
            if item.name not in ('archives', 'video', 'audio', 'documents', 'images'):
                FOLDERS.append(item)
                #  сканируем эту вложенную папку - рекурсия
                scan(item)
            #  перейти к следующему элементу в сканируемой папке
            continue

        #  Пошла работа с файлом
        ext = get_extension(item.name)  # взять расширение
        fullname = folder / item.name  # взять полный путь к файлу
        if not ext:  # если у файла нет расширения добавить к неизвестным
            OTHER.append(fullname)
        else:
            try:
                # взять список куда положить полный путь к файлу
                container = REGISTER_EXTENSIONS[ext]
                EXTENSIONS.add(ext)
                container.append(fullname)
            except KeyError:
                # Если мы не регистрировали расширение в REGISTER_EXTENSIONS, то добавить в другое
                UNKNOWN.add(ext)
                OTHER.append(fullname)

def list_of_files (file_list: list) -> list:
    names_list = []
    for el in file_list:
        names_list.append(el.name)
    return names_list

if __name__ == '__main__':
    folder_for_scan = sys.argv[1]
    print(f'Start in folder {folder_for_scan}')

    scan(Path(folder_for_scan))
    print(f'Images jpeg: {JPEG_IMAGES}')
    print(f'Images jpg: {JPG_IMAGES}')
    print(f'Images svg: {SVG_IMAGES}')
    print(f'Audio mp3: {MP3_AUDIO}')
    print(f'Archives: {ARCHIVES}')

    print(f'Types of files in folder: {EXTENSIONS}')
    print(f'Unknown files of types: {UNKNOWN}')
    print(f'other: {OTHER}')

    print(FOLDERS[::-1])
