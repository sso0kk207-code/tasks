from collections import Counter
try:
    with open("30_01/access.log", "r") as f:
        data = f.readlines()

    gets = data.count("GET")
    posts = data.count("POST")
    puts = data.count("PUT")
    deletes = data.count("DELETE")

    logs = []
    summary_response = 0
    errors = 0
    ips = []
    agents = []

    for st in data:
        st = st.replace(" - - ", " ").replace('"', "").replace('\n', "")
        logs.append(st.split(" "))

    for log in logs:
        summary_response += float(log[-1])
        if log[5][0] in ['4', '5']:
            errors += 1
        ips.append(log[0])
        agents.append(log[-2].split('/', 1)[0])

    avg = summary_response / len(logs)

    print(f"====== Результаты анализа логов ======\nСреднее время ответа: {avg:.2f}\nКоличество ошибок: {errors}\nСамый популярный User-Agent: {Counter(agents).most_common(1)}\nТоп 10 по популярности ip:")
    print(Counter(ips).most_common(10))


except FileNotFoundError:
    print('Файл не был найден')