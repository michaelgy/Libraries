class ProcessFile:
    """Base class for processing files without output
    """
    def __init__(self, input_file:str):
        self.input_file = input_file
        

class ProcessFileWF(ProcessFile):
    """Base class for processing files with output in the specify file
    """
    def __init__(self, input_file:str, output_file:str):
        super().__init__(input_file)
        self.output_file = output_file