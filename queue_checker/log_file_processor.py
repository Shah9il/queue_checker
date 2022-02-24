import os
import sys
import re
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# LINE_COUNT=100000
# SCRIPT_LOCATION='C:\\Users\\Admin\\Documents\\Projects\\queue_checker\\queue_web'
# SMS_SERVER_LOCATION = 'C:\\Users\\Admin\\Documents\\Projects\\queue_checker\\queue_web'
# SMS_SERVER_LOG_FILE = 'SMSServer.log'
# FILTERED_LOG_FILE = SCRIPT_LOCATION + os.path.sep + 'SMSServer.log'

LINE_COUNT = os.getenv('LINE_COUNT')
SCRIPT_LOCATION = os.getenv('SCRIPT_LOCATION')
SMS_SERVER_LOG_FILE = os.getenv('SMS_SERVER_LOG_FILE')
FILTERED_LOG_FILE = os.getenv('FILTERED_LOG_FILE')

# Todo: https://stackoverflow.com/questions/136168/get-last-n-lines-of-a-file-similar-to-tail


def copy_log_file(line_count=100000):
    copy_cmd = f'tail -{line_count} {SMS_SERVER_LOG_FILE} > {FILTERED_LOG_FILE}'
    os.system(copy_cmd)


def time_filtered_info(lines_list, report_time=0):
    report_min = 5  # In minutes
    report_gen_time = int(str(datetime.now().timestamp()).split('.')[0])
    report_search_time = report_gen_time - (report_min * 60)
    report_search_time = 1645601486
    time_filtered_list = []
    for i in range(0, len(lines_list)):
        if str(lines_list[i][0]) >= str(report_search_time):
            time_filtered_list.append(lines_list[i])
    return time_filtered_list


#
# class LogFileProcessor:
#     def __init__(self):
#         self.source_log = SMS_SERVER_LOCATION + os.path.sep + SMS_SERVER_LOG_FILE
#         self.filtered_log = SMS_SERVER_LOCATION + os.path.sep + FILTERED_LOG_FILE

def filter_log():
    lines = []
    fp = open(FILTERED_LOG_FILE, "r")
    for i in fp.readlines():
        line = re.findall(r'queue size for provider', i)
        if line:
            a = i.replace('  ', ' ').replace('INFO', '').replace('ProviderDTO:', '').replace('queue size for', '')
            b = a.replace('is :', '').replace('is:', '').replace('and', '').replace('\n', '').replace('-', '')
            a = b.replace('campaign ', 'campaign').replace('campaign:', '').replace('  ', ' ')
            b = a.replace('provider:', '').split(' ')
            dt = int(str(datetime.strptime(' '.join(b[0:2]), '%Y%m%d %H:%M:%S').timestamp()).split('.')[0])
            lines.append([dt, b[3], b[4], b[5], b[6]])

    fp.close()
    return lines #, type(lines)

# def main():
#     log_processor = LogFileProcessor()
#     line_list = log_processor.filter_log()
#     for i in line_list[-15:]:
#         print(i)
#
#
# if __name__ == '__main__':
#     ini_time_for_now = datetime.now()
#     main()
#     stopage_time = datetime.now()
#     print(f'Script Runtime: {str(stopage_time - ini_time_for_now)}')
