# Sorts a csv by timestamp. To run, use a command line argument with the filename you are sorting. Ex: "csvsort.py energycache.csv"

import csv
import argparse

def main():
    parser = argparse.ArgumentParser(description="Script to receive a single string argument")
    parser.add_argument("input_string", type=str, help="A string argument")
    
    args = parser.parse_args()
    
    input_file = str(args.input_string)

    with open(input_file, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)

    # Sort the data by the first element of each row
    sorted_data = sorted(data, key=lambda x: int(x[0]))

    # Write the sorted data to a new CSV file
    with open(input_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(sorted_data)




    #Check for missing time values
    with open(input_file,'r') as file:
        reader = csv.reader(file)
        prevrow = 1528948800  #first val in hourlyenergy csv file
        for row in reader:
            if (int(row[0]) - int(prevrow)) > 86400:
                print(f"Missing time value after: {prevrow}")
                prevrow = row[0]



if __name__ == "__main__":
    main()