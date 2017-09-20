import logging
import time
import re

from stefparse import CURRENT_SERIAL_IDS, MISC_SERIAL_IDS


__log__ = logging.getLogger(__name__)

THRESH = 10

def start_stefparse(ser):
    last_c_log = -10
    c_sensors = {"X": 0, "Y": 0, "Z": 0}
    while True:
        for line in ser.readlines():
            if not line.strip():
                continue

            m = re.search("(\d{2}:\d{2}:\d{2}\.\d{3})([A-Za-z])(.*)", line)

            try:
                log_time = m.group(1)
                log_type = m.group(2)
                log_text = m.group(3)
            except:
                log_str = "BAD_LOG - {}".format(line)
                __log__.error(log_str)
                continue

            if log_type in CURRENT_SERIAL_IDS:
                old_c = c_sensors[log_type]
                if time.time() > last_c_log + THRESH or \
                   float(log_text) >= old_c + THRESH or \
                   float(log_text) <= old_c - 10:

                    log_str = "OK_CURRENT_LOG - {}{}{}".format(
                            log_time,
                            log_type,
                            log_text,
                        )
                    __log__.info(log_str)

                    # update last current log time
                    last_c_log = time.time()
                    # update last current value
                    old_c = float(log_text)

            elif m.group(2) in  MISC_SERIAL_IDS:
                log_str = "OK_LOG - {}{}{}".format(
                        log_time,
                        log_type,
                        log_text,
                    )
                __log__.info(log_str)
            else:  # some glitch junk
                log_str = "UNKNOWN_LOG - {}".format(line)
                __log__.debug(log_str)
