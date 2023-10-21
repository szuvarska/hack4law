import requests
import pandas as pd
import time
import threading

# downloading all courts data from API and retreiving ids of regional and distict civil departments
out_data = []
print(f"Downloading civil department ids...")
for i in range(4):
    judgments_url = "https://www.saos.org.pl/api/dump/commonCourts?pageSize=100&pageNumber={}".format(i)
    dane = requests.request("GET", judgments_url, data={}).json()

    for x in dane['items']:
        out_data.append(x)

df = pd.DataFrame(out_data)
court_ids = df[df['type']!="APPEAL"]['divisions']\
    .apply(lambda x: [d['id'] for d in x if d['type'] == 'Cywilny'])\
    .explode('divisions').tolist()

# downloading filtered judgments with partial judgments content text
id_pool = court_ids.copy()
DOWNLOAD_BASE_URL = "https://www.saos.org.pl/api/search/judgments?&pageSize=100&judgmentTypes=SENTENCE&judgmentTypes=REASONS&ccDivisionId={dep_id}"
output_list = []

print(f"Downloading judgments from {len(id_pool)} court departments...")
def thread_func(id_pull: list[int], answer_list: list):
    while len(id_pull) > 0:
        dep_id = id_pull.pop(0)
        print(f"Dowlnoading from {dep_id} department")
        durl = DOWNLOAD_BASE_URL.format(dep_id=str(dep_id))

        def thread_download(url: str):
            try:
                res = requests.get(url)
                if res.status_code == 200:
                    return res.json()
                else:
                    print(f"Error: {res.status_code}")
                    return thread_download(url)
            except Exception as e:
                print(e)
                print(f"Retyring in 1 minute")
                time.sleep(10)
                return thread_download(url)

        downloaded = thread_download(durl)
        print(f"Downloaded from {dep_id}")
        answer_list.append((dep_id, downloaded))
        print(f"Currently downloaded {len(answer_list)}")

threads = []
for i in range(10):
    t = threading.Thread(target=thread_func, args=(id_pool, output_list))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

df = pd.DataFrame([
    item
    for ent in output_list
    for item in ent[1]["items"]
])


# downloading judgments with full text content
id_pool = list(df.id)
DOWNLOAD_BASE_URL = "https://www.saos.org.pl/api/judgments/{id}"
output_list = []

print(f"Downloading full content text from {len(id_pool)} judgments...")
def thread_func(id_pull: list[int], answer_list: list):
    while len(id_pull) > 0:
        judgment_id = id_pull.pop(0)
        print(f"Dowlnoading {judgment_id} judgment, {len(id_pull)} left")
        durl = DOWNLOAD_BASE_URL.format(id=str(judgment_id))

        def thread_download(url: str):
            try:
                res = requests.get(url)
                if res.status_code == 200:
                    return res.json()
                else:
                    print(f"Error: {res.status_code}")
                    return thread_download(url)
            except Exception as e:
                print(e)
                print(f"Retyring in 1 minute")
                time.sleep(30)
                return thread_download(url)

        downloaded = thread_download(durl)
        print(f"Downloaded {judgment_id}")
        answer_list.append((judgment_id, downloaded))
        print(f"Currently downloaded {len(answer_list)}")

threads = []
for i in range(10):
    t = threading.Thread(target=thread_func, args=(id_pool, output_list))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

result = pd.DataFrame([output_list[i][1]["data"] for i in range(len(output_list))])
result.to_csv("./Data/output.csv", index=False)