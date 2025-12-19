import shutil

def center_print(str,filler=" "):
    """Helperto print to center of console"""
    columns = shutil.get_terminal_size().columns
    print(str.center(columns,filler))