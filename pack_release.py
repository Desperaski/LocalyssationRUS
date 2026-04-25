import json
import shutil
import zipfile
from pathlib import Path

ATLYSS_VERSION = "12026.a3"
DEV_NAME = "Fel1n, Desperaski"

# Настройка путей к файлам
# Путь к самим файлам локализации
SOURCE_DIR = Path(r"G:\SteamLibrary\steamapps\common\ATLYSS\BepInEx\plugins\LocalyssationRUS")

# Путь, в который будет помещён готовый архив
OUTPUT_DIR = Path(r"G:\ATLYSS modding\MY\LocalyssationRUS\dist")

# Путь, по которому будут скопированы файлы локализации на всякий случай
BACKUP_DIR = Path(r"G:\ATLYSS modding\MY\LocalyssationRUS")

# Путь к файлу с версией, для удобного версионирования, не залезая в этот скрипт каждый раз
VERSION_FILE = SOURCE_DIR / "version.json"

# Файлы, которые будут упакованы в архив
FILES_TO_PACK = [
    "RussianLanguage.ru-RU.yml",
    "localyssationLanguage.json",
    "icon.png",
    "README.md",
    "version.json"
]

# Обработка возможных ошибок
if not SOURCE_DIR.exists():
    print(f"[ОШИБКА] Папка не найдена: {SOURCE_DIR}")
    input()
    exit(1)

try:
    with open(VERSION_FILE, "r", encoding="utf-8") as f:
        VERSION = json.load(f)["version"]
except FileNotFoundError:
    print(f"[ОШИБКА] Файл не найден: {VERSION_FILE}")
    input()
    exit(1)
except json.JSONDecodeError:
    print(f"[ОШИБКА] Файл повреждён или не является валидным JSON: {VERSION_FILE}")
    input()
    exit(1)
except KeyError:
    print(f"[ОШИБКА] В {VERSION_FILE} нет поля 'version'")
    input()
    exit(1)

# Имя архива, который будет создан
OUTPUT_ZIP = f"LocalyssationRUS-{DEV_NAME}-v{VERSION}-{ATLYSS_VERSION}.zip"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
output_zip = OUTPUT_DIR / OUTPUT_ZIP

print(f"Исходная папка : {SOURCE_DIR}")
print(f"Пакуем архив    : {output_zip}")

print(f"\nКопируем в бэкап: {BACKUP_DIR}")
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

for file_name in FILES_TO_PACK:
    src = SOURCE_DIR / file_name
    dst = BACKUP_DIR / file_name
    if not src.exists():
        print(f"[ПРОПУСК] Файл не найден: {file_name}")
        continue
    shutil.copy2(src, dst)
    print(f"  -> {file_name}")

print(f"\nПакуем архив ...")

try:
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file_name in FILES_TO_PACK:
            file_path = SOURCE_DIR / file_name
            if not file_path.exists():
                print(f"[ПРОПУСК] Файл не найден: {file_name}")
                continue
            zf.write(file_path, file_name)
            print(f"  + {file_name}")
    print(f"\nАрхив успешно создан!\n{output_zip}")
except Exception as e:
    print(f"[ОШИБКА] {e}")
    input()
    exit(1)

input("Готово!")