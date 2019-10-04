import os
import datetime

def get_timestamp():

    dt = datetime.datetime.now()
    return dt.strftime("%y%m%d-%H%M%S")

def abspath_from( relative_path, current_file=__file__ ):  # to : relative_path
    my_path = os.path.abspath( os.path.dirname( current_file ) )
    abspath = os.path.join( my_path, relative_path )
    return abspath
