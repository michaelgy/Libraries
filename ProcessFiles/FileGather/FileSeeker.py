from typing import List, Union
from pathlib import Path
import re

def get_files(root_dir_path: str, file_pattern: str, max_depth_search : Union[int, None] = None, current_depth : int = 0, flags_regex=re.I) -> List[str]:
    p = Path(root_dir_path)
    pf = []
    if max_depth_search == None:
        cont = True
    else:
        cont = max_depth_search > current_depth
    if cont:
        for pi in p.iterdir():
            if pi.is_file() and re.fullmatch(file_pattern, pi.name, flags_regex):
                pf.append(pi)
            elif pi.is_dir():
                pf.extend(get_files(pi, file_pattern, max_depth_search, current_depth+1))
    return pf

if __name__ == "__main__":
    root_dir_path = "Z:\\Informacion de estudiante en practica\\Archivos para indicadores de mantto\\MTTO CORRECTIVO - DMS\\2020\\SEMANAS"
    
    """La siguiente expresión hace match de los archivos que:
    -no comienzan con "~" o con "Copia"
    -tienen: "mtto", "correc", "sem" y dos digitos en ese orden
    -terminan con ".xlsx" o  "macro.xlsm"
    """
    file_pattern = "(?!~|Copia).*mtto.*correc.*.*sem.*\d\d((.xlsx)|(.*macro.xlsm))"
    
    r = get_files(root_dir_path, file_pattern)
    for p in r:
        print(p.name,"\t",str(p))
    print(len(r))
