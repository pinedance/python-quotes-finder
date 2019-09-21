import time

def get_output_path():

    now = time.gmtime( time.time() )
    return "output-{:02d}{:02d}{:02d}-{:02d}{:02d}{:02d}"\
        .format( now.tm_year, now.tm_mon, now.tm_mday,\
                 now.tm_hour, now.tm_min, now.tm_sec )
