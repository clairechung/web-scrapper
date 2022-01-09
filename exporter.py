import csv
import os.path


def save_to_file(jobs, word):
    path = "/Users/hae/Desktop/programming/web-scrapper"
    completeName = os.path.join(path, word + ".csv")
    file = open(completeName, mode="w")  # when file contains something, "w" mode erase everthing in it
    writer = csv.writer(file)
    writer.writerow(["title", "company", "location", "link"])
    for job in jobs:
        writer.writerow(list(job.values())) 
    return

