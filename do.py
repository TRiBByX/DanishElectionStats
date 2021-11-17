import pandas as pd

def main():
    importCSV('data/valgdata.csv')








def importCSV(file_name):
    data_frame = pd.read_csv(file_name, encoding='latin-1', error_bad_lines=False)
    print(data_frame)


if __name__ == '__main__':
    main()