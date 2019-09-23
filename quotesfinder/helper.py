import datetime

def get_timestamp():

    dt = datetime.datetime.now()
    return dt.strftime("%y%m%d-%H%M%S")
