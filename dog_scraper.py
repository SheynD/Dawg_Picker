"""
Scrape dog stats/info from dogtime.com/dog-breeds
"""
import requests
from bs4 import BeautifulSoup

if __name__ == "__main__":

	with open("characteristic_stats.csv", "w+") as out:
		out.write("breed,characteristic,rating\n")

		url = "http://www.dogtime.com/dog-breeds"
		r = requests.get(url)
		page = BeautifulSoup(r.text, "lxml")

		main_box = page.find("div", {"class": "group with-image-mobile-only"})
		all_breeds = main_box.findAll("div", recursive=False) # recursive=False will only find matching tags on the top level

		for letter_group in all_breeds:
			breeds = letter_group.findAll("div", recursive=False)

			for breed in breeds:
				breed_url = breed.find("a").get("href")
				r = requests.get(breed_url)
				page = BeautifulSoup(r.text, "lxml")

				breed = breed_url.split("/")[-1] # http://dogtime.com/dog-breeds/saint-bernard
				main_box = page.find("div", {"class": "inside-box"})
				characteristics = main_box.findAll("div", recursive=False)

				for characteristic in characteristics:
					name = characteristic.find("span", {"class": "characteristic item-trigger-title"}).get_text()
					stars = characteristic.select("span[class*='star star-']")[0]
					rating = stars.get("class")[1].split("-")[1]

					out.write("%s,%s,%i\n" % (breed.strip(), name.strip(), int(rating)))
				
				print("Pulling data for %s... " % breed.strip())
