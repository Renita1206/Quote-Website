import os
import pymongo
from pymongo import MongoClient
import certifi
import random

certificate = certifi.where()

password = os.environ["MONGO_PASSWORD"]
url = "mongodb+srv://renitaKurian:"+ password +"@datacluster.ylfhthx.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(url, tlsCAFile = certificate)
#print(client.server_info())

mydb = client.Quotes # to access database quotes
collection = mydb.Random

noQ = 0
objects = collection.find()
for i in objects:
    noQ+=1


def printAll():
    objects = collection.find()

    for i in objects:
        print("Quote: ",i['quote'])
        if i["lang"]!="English":
            print("Translation: ",i['translation'])
            print("Language: ",i['lang'])
        print("Author: ",i['author'])
        print()

def randomQuote():
    objects = collection.find()
    n = random.randint(0, noQ-1)
    q = objects[n]
    print("Quote: ",q['quote'])
    if q["lang"]!="English":
        print("Translation: ",q['translation'])
        print("Language: ",q['lang'])
    print("Author: ",q['author'])
    print()

def addQuote():
    quote = input("Enter Quote: ")
    lang = input("Enter language: ")
    if lang!="English":
        translation = input("Enter translation of quote in English: ")
    else:
        translation = "-"
    auth = input("Enter name of author: ")

    qd = {"quote":quote, "lang": lang, "author":auth, "translation": translation}

    x = collection.insert_one(qd)
    print("Object id: ", x.inserted_id)
    print()

def searchQuote():
    searchQuery = ""
    inp = input("Would you like to search by language or author? ")
    if inp=="author":
        searchQuery = "author"
        auth = input("Enter name of author: ")
        result = collection.find({searchQuery:auth})
        numberOfResults = 0
        for i in result:
            numberOfResults+=1
            print("Quote: ",i['quote'])
            if i["lang"]!="English":
                print("Translation: ",i['translation'])
                print("Language: ",i['lang'])
            print()
        print(numberOfResults," quotes match the search query.")
        
    elif inp=="language":
        searchQuery = "lang"
        lang = input("Enter the language: ")
        result = collection.find({searchQuery:lang})
        numberOfResults = 0
        for i in result:
            numberOfResults+=1
            print("Quote: ",i['quote'])
            if i["lang"]!="English":
                print("Translation: ",i['translation'])
            print("Author: ",i['author'])
            print()
        print(numberOfResults," quotes match the search query.")
    else:
        print("Invalid input")
    print()

def main():
    while(1):
        print("1. Generate Random Quote")
        print("2. Print all quotes")
        print("3. Add Quote to database")
        print("4. Search for Quotes")
        print("5. Exit")
        inp = int(input("Enter your choice (1-5): "))
        if inp==1:
            randomQuote()
        elif inp==2:
            printAll()
        elif inp==3:
            addQuote()
        elif inp==4:
            searchQuote()
        elif inp==5:
            exit()
        else:
            print("Invalid Input")

main()
