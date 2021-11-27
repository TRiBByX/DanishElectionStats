import collections
import os

def main():
    electionData = importCSV('data/valgdata.csv')
    # PartyDataOverTime(electionData, 'Socialdemokratiet', 'Køge')
    # DifOfPartiesByYear(electionData, ['Socialdemokratiet', 'Konservative Folkeparti'], 'Frederiksberg')
    # partyCountryWide(electionData, 'Venstre')
    partiesCountryWide(electionData, ['Venstre', 'Socialdemokratiet', 'Konservative Folkeparti', 'Socialistisk Folkeparti'])


def partiesCountryWide(electionData, parties):
    development = {}
    for party in parties:
        development[party] = {year: [list(num.values()) for name, num in kommune.items() if name == party] for year, kommune in electionData.items()}
    for party, years in development.items():
        for year, numbers in years.items():
            development[party][year] = sum([int(float(num.replace(',', '.'))) for num in numbers[0]])
    fileName = ''.join(parties)
    with open(f'data/{fileName}.csv', 'w') as fi:
        partyNames = ','.join(parties)
        fi.write(f'year,{partyNames}\n')
        years = [list(year.keys()) for party, year in development.items()][0]
        for year in years:
            fi.write(f'{year},')
            for party in parties:
                fi.write(f'{development[party][year]},')
            fi.write('\n')


def partyCountryWide(electionData, party):
    development = {year: [v for k, v in value[party].items()] for year, value in electionData.items()}
    for k, v in development.items():
        development[k] = sum([int(float(value.replace(',', '.'))) for value in v])

    with open(f'data/{party}.csv', 'w') as fi:
        fi.write(f'year,{party}\n')
        for k, v in development.items():
            fi.write(f'{k},{v}\n')


def PartyDataOverTime(electionData, party, kommune):
    development = {year: value[party][f'{kommune} Kommune'] for year, value in electionData.items()}
    with open(f'data/{party}In{kommune}.csv', 'w') as f:
        f.write('year,votes\n')
        for year, votes in development.items():
            f.write(f'{year},{votes}\n')


def DifOfPartiesByYear(electionData, parties, kommune):  # Only two parties.
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