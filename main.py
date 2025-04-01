import os
import img2pdf
import requests
from tqdm import tqdm
from colorama import Fore
from bs4 import BeautifulSoup

class Mangalear:
    def get_info(self, url):
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")

        title = soup.find("h1", class_="entry-title").text
        elems = soup.find_all("div", class_="entry-content cf iwe-border")
        links = []
        for elem in elems:
            imgs = elem.find_all("p")
            for img in imgs:
                links.append(img.find("a").get("href"))

        return title, links

    def download(self, url):
        if not os.path.exists("mangas"):
            os.makedirs("mangas")
        imgs = self.get_info(url)[1]
        filename = 0
        for link in tqdm(imgs, desc="Downloading", unit="file"):
            try:
                res = requests.get(link, stream=True) 
                res.raise_for_status()
                filename += 1
                path = os.path.join("mangas", f"{str(filename)}.jpg")
                with open(path, "wb") as f:
                    for chunk in res.iter_content(chunk_size=8192):
                        f.write(chunk)
                tqdm.write(Fore.GREEN+"[Success] "+Fore.RESET+f"{str(filename)}.jpg")
            except Exception as e:
                tqdm.write(Fore.GREEN+"[Failed] "+Fore.RESET+f"{link}")

if __name__ == "__main__":
    mangalear = Mangalear()
    mangalear.download("")