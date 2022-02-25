import os
import re
import logging
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

# LINE_COUNT=100000
# SCRIPT_LOCATION='C:\\Users\\Admin\\Documents\\Projects\\queue_checker\\queue_web'
# SMS_SERVER_LOCATION = 'C:\\Users\\Admin\\Documents\\Projects\\queue_checker\\queue_web'
# SMS_SERVER_LOG_FILE = 'SMSServer.log'
# FILTERED_LOG_FILE = SCRIPT_LOCATION + os.path.sep + 'SMSServer.log'

SCRIPT_LOCATION = os.getenv('SCRIPT_LOCATION')
SMS_SERVER_LOG_FILE = os.getenv('SMS_SERVER_LOG_FILE')
FILTERED_LOG_FILE = os.getenv('FILTERED_LOG_FILE')
DJANGO_ENV = os.getenv('DJANGO_ENV') if os.getenv('DJANGO_ENV') else 'TEST'
LOG_DATE_FORMAT = os.getenv('LOG_DATE_FORMAT') if os.getenv('LOG_DATE_FORMAT') else '%Y%m%d %H:%M:%S'
ITELBILLING_DBNAME = os.getenv('ITELBILLING_DBNAME')
DBHOST = os.getenv('DBHOST')
DBUSER = os.getenv('DBUSER')
DBPASSWORD = os.getenv('DBPASSWORD')
DBPORT = os.getenv('DBPORT')
DBNAME = os.getenv('DBNAME')


if DJANGO_ENV == 'LIVE':
    import MySQLdb


# Todo: https://stackoverflow.com/questions/136168/get-last-n-lines-of-a-file-similar-to-tail
# Todo: file conversion not working
# Todo: Need to check from live server


def copy_log_file(line_count=100000):
    try:
        copy_cmd = f'tail -{line_count} {SMS_SERVER_LOG_FILE} > {FILTERED_LOG_FILE}'
        # logger.debug(f'{copy_cmd}')
        logger.debug(os.system(copy_cmd))
    except Exception as e:
        logger.debug(f'{e}')


def time_filtered_info(lines_list, report_time=0):
    try:
        report_min = 5  # In minutes
        report_gen_time = int(str(datetime.now().timestamp()).split('.')[0])
        report_search_time = report_gen_time - (report_min * 60)
        if DJANGO_ENV == 'TEST':
            report_search_time = 1645712075
        time_filtered_list = []
        logger.debug(len(lines_list))
        for i in range(len(lines_list) - 1, 0, -1):
            if str(lines_list[i][0]) >= str(report_search_time):
                logger.debug(f'{i}: {lines_list[i]}')
                logger.debug(f'{i}: {lines_list[i][2]}, {lines_list[i][3]}, {lines_list[i][4]}, {lines_list[i][5]}')
                try:
                    if lines_list[i][4] > 0 or lines_list[i][5] > 0:
                        if len(time_filtered_list) > 0:
                            if len([x for x in time_filtered_list if lines_list[i][3] in x and lines_list[i][2] in x]) == 0:
                                # logger.debug(f'{lines_list[i]}')
                                time_filtered_list.append(['', lines_list[i][2], lines_list[i][3], lines_list[i][4],
                                                           lines_list[i][5]])
                            else:
                                # logger.debug(f'{lines_list[i]}')
                                pass
                        else:
                            time_filtered_list.append(['', lines_list[i][2], lines_list[i][3], lines_list[i][4],
                                                       lines_list[i][5]])
                    else:
                        # logger.debug(f'{lines_list[i]}')
                        pass
                except Exception as e:
                    logger.debug(f'{e}')
            # else:
            #     logger.info(f'{lines_list[i]}')
        return time_filtered_list
    except Exception as e:
        logger.debug(f'{e}')
        return []


def get_provider_data(provider_id_list=[]):
    provider_dict = {}
    # logger.debug(f'{DBHOST, DBUSER, DBPASSWORD, ITELBILLING_DBNAME}')
    try:
        db = MySQLdb.connect(DBHOST, DBUSER, DBPASSWORD, ITELBILLING_DBNAME)
        if len(provider_id_list) > 0:
            query = f"""SELECT spcProviderID, spcProviderName
            FROM {ITELBILLING_DBNAME}.vbSMSProviderCredentials 
            WHERE spcProviderID in ({', '.join([str(x) for x in provider_id_list])})"""
            cursor = db.cursor()
            cursor.execute(query)
            for i in cursor.fetchall():
                provider_dict[i[0]] = i[1]
        db.close()
    except Exception as e:
        logger.debug(f'{e}')
    finally:
        return provider_dict


def filter_log():
    lines = []
    # logger.debug(FILTERED_LOG_FILE)
    # logger.debug(LOG_DATE_FORMAT)
    try:
        fp = open(FILTERED_LOG_FILE, "r")
        for i in fp.readlines():
            # logger.debug(f'57: {type(i)} - {i}')
            line = re.findall(r'queue size for provider', i)
            # logger.debug(f'59: {line}')
            if line:
                a = i.replace('  ', ' ').replace('INFO', '').replace('ProviderDTO:', '').replace('queue size for', '')
                b = a.replace('is :', '').replace('is:', '').replace('and', '').replace('\n', '').replace('-', '')
                a = b.replace('campaign ', 'campaign').replace('campaign:', '').replace('  ', ' ')
                b = a.replace('provider:', '').split(' ')
                dt = int(str(datetime.strptime(' '.join(b[0:2]), LOG_DATE_FORMAT).timestamp()).split('.')[0])
                dt_ms = float(str(datetime.strptime(' '.join(b[0:2]), LOG_DATE_FORMAT).timestamp()))
                lines.append([dt, dt_ms, b[3], int(b[4]), int(b[5]), int(b[6])])
        fp.close()
        return lines
    except Exception as e:
        logger.debug(f'{e}')
        return []

# def main():
#     log_processor = LogFileProcessor()
#     line_list = log_processor.filter_log()
#     for i in line_list[-15:]:
#         logger.debug(i)
#
#
# if __name__ == '__main__':
#     ini_time_for_now = datetime.now()
#     main()
#     stopage_time = datetime.now()
#     logger.debug(f'Script Runtime: {str(stopage_time - ini_time_for_now)}')
