import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time
import random
import datetime
import csv
import os
from decimal import Decimal
from boroughList import boroughList
from os import listdir
from os.path import isfile, join

class main():

    def scrape(self, borough, name):

        allApartmentLinks = []
        allDescription = []
        allPrice = []

        index = 0
        key = [key for key, value in boroughList.items() if value == borough]
        
        for pages in range(41):

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
            }

            if index == 0:
                rightmove = f"https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%{borough}&sortType=6&propertyTypes=&includeSSTC=false&mustHave=&dontShow=&furnishTypes=&keywords="

            elif index != 0:
                rightmove = f"https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%{borough}&sortType=6&index={index}&propertyTypes=&includeSSTC=false&mustHave=&dontShow=&furnishTypes=&keywords="

            res = requests.get(rightmove, headers=headers)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, "html.parser")

            # This gets the list of apartments
            apartments = soup.find_all("div", class_="l-searchResult is-list")

            # This gets the number of listings
            numListings = soup.find(
                "span", {"class": "searchHeader-resultCount"}
            )
            numListings = numListings.get_text()
            numListings = int(numListings.replace(",", ""))

            for i in range(len(apartments)):

                # Tracks which apartment we are on in the page
                firstVar = apartments[i]

                # Append link
                apartmentInfo = firstVar.find("a", class_="propertyCard-link")
                link = "https://www.rightmove.co.uk" + apartmentInfo.attrs["href"]
                allApartmentLinks.append(link)

                # Append description
                description = (
                    apartmentInfo.find("h2", class_="propertyCard-title")
                    .get_text()
                    .strip()
                )
                allDescription.append(description)

                # Append price
                price = (
                    firstVar.find("div", class_="propertyCard-priceValue")
                    .get_text()
                    .strip()
                )
                allPrice.append(price)

            index = index + 24

            if index >= numListings:
                break
        
        data = {
            "Links": allApartmentLinks,
            "Description": allDescription,
            "Price": allPrice,
        }
        df = pd.DataFrame.from_dict(data)
        df.to_csv(fr"{name}.csv", encoding="utf-8", header="true", index=False)
            
            
    def all(self, borough, name):
        self.clearConsole()
        
        fileList = [f for f in listdir(os.getcwd()) if isfile(join(os.getcwd(), f))]

        if f"{name}.csv" not in fileList:
            print("Loading...")
            self.scrape(borough, name)
            self.clearConsole()

    def links(self, borough, name):
        self.clearConsole()
        
        fileList = [f for f in listdir(os.getcwd()) if isfile(join(os.getcwd(), f))]

        if f"{name}.csv" not in fileList:
            print("Loading...")
            self.scrape(borough, name)
            self.clearConsole()

    def description(self, borough, name):
        self.clearConsole()
        
        fileList = [f for f in listdir(os.getcwd()) if isfile(join(os.getcwd(), f))]

        if f"{name}.csv" not in fileList:
            print("Loading...")
            self.scrape(borough, name)
            self.clearConsole()

    def values(self, borough, name):

        def extract(task, name):
                
            with open(f"{name}.csv", newline='') as csvfile:
                data = csv.DictReader(csvfile)
                    
                priceList = []
                maxLength = 0
                numList = []
                
                for row in data:
                    priceList.append(row["Price"])
                    numList.append(Decimal(re.sub(r'[^\d.]', '', row["Price"])))
                    if len(row["Price"]) > maxLength:
                        maxLength = len(row["Price"])
                        
                    
                if task == "list":
                    return [
                        priceList,
                        maxLength
                    ]
                    
                elif task == "top10":
                    return [
                        priceList[10:],
                        priceList[:10],
                        maxLength,
                    ]
                    
                elif task == "overview":
                    total = sum(numList)
                    length = len(numList)
                    
                    return {
                        "high": priceList[0],
                        "low": priceList[-1],
                        "mean": total / length,
                        "total": total,
                        "amount": length,
                    }
        
        fileList = [f for f in listdir(os.getcwd()) if isfile(join(os.getcwd(), f))]
        
        if f"{name}.csv" not in fileList:
            print("Loading...")
            self.scrape(borough, name)
            self.clearConsole()

        print(f"\nWe have succedfully scraped all the information about the property values for the London borough of {name}.\nPlease choose from some of the options below regarding outputing this data:")

        iterationsNum = 0
        while True:
            if iterationsNum == 0:
                print("\nA: List the values of all of the houses\nB: List the 10 highest and lowest house prices\nC: Give an overview of the data collected\nD: Exit")
            else:
                print("\n\nA: List the values of all of the houses\nB: List the 10 highest and lowest house prices\nC: Give an overview of the data collected\nD: Exit")
            choices = ["A","B","C","D"]
            choice = input("\nEnter choice: ").upper()
    
            while choice not in choices:
                choice = input("\nInvalid choice, try again.\nEnter Choice: ").upper()
    
            if choice == "A":
                result = extract("list", name)

                for n, i in enumerate(result[0]):
                    if n % 4 == 0:
                        print("")
                    print(i, end=" "*((result[1]+8)-len(i)))           
                
            elif choice == "B":
                result = extract("top10", name)
                print(result)
                
            elif choice == "C":
                result = extract("overview", name)
                print(result)
                
            else:
                break
            iterationsNum += 1
        
    
    def options(self, arr):
        self.clearConsole()

        print(f"You have selected the London borough of {arr[0]}.\n")
        print("Please choose from one of these options below:\n")
        print("A: Scrape information about the prices of the properties\nB: Scrape information about the types of properties\nC: Scrape all the links to every property\nD: All of the above")

        choices = ["A","B","C","D"]
        choice = input("\nEnter choice: ").upper()

        while choice not in choices:
            choice = input("\nInvalid choice, try again.\nEnter Choice: ").upper()

        if choice == "A":
            self.values(arr[1], arr[0])
        elif choice == "B":
            self.description(arr[1], arr[0])
        elif choice == "C":
            self.links(arr[1], arr[0])
        elif choice == "D":
            self.all(arr[1], arr[0])
        
    def clearConsole(self):
        command = "clear"
        if os.name in ("nt", "dos"):
            command = "cls"
        os.system(command)

    def __init__(self):
        self.clearConsole()
        
        print("Welcome to the Rightmove Property Value Surveyor!\n")
        print("Start by selecting a London borough to scrape from:\n")

        boroughChoices = {}

        for n, i in enumerate(boroughList):
            print((f"{n+1}: {i}"))
            boroughChoices[n+1] = [i, boroughList[i]]

        while True:
            try:
                choice = int(input("\nEnter the boroughs corresponding number: "))
                break
            except:
                print("\nTry again.")
        while choice not in boroughChoices:
            choice = int(input("\nTry again.\nEnter the boroughs corresponding number: "))

        self.options(boroughChoices[choice])
        
if __name__ == "__main__":
    main()