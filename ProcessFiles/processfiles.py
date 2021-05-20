from Processing import ProcessWeeksExcel1 as PWE1
from FileGather.FileSeeker import get_files
import time

root_dir_path = "Z:\\Informacion de estudiante en practica\\Archivos para indicadores de mantto\\MTTO CORRECTIVO - DMS\\2020\\SEMANAS"
"""La siguiente expresión hace match de los archivos que:
-no comienzan con "~" o con "Copia"
-que tienen: "mtto", "correc", "sem" y dos digitos en ese orden
-terminan con ".xlsx" o  "macro.xlsm"
"""
file_pattern_1 = "(?!~|Copia).*mtto.*correc.*.*sem.*0[1-8]((.xlsx)|(.*macro.xlsm))"
output_file="Z:\\Informacion de estudiante en practica\\Archivos para indicadores de mantto\\MTTO CORRECTIVO - DMS\Anual\\2020S01-08.xlsm"
r = get_files(root_dir_path, file_pattern_1)
for p in r:
    PWE1.main(str(p), output_file)
    time.sleep(3)
print(len(r))