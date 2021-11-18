import collections

def main():
    electionData = importCSV('data/valgdata.csv')
    # PartyDataOverTime(electionData, 'Socialdemokratiet', 'Køge')
    DifOfPartiesByYear(electionData, ['Socialdemokratiet', 'Socialistisk Folkeparti'], 'Køge')


def PartyDataOverTime(electionData, party, kommune):
    development = {year: value[party][f'{kommune} Kommune'] for year, value in electionData.items()}
    with open(f'data/{party}In{kommune}.csv', 'w') as f:
        f.write('year,votes\n')
        for year, votes in development.items():
            f.write(f'{year},{votes}\n')


def DifOfPartiesByYear(electionData, parties, kommune): # Only two parties.
    if len(parties) > 2:
        raise Exception('Party list too long')
    development = {year: [value[parties[0]][f'{kommune} Kommune'], value[parties[1]][f'{kommune} Kommune']] for year, value in electionData.items()}
    with open(f'data/{parties[0]}vs{parties[1]}.csv', 'w') as fi:
        fi.write(f'year,{parties[0]} votes,{parties[1]} votes\n')
        for year, votes in development.items():
            fi.write(f'{year},{votes[0]},{votes[1]}\n')

def importKommuneNr():
    with open('kommunenr.csv') as komcsv:
        data = komcsv.readlines()
        kommuner = {kommune.strip().split(',')[0]: kommune.strip().split(',')[1] for kommune in data}
        return kommuner


def importCSV(file_name):
    with open('data/valgdata.csv', 'r', encoding='latin-1') as csv:
        banner = csv.readline().replace('"', '').strip().split(';')
        fv = list(set([year[2:6] for year in banner if 'FV' in year]))
        _data = csv.readlines()
        _data = [dat.replace('"', '').strip().split(';') for dat in _data]
        data = {}
        kommuner = importKommuneNr()
        for x in range(0, len(fv)):
            data[fv[x]] = {banner[y].replace(f'FV{fv[x]} - ', ''): {kommuner[item[1]] + ' Kommune': item[y] for item in _data} 
                           for y in range(2, len(banner)) 
                           if fv[x] in banner[y]}
    data = collections.OrderedDict(sorted(data.items()))
    return data
if __name__ == '__main__':
    main()