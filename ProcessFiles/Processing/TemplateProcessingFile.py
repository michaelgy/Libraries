from BaseClasses import ProcessFileWF

class main(ProcessFileWF):
    def __init__(self, *args,**kargs):
        """All the configurations variables must be here"""
        super().__init__(*args,**kargs)
    
    def process(self):
        """The process to be performed must be here"""
        pass

if __name__ == "__main__":
    """Testing"""
    t = main(input_file="hello", output_file="world")
    print(t.input_file, t.output_file)