"""Serial parser/filter/logger module"""
import logging
import time
import re

__log__ = logging.getLogger(__name__)


# current sensor log IDs dictionary containing tuples of
# (last current display time, last displayed current value)
CURRENT_SENSORS = {"X": (0, 0), "Y": (0, 0), "Z": (0, 0)}

# other log IDs are added here
MISC_LOG_IDS = {"A", "B"}

# time threshold
THRESH_T = 10

# upper current threshold
THRESH_U = 10

# lower current threshold
THRESH_D = 10


def start_stefparse(ser):
    last_c_log = -10

    while True:
        for line in ser.readlines():

            # ignore blank lines
            if not line.strip():
                continue

            m = re.search("(\d{2}:\d{2}:\d{2}\.\d{3})([A-Za-z\s]\s*)(.*)", line)

            log_str = "RAW_LOG - {}".format(line)
            __log__.debug(log_str)

            try:
                log_time = m.group(1)
                log_id = m.group(2).strip()
                log_mssg = m.group(3).strip()
            except:
                log_str = "CORRUPT_LOG - {}".format(line)
                __log__.debug(log_str)
                continue

            if log_id in CURRENT_SENSORS:
                current_val = float(log_mssg)
                # limit filter current logs as they are spammy
                if time.time() > CURRENT_SENSORS[log_id][0] + THRESH_T or \
                   current_val >= CURRENT_SENSORS[log_id][1] + THRESH_U or \
                   current_val <= CURRENT_SENSORS[log_id][1] - THRESH_D:

                    log_str = "CURRENT_{}_LOG - {}{} \t{}".format(
                        log_id,
                        log_time,
                        log_id,
                        log_mssg,
                    )
                    __log__.info(log_str)

                    # update current id current value and log time
                    CURRENT_SENSORS[log_id] = (time.time(), current_val)

            elif log_id in  MISC_LOG_IDS:
                log_str = "{}_LOG - {}{} \t{}".format(
                    log_id,
                    log_time,
                    log_id,
                    log_mssg,
                )
                __log__.info(log_str)
            else:
                log_str = "UNKNOWN_LOG - {}".format(line.strip())
                __log__.warning(log_str)
