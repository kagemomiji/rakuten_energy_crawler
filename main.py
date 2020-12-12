# coding: utf-8
from rekuten_energy_crawler.crawler import RakutenEnergyCrawler
from webhook_client.client import Client

def main():
    rec = RakutenEnergyCrawler()
    try:
        json = rec.get_json()
        print(json)
        client = Client()
        client.post_data(json)
        pass
    finally:
        rec.close()
    


if __name__ == "__main__":
    main()