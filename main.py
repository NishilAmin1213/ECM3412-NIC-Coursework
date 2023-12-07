# pip install beautifulsoup4 lxml
from bs4 import BeautifulSoup
from ACO import *


def get_metadata(path):
    metadata = {}
    headers = ['name', 'source', 'description', 'doublePrecision', 'ignoredDigits']

    with open(path, 'r') as xml_file:
        data = xml_file.read()
        bs4_data = BeautifulSoup(data, 'xml')

        for header in headers:
            value = bs4_data.find(header).get_text()
            metadata[header] = value

    return metadata


if __name__ == "__main__":
    brazil = './data/brazil58.xml'
    burma = './data/burma14.xml'
    path = burma

    metadata = get_metadata(path)
    my_aco = ACOGraph(path, 10, 10, 0.5, 10000)
