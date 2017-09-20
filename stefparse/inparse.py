import logging
import time
import re


__log__ = logging.getLogger(__name__)


CURRENT_LOG_IDS = {"X", "Y", "Z"}
CURRENT_SENSORS = {"X": 0, "Y": 0, "Z": 0}
MISC_LOG_IDS = {"A", "B"}

# time threshold
THRESH_T = 10

# upper and lower current thresholds
THRESH_U = 10
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
                log_type = m.group(2).strip()
                log_text = m.group(3).strip()
            except:
                log_str = "CORRUPT_LOG - {}".format(line)
                __log__.debug(log_str)
                continue

            if log_type in CURRENT_LOG_IDS:
                # limit filter current logs as they are spammy
                if time.time() > last_c_log + THRESH_T or \
                   float(log_text) >= CURRENT_SENSORS[log_type] + THRESH_U or \
                   float(log_text) <= CURRENT_SENSORS[log_type] - THRESH_D:

                    log_str = "CURRENT_{}_LOG - {}{} \t{}".format(
                        log_type,
                        log_time,
                        log_type,
                        log_text,
                    )
                    __log__.info(log_str)

                    # update last current log time
                    last_c_log = time.time()
                    # update last current value
                    CURRENT_SENSORS[log_type] = float(log_text)

            elif log_type in  MISC_LOG_IDS:
                log_str = "{}_LOG - {}{} \t{}".format(
                    log_type,
                    log_time,
                    log_type,
                    log_text,
                )
                __log__.info(log_str)
            else:
                log_str = "UNKNOWN_LOG - {}".format(line.strip())
                __log__.warning(log_str)
