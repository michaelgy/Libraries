from Processing import ProcessWeeksExcel1 as PWE1, ProcessWeeksExcel2 as PWE2
from FileGather.FileSeeker import get_files
import time


root_dir_path = "Z:\\Informacion de estudiante en practica\\Archivos para indicadores de mantto\\MTTO CORRECTIVO - DMS\\2020\\SEMANAS"

def procesar1():
    """La siguiente expresión hace match de los archivos que:
    -no comienzan con "~" o con "Copia"
    -que tienen: "mtto", "correc", "sem", "0" y algun digito del 1 al 8 (todas las condiciones en el orden mencionado)
    -terminan con ".xlsx" o  "macro.xlsm"
    """
    file_pattern_1 = "(?!~|Copia).*mtto.*correc.*.*sem.*0[1-8]((.xlsx)|(.*macro.xlsm))"
    output_file="Z:\\Informacion de estudiante en practica\\Archivos para indicadores de mantto\\MTTO CORRECTIVO - DMS\Anual\\2020S01-08.xlsm"
    r = get_files(root_dir_path, file_pattern_1)
    for p in r:
        PWE1.main(str(p), output_file)
        time.sleep(3)
    print(len(r))

def procesar2():
    """La siguiente expresión hace match de los archivos que:
    -no comienzan con "~" o con "Copia"
    -que tienen: "mtto", "correc", "sem", "0" y algun digito del 1 al 8 (todas las condiciones en el orden mencionado)
    -terminan con ".xlsx" o  "macro.xlsm"
    """
    file_pattern_1 = "(?!~|Copia).*mtto.*correc.*.*sem.*(09|1[0-9]|20)((.xlsx)|(.*macro.xlsm))"
    output_file="Z:\\Informacion de estudiante en practica\\Archivos para indicadores de mantto\\MTTO CORRECTIVO - DMS\Anual\\2020S09-20.xlsm"
    r = get_files(root_dir_path, file_pattern_1)
    for p in r:
        print(p.name)
        #PWE2.main(str(p), output_file)
        #time.sleep(3)
    print(len(r))

if __name__ == "__main__":
    #procesar1()
    procesar2()