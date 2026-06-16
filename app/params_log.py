from datetime import datetime
pass_log_text = '# 192.30.253.112 - - [02.01.2018:20:59:51 +0100] "GET /dolorem/dicta.csv HTTP/1.0" 200 5039 "https://example1.com/" "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_9) AppleWebKit/5351 (KHTML, как у Геккона) Chrome/14.0.850.0 Safari/5351'
error_log_text = '# 192.30.253.112  Error 404'
current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
file_log = f"date_{current_datetime}.txt"