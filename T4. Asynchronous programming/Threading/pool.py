from concurrent.futures import ThreadPoolExecutor

concurrency = 50
queryset = range(100)

def upload(query):
    print(query, end=', ')


with ThreadPoolExecutor(concurrency) as executor:
    for _ in executor.map(upload, queryset):
        pass