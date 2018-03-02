import csv
import json


def get_csv_rows():
    with open("../resources/plowdataNew.csv", "r", newline="") as csv_in:
        reader = csv.reader(csv_in, delimiter=",", quotechar="|")
        return [r for r in reader]


def get_row_keys(row_data):
    values = {}
    row_keys = []
    for i, item in enumerate(row_data):
        this_row = {}
        if i == 0:
            for j in range(len(list(item))):
                values[j] = item[j]
        else:
            row = list(item)
            for k, r in enumerate(row):
                this_row[values[k]] = r.strip()
        if this_row:
            row_keys.append(this_row)
    return row_keys


def create_dict(dict_in):
    trucks = {}
    for m in dict_in:
        for item in m:
            if item == "truck_name":
                if m[item] not in trucks:
                    trucks[m[item]] = [m]
                else:
                    trucks[m[item]] += [m]
    return trucks


def event_list(rows_dict):
    return [event for event in rows_dict]


def write_json_file(dict_out):
    with open("../resources/plowdata.json", "w", encoding="UTF-8") as json_file:
        json.dump(dict_out, json_file)


def main():
    csv_rows = get_csv_rows()
    rows_dict = get_row_keys(csv_rows)
    events = event_list(rows_dict)
    write_json_file(events)

if __name__ == "__main__":
    main()
