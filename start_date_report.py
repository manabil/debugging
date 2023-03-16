#!/usr/bin/env python3

import csv
import datetime
import requests


FILE_URL = "https://storage.googleapis.com/gwg-content/gic215/employees-with-date.csv"

def get_start_date() -> datetime.datetime:
    """Interactively get the start date to query for."""

    print()
    print('Getting the first start date to query for.')
    print()
    print('The date must be greater than Jan 1st, 2018')
    year = int(input('Enter a value for the year: '))
    month = int(input('Enter a value for the month: '))
    day = int(input('Enter a value for the day: '))
    print()

    return datetime.datetime(year, month, day)

def get_file_lines(url: str) -> list:
    """Returns the lines contained in the file at the given URL"""

    # Download the file over the internet
    response = requests.get(url, stream=True)
    lines = []

    for line in response.iter_lines():
        lines.append(line.decode("UTF-8"))
    return lines

def get_ordered_data() -> dict:
    data = get_file_lines(FILE_URL)
    reader = csv.reader(data[1:])
    data_dict = {}
    
    for row in reader:
        if row[3] not in data_dict:
            data_dict.update({row[3]: [f"{row[0]} {row[1]}"]})
        else:
            data_dict[row[3]].append(f"{row[0]} {row[1]}")
           
    data_dict = sort_dict(data_dict)
    return data_dict

def sort_dict(data: dict) -> dict:
    myKeys = list(data.keys())
    myKeys.sort()
    sorted_dict = {i: data[i] for i in myKeys}
    return sorted_dict

def get_employee(datas: dict, start_date: datetime.datetime) -> None:
    str_date = start_date.strftime("%Y-%m-%d")
    for data in datas.items():
        if data[0] >= str_date:
            print(f"Started on {data[0]}: {data[1]}")

def main():
    start_date = get_start_date()
    data = get_ordered_data()
    get_employee(data, start_date)

if __name__ == "__main__":
    main()
