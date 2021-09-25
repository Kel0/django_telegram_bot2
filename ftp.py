import time
import ftplib
import asyncio
# with ftplib.FTP('HOST', 'LOGIN', 'PASSWORD') as ftp:
#     ftp.cwd("input")
#     print(ftp.dir())


def send_to_ftp(telegram_id):
    try:
        with ftplib.FTP('ftp.almacloud.kz', 'umag', 'HCAJLzLd3XcK') as ftp:
            ftp.cwd("input")
            file = open(f"oneC{telegram_id}.txt", "rb")
            ftp.storbinary(f"STOR oneC{telegram_id}.txt", file)
            file.close()
        return True
    except:
        return

#
# def upload_from_ftp(telegram_id):
#     for _ in range(10):
#         try:
#             with ftplib.FTP('ftp.almacloud.kz', 'umag', 'HCAJLzLd3XcK') as ftp:
#                 ftp.cwd("output")
#                 ftp.retrbinary(f"RETR oneC{telegram_id}.txt", open(f'oneCoutput{telegram_id}.txt', 'wb').write)
#             return
#         except:
#             time.sleep(1)