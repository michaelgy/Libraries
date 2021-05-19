class ProcessFile:
    """Base class for processing files without output
    """
    def __init__(input_file:str):
        pass

class ProcessFileWF(ProcessFile):
    """Base class for processing files with output in the specify file
    """
    def __init__(input_file:str, output_file:str):
        pass