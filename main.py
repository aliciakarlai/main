import pandas as pd
from pyscript import document

def replace_backslashes(input_string):
    replaced_string = input_string.replace("\\", "//")
    replaced_string=replaced_string.replace('"','')
    return replaced_string

file_inpput=document

try:
    file=replace_backslashes(file_inpput)
    df = pd.read_excel(file)
except:
    output=print("INVALID file path "+file_inpput)
else:
    output=print("valid file path :)")