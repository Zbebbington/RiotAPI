import requests
import pandas as pd

apiKey = 'RGAPI-23110ebc-c512-42b7-9d3a-036b45a465ab'
def requestSummonerData(summonerName):
    URL = 'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + summonerName + '?api_key=' + apiKey
    response = requests.get(URL)
    return response.json()

def requestAllMasteries(accountID):
    URL = 'https://na1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/' + accountID + '?api_key=' + apiKey
    response = requests.get(URL)
    return response.json()

def championData(patch):
    URL = 'http://ddragon.leagueoflegends.com/cdn/' + patch + '/data/en_US/champion.json'
    response = requests.get(URL)
    return response.json()

def main():
    testResponse = requestSummonerData('Fractions')
    #print(testResponse)
    testResponse2 = requestAllMasteries(testResponse['id'])
    #print(testResponse2)
    champInfo = championData('9.6.1')['data']
    #print(champInfo)

    idMaps = {}
    for champion in champInfo:
        idMaps[champInfo[champion]['key']] = champInfo[champion]['name']
    #print(idMaps)

    diff = []
    for champion in champInfo:
        diff.append((champInfo[champion]['name'], champInfo[champion]['info']['difficulty']))

    dframe = pd.DataFrame(diff)
    dframe.columns = ['Name', 'Difficulty']

    frame = pd.DataFrame.from_dict(testResponse2)
    #print(frame.columns)
    #print(frame)
    masteryFrame = frame.iloc[:, :3]
    #print(masteryFrame.columns)

    masteryFrame['championId'] = masteryFrame['championId'].apply(lambda x: idMaps[str(x)])
    masteryFrame.columns = ['Name', 'Level', 'Points']
    masteryFrame = pd.merge(left=masteryFrame, right=dframe, on='Name')
    masteryFrame.set_index('Name', inplace = True)
    #print(masteryFrame)

    masteryFrame.to_excel(r'D:\Documents\Programming\Python\Projects\Riot\masteryData.xlsx')
if __name__ == '__main__':
    main()
