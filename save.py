import csv

def save_to_file(jobs):
    # file = open("jobs.csv", mode="w")
    file = open("jobs.csv", mode="w", encoding="utf-8")  # when file contains something, "w" mode erase everthing in it
    writer = csv.writer(file)
    writer.writerow(["title", "company", "location", "link"])
    for job in jobs:
        writer.writerow(list(job.values())) 
    return

