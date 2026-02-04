from collections import Counter
import re

summary_response = errors = gets = posts = puts = deletes = 0

pattern = r'(?P<ip>\S+) - - \[(?P<date>.*?)\] "(?P<method>\w+) (?P<path>\S+) (?P<proto>.*?)" (?P<status>\d+) (?P<size>\d+) "(?P<agent>.*?)" (?P<time>\d+\.\d+)'

ips = []
agents = []

try:
    with open("30_01/access.log", "r") as f:
        for st in f:
            match = re.match(pattern, st)
            if not match:
                continue
            res = match.groupdict()
            summary_response += float(res['time'])
            if res['status'].startswith(("4", "5")):
                errors += 1
            if res['method'] == "GET":
                gets += 1
            elif res['method'] == "POST":
                posts += 1
            elif res['method'] == "PUT":
                puts += 1
            elif res['method'] == "DELETE":
                deletes += 1
            ips.append(res['ip'])
            agents.append(res['agent'].split('/')[0])

except FileNotFoundError:
    print('Файл не был найден')

avg = summary_response / len(ips) if ips else 0

print(f"====== Результаты анализа логов ======\nКоличество методов GET: {gets}\nКоличество методов POST: {posts}\nКоличество методов PUT: {puts}\nКоличество методов DELETE: {deletes}\nСреднее время ответа: {avg:.2f}\nКоличество ошибок: {errors}\nСамый популярный User-Agent: {Counter(agents).most_common(1)[0][0]}\nТоп 10 по популярности ip:")
for ip in enumerate(dict(Counter(ips).most_common(10)).keys(), start=1):
    print(ip)
