"""Serial parser/filter/logger module"""
import logging
import re
import time

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
    """While loop that continually parses/filters/logs serial input"""
    while True:
        for line in ser.readlines():
            # ignore blank lines
            if not line.strip():
                continue
            __log__.debug("RAW_LOG - {}".format(line))

            m = re.search("(\d{2}:\d{2}:\d{2}\.\d{3})([A-Za-z\s]\s*)(.*)", line)

            try:
                log_time = m.group(1)
                log_id = m.group(2).strip()
                log_mssg = m.group(3).strip()
            except (TypeError, AttributeError):
                __log__.debug("CORRUPT_LOG - {}".format(line))
                continue

            if log_id in CURRENT_SENSORS:
                current_val = float(log_mssg)
                # limit filter current logs
                if time.time() > CURRENT_SENSORS[log_id][0] + THRESH_T or \
                   current_val >= CURRENT_SENSORS[log_id][1] + THRESH_U or \
                   current_val <= CURRENT_SENSORS[log_id][1] - THRESH_D:
                    __log__.info("CURRENT_{}_LOG - {}{} \t{}".format(
                            log_id,
                            log_time,
                            log_id,
                            log_mssg,
                        )
                    )

                    # update current id current value and log time
                    CURRENT_SENSORS[log_id] = (time.time(), current_val)

            elif log_id in MISC_LOG_IDS:
                __log__.info("{}_LOG - {}{} \t{}".format(
                        log_id,
                        log_time,
                        log_id,
                        log_mssg,
                    )
                )

            else:
                __log__.warning("UNKNOWN_{}_LOG - {}{} \t{}".format(
                        log_id,
                        log_time,
                        log_id,
                        log_mssg,
                    )
                )