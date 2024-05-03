import logging, json, requests, socket
def main():
    # api refs: http://www.bom.gov.au/catalogue/data-feeds.shtml
    data= requests.get('http://reg.bom.gov.au/fwo/IDV60901/IDV60901.95936.json').json()

    print(data)
    return 'OK'


main()