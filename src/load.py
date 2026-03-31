# Save to CSV / insert into PostgreSQL

import os
import csv

def save_to_csv(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['title'])

        for row in data:
            writer.writerow([row["title"]])