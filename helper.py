import sqlite3
import os
# get n number of most commonly visited websites from history


def get_list(n):
    # get history from chrome
    history_db = os.path.expanduser('~') + r"/Library/Application Support/Google/Chrome/Default/history"
    c = sqlite3.connect(history_db)
    cursor = c.cursor()
    select_statement = "SELECT urls.url, urls.visit_count FROM urls, visits WHERE urls.id = visits.url;"
    cursor.execute(select_statement)
    results = cursor.fetchall()  # tuple
    # sort by visit count
    results_sorted = sorted(results, key=lambda tup: tup[1], reverse=True)
    # get top n
    top_n = results_sorted[:n]
    # get list of websites
    websites = []
    for i in top_n:
        websites.append(i[0])
    return websites


print(get_list(1000))
