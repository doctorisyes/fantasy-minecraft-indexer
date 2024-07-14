import json
import os
import matplotlib.pyplot as plt

global assumeToUseDefaultBackup
assumeToUseDefaultBackup = True

global defaultDatabase
defaultDatabase = 'now'

def getBackupFileName(backup):
    if backup != 'now':
        backup = 'update' + backup + '.json'
    elif backup == 'now':
        backup = 'database.json'
    return backup

def loadDatabse(backup):
    file = open(backup, 'r')
    database = json.load(file)
    file.close()
    return database

def loadPeople(backup):
    return loadDatabse(backup)[0]

def loadCompanies(backup):
    return loadDatabse(backup)[1]

def loadCompanyFetchList(backup):
    return loadDatabse(backup)[2]

def overwritePeople(backup, peopleDatabase):
    database = loadDatabse(backup)
    database[0] = peopleDatabase
    file = open(backup, 'w')
    json.dump(database, file)
    file.close()

def overwriteCompany(backup, companyDatabase):
    database = loadDatabse(backup)
    database[1] = companyDatabase
    file = open(backup, 'w')
    json.dump(database, file)
    file.close()

def overwriteCompanyFetchList(backup, companyFetchList):
    database = loadDatabse(backup)
    database[2] = companyFetchList
    file = open(backup, 'w')
    json.dump(database, file)
    file.close()

def askForBackup():
    if assumeToUseDefaultBackup == False:
        ask = input('What is the number of the backup you would like to use for this action?\nYou may say "now".\nEnter Here: ')
    else:
        ask = defaultDatabase
    return ask.lower()

def addPerson(backup):
    backup = getBackupFileName(backup)
    print('\nYou are now adding a new person.')
    name = input("Enter Name:\n")
    assets = int(input('Enter Assets:\n'))
    reputation = int(input('Enter Reputation:\n'))
    security = int(input('Enter Security:\n'))
    crim = int(input('Enter Criminal Record:\n'))
    influence = int(input('Enter Influence:\n'))
    success = int(input('Enter Success:\n'))
    peopleDatabase = loadPeople(backup)
    peopleDatabase[name] = [assets, reputation, security, crim, influence, success]
    overwritePeople(backup, peopleDatabase)

def addCompany(backup):
    backup = getBackupFileName(backup)
    print('\nYou are now adding a new company.')
    name = input("Enter company name:\n")
    num = int(input('How many partners form this company?\n'))
    partners = []
    for i in range(num):
        partners.append(input('Enter the name of a partner:\n'))

    companyDatabase = loadCompanies(backup)
    companyDatabase[name] = partners
    overwriteCompany(backup, companyDatabase)

    companyFetchList = loadCompanyFetchList(backup)
    companyFetchList.append(name)
    overwriteCompanyFetchList(backup, companyFetchList)

def resetCompanyDatabase(backup):
    backup = getBackupFileName(backup)
    print('\nYou are resetting the company ownership database.')
    companyDatabase = {}
    companyFetchList = []
    num1 = int(input('How many companies are there?\n'))
    for i in range(num1):
        companyName = input('What is the name of this company?\n')
        num2 = int(input('How many members are in this company?\n'))
        partners = []
        for x in range(num2):
            name = input("Enter the partner's name: ")
            partners.append(name)
        companyDatabase[companyName] = partners
        companyFetchList.append(companyName)
        overwriteCompanyFetchList(backup, companyFetchList)
    overwriteCompany(backup, companyDatabase)


def resetCompanyFetchList(backup):
    backup = getBackupFileName(backup)
    print('\nYou are resetting the company fetch list.')
    num = int(input('How many companies will be fetched?\n'))
    companies = []
    for i in range(num):
        companies.append(input('Enter the name of a company:\n'))
    overwriteCompanyFetchList(backup, companies)


def backupCurrent():
    print('\nYou are about to backup your current database.')
    update = (input('Which is this backup (number only)?\n'))
    current = loadDatabse('database.json')
    file = open('update' + update + '.json', 'w')
    json.dump(current, file)
    file.close()

def createBackupFetchList():
    start = int(input('\nWhat is the starting update? '))
    end = int(input('What is the last update: '))
    list = []
    for i in range(start, end+1):
        list.append(f"update{i}.json")
    list.append('database.json')
    return list

def fetchCategoryOfPerson(backup, category, person):
    peopleDatabase = loadPeople(backup)
    return peopleDatabase[person][category]

def fetchCategoriesOfPerson(backup, person):
    categories = []
    for i in range(6):
        categories.append(fetchCategoryOfPerson(backup, i, person))
    return categories

def fetchTotalOfPerson(backup, person):
    return sum(fetchCategoriesOfPerson(backup, person))

def fetchCategoryOfCompany(backup, category, company):
    peopleDatabse = loadPeople(backup)
    companyDatabase = loadCompanies(backup)
    partners = companyDatabase[company]
    total = 0
    for i in partners:
        total += peopleDatabse[i][category]
    return total

def fetchCategoriesOfCompany(backup, company):
    categories = []
    for i in range(6):
        categories.append(fetchCategoryOfCompany(backup, i, company))
    return categories

def fetchTotalOfCompany(backup, company):
    return sum(fetchCategoriesOfCompany(backup, company))

def editCategory(backup):
    backup = getBackupFileName(backup)
    print("""Which category do you want to change?
    1. Assets
    2. Reputation
    3. Security
    4. Criminal Record
    5. Influence
    6. Success""")
    category = int(input('\nEnter here: '))
    person = input('Who are you editing? \n')
    peopleDatabase = loadPeople(backup)
    print('The current value is: ' + str(peopleDatabase[person][category-1]))
    newValue = int(input('Enter new value: '))
    peopleDatabase[person][category-1] = newValue
    overwritePeople(backup, peopleDatabase)

def displayIndividualsResults(backup):
    backup = getBackupFileName(backup)
    person = input("Which person's categories do you want to see?\n")
    categories = fetchCategoriesOfPerson(backup, person)
    total = fetchTotalOfPerson(backup, person)
    print('\n' + person + ':')
    print(f"Assets: {categories[0]}")
    print(f"Reputation: {categories[1]}")
    print(f"Security: {categories[2]}")
    print(f"Criminal Record: {categories[3]}")
    print(f"Influence: {categories[4]}")
    print(f"Success: {categories[5]}")
    print("----------------------")
    print(f"Total is {total}MEPs")

def displayComapanyResults(backup):
    backup = getBackupFileName(backup)
    company = input("Which company's results do you want to see?\n")
    categories = fetchCategoriesOfCompany(backup, company)
    total = fetchTotalOfCompany(backup, company)
    print('\n' + company + ':')
    print(f"Assets: {categories[0]}")
    print(f"Reputation: {categories[1]}")
    print(f"Security: {categories[2]}")
    print(f"Criminal Record: {categories[3]}")
    print(f"Influence: {categories[4]}")
    print(f"Success: {categories[5]}")
    print("----------------------")
    print(f"Total is {total}MEPs")

def displayAllCompanyTotals(backup):
    backup = getBackupFileName(backup)
    fetchList = loadCompanyFetchList(backup)
    print('\n' + 'All Companies' + ':')
    for i in fetchList:
        print(f"{i}: {fetchTotalOfCompany(backup, i)}MEPs")

def displayIndividualsResultsOverTime():
    backupFetchList = createBackupFetchList()
    person = input("Which person's categories do you want to see?\n")
    for i in backupFetchList:
        categories = fetchCategoriesOfPerson(i, person)
        total = fetchTotalOfPerson(i, person)
        if i == 'database.json':
            i = 'Now'
        print('')
        print(i + ':')
        print(f"Assets: {categories[0]}")
        print(f"Reputation: {categories[1]}")
        print(f"Security: {categories[2]}")
        print(f"Criminal Record: {categories[3]}")
        print(f"Influence: {categories[4]}")
        print(f"Success: {categories[5]}")
        print("----------------------")
        print(f"Total is {total}MEPs")

def displayCompanyResultsOverTime():
    backupFetchList = createBackupFetchList()
    company = input("Which company's results do you want to see?\n")
    for i in backupFetchList:
        categories = fetchCategoriesOfCompany(i, company)
        total = fetchTotalOfCompany(i, company)
        if i == 'database.json':
            i = 'Now'
        print(f"\n{i}:")
        print(f"Assets: {categories[0]}")
        print(f"Reputation: {categories[1]}")
        print(f"Security: {categories[2]}")
        print(f"Criminal Record: {categories[3]}")
        print(f"Influence: {categories[4]}")
        print(f"Success: {categories[5]}")
        print("----------------------")
        print(f"Total is {total}MEPs")

def displayAllResultsOverTime():
    backupFetchList = createBackupFetchList()
    counter = 0
    for i in backupFetchList:
        fetchList = loadCompanyFetchList(i)
        if i == 'database.json':
            backupName = 'Now'
        elif i != 'database.json':
            backupName = i
        print('\n' + backupName + ':')
        for x in fetchList:
            print(f"{x}: {fetchTotalOfCompany(i, x)}MEPs")
        counter += 1


def addToTotalsDatabse(backup, companies):
    backup = getBackupFileName(backup)
    file = open('history.json', 'r')
    exsistingHistory = json.load(file)
    file.close()
    for i in companies:
        try:
            exsistingHistory[i].append(fetchTotalOfCompany(backup, i))
        except:
            exsistingHistory[i].append(0)
    file = open('history.json', 'w')
    json.dump(exsistingHistory, file)
    file.close()

def revertToBackup():
    print('You will need to backup the current database first!')
    check = ""
    while check != 'y' and check != 'n':
        check = input('Have you backed up yet?\n')
        check = check.lower()[0]
        if check == 'y':
            None
        elif check == 'n':
            backupCurrent()
    backupName = input('Which backup do you want to revert to (number only)?\n')
    backup = getBackupFileName(backupName)
    os.remove('database.json')
    file1 = open(backup, 'r')
    file2 = open('database.json', 'w')
    json.dump(json.load(file1), file2)

def deleteLastUpdateHistory(companies):
    file = open('history.json', 'r')
    exsistingHistory = json.load(file)
    file.close()
    for i in companies:
        exsistingHistory[i] = exsistingHistory[i][:-1]
    file = open('history.json', 'w')
    json.dump(exsistingHistory, file)
    file.close()

def plot_companies(data):
    # Initialize lists to store x, y coordinates for each company
    x_coords = []
    y_coords = []
    labels = []

    # Iterate over each company in the dictionary
    for company, values in data.items():
        # Extract x (index) and y (value) coordinates for the company
        x = []
        y = []
        for idx, value in enumerate(values):
            if value != 0:
                x.append(idx)
                y.append(value)
        # Plot the line for the company
        plt.plot(x, y, marker='o', label=company)

    # Set labels and title
    plt.xlabel('Update')
    plt.ylabel('MEPs')
    plt.title('Minecraft Economy')  # Set the title here

    plt.ylim(bottom=0)

    # Show legend outside the plot
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    # Show grid
    plt.grid(True)

    # Show the plot
    plt.tight_layout()
    plt.show()

companies = [
    "Ignis International",
    "HristoCorp",
    "Combat",
    "TTS Industries",
    "SD International",
    "Master Creators",
    "Aqua Studios",
    "MB Industries",
    "Pacific Studios"
]

try:
    file = open('database.json', 'r')
except FileNotFoundError:
    file = open('database.json', 'w')
    json.dump([{},{},[]], file)
    file.close()

try:
    file = open('history.json', 'r')
except FileNotFoundError:
    file = open('history.json', 'w')
    json.dump({}, file)
    file.close()



print('Welcome to the Minecraft Economy Software version 2.2')

print('Do you want to always load the current database?')
choice2 = input()
if choice2.lower()[0] == 'y':
    assumeToUseDefaultBackup = True
elif choice2.lower()[0] == 'n':
    assumeToUseDefaultBackup = False
    print('Do you want to choose a different default database backup?')
    defChoice = input()
    if defChoice.lower()[0] == 'y':
        print('Please note that your new default only lasts for this session')
        defaultDatabase = input('Enter ONLY the number of the new default database backup:\n')
        assumeToUseDefaultBackup = True

while True:
    print('\nYou are now back at the home menu.')
    print('You can either: 1. Make changes, or 2. view data')
    choice1 = int(input())
    if choice1 == 1:
        print("""Welcome to the Minecraft Economy Editor.
Here are your options:
        
1. Add a Person
2. Add a Company
3. Reset the Company Fetch List
4. Backup the Current Database
5. Edit a Person's Category
6. Reset Company Ownership Registry
7. Revert to a Backup
8. Remove most recent update from the graph
        
Enter you choice here: """)
        editorChoice = int(input())
        if editorChoice == 1:
            addPerson(askForBackup())
        elif editorChoice == 2:
            addCompany(askForBackup())
        elif editorChoice == 3:
            resetCompanyFetchList(askForBackup())
        elif editorChoice == 4:
            backupCurrent()
        elif editorChoice == 5:
            editCategory(askForBackup())
        elif editorChoice == 6:
            resetCompanyDatabase(askForBackup())
        elif editorChoice == 7:
            revertToBackup()
        elif editorChoice == 8:
            deleteLastUpdateHistory(companies)

    elif choice1 == 2:
        print("Do you want to see results from multiple backups?")
        multiple = input()
        if multiple.lower()[0] == 'n':
            print("""Welcome to Minecraft Economy Statistics.
Here Are Your Option:
            
1. Display an Individual's Categories and Total
2. Display a Company's Categories and Total
3. Display all Companies' totals
            
Enter your choice here: """)
            disp1choice = int(input())
            if disp1choice == 1:
                displayIndividualsResults(askForBackup())
            elif disp1choice == 2:
                displayComapanyResults(askForBackup())
            elif disp1choice == 3:
                displayAllCompanyTotals(askForBackup())

        elif multiple.lower()[0] == 'y':
            print("""Welcome to the Minecraft Economy Statistics History.
Here Are Your Option:
            
1. Display an Individual's Categories and Totals over time
2. Display a Company's Categories and Totals over time
3. Display all Companies' totals over time
4. Display ME Graph
            
Enter your choice here: """)
            disp2choice = int(input())
            if disp2choice == 1:
                displayIndividualsResultsOverTime()
            elif disp2choice == 2:
                displayCompanyResultsOverTime()
            elif disp2choice == 3:
                displayAllResultsOverTime()
            elif disp2choice == 4:
                check = input('Do you want to add the current totals to the graph again?\n')
                check = check.lower()[0]
                if check == 'y':
                    addToTotalsDatabse('now', companies)

                file = open('history.json', 'r')
                history = json.load(file)
                file.close()

                plot_companies(history)