import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup

#Global variable for centering
centerOffset = 70

#**********************************************************
# Pokemon Info
def getPokemonInfo():
    #Get name of Pokemon to search for
    pokemonName = input('Enter name of Pokémon, or press Q to quit: ')

    #Form URL with Pokemon info
    url = 'https://pokemondb.net/pokedex/' + pokemonName.lower()

    #Form request with header
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'})

    #Attempt to connect to url
    try:
        urlHandle = urllib.request.urlopen(req)
    except:
        print('Error; failed to connect. Did you spell the Pokémon\'s name correctly?')
        return

    #Set up BS object
    soup = BeautifulSoup(urlHandle.read(), 'html.parser')

    #Print details
    #Name
    print('*'*centerOffset)
    pkmnName = soup.body.main.h1.get_text()
    print(pkmnName.center(centerOffset))

    #Table of 'vital' info
    print('*'*centerOffset + '\n' + 'Basic Info'.center(centerOffset) + '\n' + '*'*centerOffset)
    vitalTable = soup.body.main.find("table", class_="vitals-table").contents[1]
    tableRows = vitalTable.find_all('tr')

    #National no, type, species, height, weight
    for row in tableRows[:5]:

        header = row.find('th').get_text().strip()
        info = row.find('td').get_text().strip()
        print('\n' + header + ':', info)


    #Abilities
    abilities = tableRows[5].find_all('a')
    print('\nAbilities:')
    for ab in abilities:
        print(ab.get_text())

    #Local Pokedex Numbers
    print('\n' + tableRows[6].find('th').get_text().strip() + ':')

    #Get each local num in an array, separated by region
    localNums = tableRows[6].find('td').get_text().strip().split(')')

    #Print Note: The last one ends up being empty, which is why it's thrown out
    for num in localNums[:len(localNums) - 1]:
        print(num + ')')



    #Evolution Chain
    print('\n' + '*'*centerOffset + '\n' + 'Evolution Chain'.center(centerOffset) + '\n' + '*'*centerOffset)

    #Handle single-stage Pokemon
    if soup.find(class_='infocard-list-evo') is None:
        print(pkmnName.capitalize(), 'does not evolve.')
    
    else:
        evoTable = soup.find(class_='infocard-list-evo').find_all(class_='infocard-lg-data')
        evoMethods = soup.find(class_='infocard-list-evo').find_all(class_='infocard-arrow')
        
        #Separate count for printing matching evolution methods
        evoMethodCnt = 0

        for idx, item in enumerate(evoTable):
            print('\nStage', idx + 1)
            print(item.get_text())
            
            #Print evolution method, except for final stage
            if(evoMethodCnt <= len(evoMethods) - 1):
                methodText = evoMethods[evoMethodCnt].get_text()
                print('\n->', methodText, '->')
                evoMethodCnt = evoMethodCnt + 1

    #Moveset
    selection = input('\nView moveset? (Y/N)')
    
    if selection.upper() == 'Y':
        print('\n' + '*'*centerOffset + '\n' + 'Moveset'.center(centerOffset) + '\n' + '*'*centerOffset + '\n')

        #Learnt by level up
        movesTable = soup.find(class_='tabset-moves-game').find(class_='data-table').tbody.find_all('tr')

        print('Learned by level up:\n')
        for move in movesTable:
            details = move.find_all('td')
            
            print('Lv:', details[0].get_text() + '     ' + 'Move:', details[1].get_text() + '     ' + 'Type:', details[2].get_text())

        #Learned by TM/TR
        movesTable = soup.find(class_='tabset-moves-game').find("h3", string='Moves learnt by TM').find_next_sibling(class_='resp-scroll').tbody.find_all('tr')
            
        print('\nLearned by TM:\n')
        for move in movesTable:
            details = move.find_all('td')
            print('TM No:', details[0].get_text() + '     ' + 'Move:', details[1].get_text() + '     ' + 'Type:', details[2].get_text())

        
        movesTable = soup.find(class_='tabset-moves-game').find("h3", string='Moves learnt by TR').find_next_sibling(class_='resp-scroll').tbody.find_all('tr')
        print('\nLearned by TR:\n')
        for move in movesTable:
            details = move.find_all('td')
            print('TR No:', details[0].get_text() + '     ' + 'Move:', details[1].get_text() + '     ' + 'Type:', details[2].get_text())

        #Egg moves
        movesTable = soup.find(class_='tabset-moves-game').find("h3", string='Egg moves').find_next_sibling(class_='resp-scroll').tbody.find_all('tr')

        print('\nEgg Moves:\n')
        for move in movesTable:
            details = move.find_all('td')
            print('Move:', details[0].get_text() + '     ' + 'Type:', details[1].get_text())


#**********************************************************
# Type Info
def getTypeInfo():
    typeName = input('Enter type: ')

    #Form URL and request
    url = 'https://pokemondb.net/type/' + typeName.lower()
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'})

    #Attempt connection
    try:
        urlHandle = urllib.request.urlopen(req)
    except:
        print('Error; failed to connect.')
        return

    #Get raw data, set up BS object
    soup = BeautifulSoup(urlHandle.read(), 'html.parser')

    #Get type effectiveness information
    typeLists = soup.find_all(class_='grid-row')[1].find_all(class_='type-fx-list')
    nameStrings = soup.find_all(class_='grid-row')[1].find_all(class_='icon-string')

    print(nameStrings)
    #Name
    print('*'*centerOffset)
    print((typeName.capitalize() + ' Type').center(centerOffset))
    print('*'*centerOffset)

    for idx, typeList in enumerate(typeLists):
        #Type category
        print('\n' + nameStrings[idx].get_text())

        #Types
        for typeName in typeList.find_all('a'):
            print(typeName.get_text())


#**********************************************************
# Ability Info
def getAbilityInfo():
    abilityName = input('Enter name of ability: ')

    #Form url and request from ability name
    url = 'https://pokemondb.net/ability/' + abilityName.lower().replace(' ', '-')
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'})

    #Connection + BS object
    try:
        soup = BeautifulSoup(urllib.request.urlopen(req).read(), 'html.parser')
    except:
        print('Error; failed to connect.')
        return

    #Info
    #Name
    #Correct capitalization for names with spaces
    if ' ' in abilityName:
        newName = ""
        cap = True
        for letter in abilityName:

            if cap is True and letter != ' ':
                newName = newName + letter.capitalize()
                cap = False
            elif letter == ' ':
                newName = newName + letter
                cap = True
            else:
                newName = newName + letter
    else:
        newName = abilityName.capitalize()

    #Print fixed name
    print('\n' + '*'*centerOffset)
    print(newName.center(centerOffset))
    print('*'*centerOffset)

    #Description
    descrip = soup.main.find(class_="grid-row").p
    
    #Handle error involving unclosed p tag
    pos = str(descrip).find('<div')
    if pos != -1:
        descrip = str(descrip)[3:pos]
    
    else:
        descrip = descrip.get_text()

    print('\nEffect:')

    #Make sure not too many words are printed on one line
    wordsPrinted = 0
    for idx, char in enumerate(descrip.split(' ')):

        print(char, end=" ")
        
        wordsPrinted = wordsPrinted + 1

        if wordsPrinted > 10 and idx < len(descrip.split(' ')) - 1:
            print('\n', end="")
            wordsPrinted = 0


    #Pokemon with ability
    pkmnList = soup.main.find_all(class_="grid-col span-md-12 span-lg-6")[1].find(class_='data-table').tbody.find_all('tr')

    print('\n\nPokémon with', newName + ':')

    wordsPrinted = 0
    for idx, pkmn in enumerate(pkmnList):
        print(pkmn.find('a').get_text(), end=" ")

        #Make sure not too many are printed on one line
        wordsPrinted = wordsPrinted + 1
        if wordsPrinted > 7 and idx < len(pkmnList) - 1:
            print('\n', end="")
            wordsPrinted = 0

    #Pokemon with hidden ability
    try: 
        hiddenPkmnList = soup.main.find_all(class_="grid-col span-md-12 span-lg-6")[1].find_all(class_="data-table")[1].tbody.find_all('tr')
    #Handle lack of hidden ability table
    except:
        return 

    print('\n\nPokémon with', newName, 'as a Hidden Ability:')
    wordsPrinted = 0
    for idx, pkmn in enumerate(hiddenPkmnList):
        print(pkmn.find('a').get_text(), end=" ")

        #Make sure not too many are printed on one line
        wordsPrinted = wordsPrinted + 1
        if wordsPrinted > 6 and idx < len(hiddenPkmnList) - 1:
            print('\n', end="")
            wordsPrinted = 0


#**********************************************************
#Move Info
def getMoveInfo():

    #Get name of move
    moveName = input('Enter name of move: ')

    #Format url and request
    url = 'https://pokemondb.net/move/' + moveName.lower().replace(' ', '-')
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'})

    #Connection + BS object
    try:
        soup = BeautifulSoup( urllib.request.urlopen(req).read(), 'html.parser' )
    except:
        print('Error; failed to connect')
    
    #Name
    #Correct capitalization for names with spaces
    if ' ' in moveName:
        newName = ""
        cap = True
        for letter in moveName:

            if cap is True and letter != ' ':
                newName = newName + letter.capitalize()
                cap = False
            elif letter == ' ':
                newName = newName + letter
                cap = True
            else:
                newName = newName + letter
    else:
        newName = moveName.capitalize()

    #Print
    print('\n' + '*'*centerOffset)
    print(newName.center(centerOffset))
    print('*'*centerOffset)

    #Move stats
    dataTable = soup.main.find(class_='vitals-table')
    dataItems = dataTable.find_all('tr')

    print('Move Stats:')
    for item in dataItems:
        header = item.find('th').get_text()
        info = item.find('td').get_text()

        print(header + ':', info)

    #Effect
    effect = soup.main.find(class_='grid-col span-md-8 span-lg-9').p.get_text()  
    print('\nEffect:')

    #Make sure not too many words are printed on one line
    wordsPrinted = 0
    for idx, char in enumerate(effect.split(' ')):

        print(char, end=" ")
        
        wordsPrinted = wordsPrinted + 1

        if wordsPrinted > 10 and idx < len(effect.split(' ')) - 1:
            print('\n', end="")
            wordsPrinted = 0


#**********************************************************
#Item Info
def getItemInfo():

    #Get name of item
    itemName = input('Enter item name: ')

    #Format url and request
    url = 'https://pokemondb.net/item/' + itemName.lower().replace(' ', '-')
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'})

    #Connection + BS object
    try:
        soup = BeautifulSoup( urllib.request.urlopen(req).read(), 'html.parser' )
    except:
        print('Error; failed to connect.')
        return 

    #Name
    #Correct capitalization for names with spaces
    if ' ' in itemName:
        newName = ""
        cap = True
        for letter in itemName:

            if cap is True and letter != ' ':
                newName = newName + letter.capitalize()
                cap = False
            elif letter == ' ':
                newName = newName + letter
                cap = True
            else:
                newName = newName + letter
    else:
        newName = itemName.capitalize()

    #Print
    print('\n' + '*'*centerOffset)
    print(newName.center(centerOffset))
    print('*'*centerOffset)

    #Effect
    effect = soup.main.find(class_='grid-col span-md-8').find('p').get_text()
    print('\nEffect:')

    #Make sure not too many words are printed on one line
    wordsPrinted = 0
    for idx, char in enumerate(effect.split(' ')):

        print(char, end=" ")
        
        wordsPrinted = wordsPrinted + 1

        if wordsPrinted > 10 and idx < len(effect.split(' ')) - 1:
            print('\n', end="")
            wordsPrinted = 0


#**********************************************************
#Natures
def getNaturesInfo():
    print('\n' + '*'*centerOffset + '\n' + 'Natures'.center(centerOffset) + '\n' + '*'*centerOffset)

    #Form request (url is static)
    req = urllib.request.Request('https://bulbapedia.bulbagarden.net/wiki/Nature', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'})
    
    #Connection + BS object
    try:
        soup = BeautifulSoup( urllib.request.urlopen(req).read(), 'html.parser')
    except:
        print('Error; failed to connect.')
        return
    
    #Get nature table
    natureTable = soup.body.find_all('table')[1].find_all('tr')
    
    for nature in natureTable:
        details = nature.find_all('td')
        name = nature.find('th')

        if len(details) > 0: 
            print('\n\nNature:', name.get_text().strip())
            print('Increases:', details[2].get_text().strip() + '     ', 'Decreases:', details[3].get_text().strip())
            print('Liked flavor:', details[4].get_text().strip() + '     ', 'Disliked flavor:', details[5].get_text().strip())


#**********************************************************
#Main Menu
while True:
    print('\n\n' + '*'*centerOffset)
    selection = input(
    '''
    Welcome to PokéInfo! Select an action:

    Pokémon (P)
    Ability (A)
    Type (T)
    Move (M)
    Natures (N)
    Item (I)
    Quit (Q)
    '''.center(centerOffset) + '\n' + '*'*centerOffset + '\n>>')


    #Options
    if selection.upper() == 'P':
        getPokemonInfo()
    elif selection.upper() == 'A':
        getAbilityInfo()
    elif selection.upper() == 'T':
        getTypeInfo()
    elif selection.upper() == 'M':
        getMoveInfo()
    elif selection.upper() == 'N':
        getNaturesInfo()
    elif selection.upper() == 'I':
        getItemInfo()
    elif selection.upper() == 'Q':
        quit()







