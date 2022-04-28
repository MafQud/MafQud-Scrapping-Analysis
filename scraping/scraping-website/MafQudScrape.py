import os
import json
import shutil
import requests
from time import sleep
from bs4 import BeautifulSoup
from urllib3.util import Retry
from translate import Translator
from requests.adapters import HTTPAdapter
from ..data-preprocessing.arabic_content import ARABIC_MAPPING, GOVS_MAPPING_V2


def session_request(url, stream=False):
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    response = session.get(url, stream=stream)
    return response


def extract_people_url(url):
    """
    Extract the page of each missing person on Atfal Mafkoda website based on the url. \

    Parameters
    ----------
    url : str
        the url of the page will be scrapped from Atfal Mafkoda website.
    Returns
    -------
    cnt : list
        list of the links of the content of each person on the page.
    """
    print('********   Extracting URL   ************')
    cnt = []
    response = session_request(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    for tag in soup.find_all('button', {'class': 'btn ebtn-4 ebtn-sm p-1', 'data-target': '#modal_persons_missing'}):
        cnt.append(
            {"id": int(tag['data-id']), "URL": "https://atfalmafkoda.com" + tag['data-url']})
    return cnt


def find_gov(content):
    """
    Search for the government name in the arabic text content and return the arabic and english
    government name based on the GOVS_MAPPING dict.

    Parameters
    ----------
    content : str
        the text content scapped from the website.
    Returns
    -------
    gov_arabic : str
        the arabic name of the government.
    gov_english : str
        the english name of the government.
    """
    gov_arabic = ""
    gov_english = ""
    for gov in GOVS_MAPPING_V2.keys():
        if content.find(gov) >= 0:
            gov_arabic = gov
            gov_english = GOVS_MAPPING_V2[gov]
            return gov_arabic, gov_english
    gov_arabic = 'مفقود'
    gov_english = 'Null'
    return gov_arabic, gov_english


def translate_content(content, from_language='ar', to_language='en'):
    """
    Translate the content (mostly: name, gov) string from one 
    language (mostly: 'ar') to another (mostly: 'en') using 
    translate open source library. 
    Note: the library has daily limited times of usage. 

    Parameters
    ----------
    content : str
        the content list to be translated (mostly: names, govs).
    from_language : str, optional
        the language of your content. The default is 'ar'.
    to_language : str, optional
        the language you need to translate to. The default is 'en'.
    Returns
    -------
    content_translated : str 
        string of the translated content.
    """
    translator = Translator(from_lang=from_language, to_lang=to_language)
    content_translated = translator.translate(content)

    return content_translated


def mapping_to_english(name):
    """
    Mapping the Arabic name to English using list of 
    pre-written dict according to ARABIC_MAPPING.

    Parameters
    ----------
    name : str
        list of Arabic names to be mapped.
    Returns
    -------
    names_mapped : str
        string of the mapped name.
    """

    mapped_name = ""
    for c in name:
        try:
            mapped_name += ARABIC_MAPPING[c]
        except:
            mapped_name += c

    return mapped_name.title()


def extract_people_info(base, mapping_method="mapping"):
    """
    Extract the information from the information page of the person  (id, Name_Arabic, Name_English, Government_Arabic, 
    Government_English, Missing_Date, Current_Age, images).
    Parameters
    ----------
    base : dict
        the information data about the person. 
    mapping_method : str, optional
        the method of mapping the arabic name to english name. 
        methods: mapping (default), translating. 

    Returns
    -------
    base : dict
        the dict of the data about the person after appending the data.
    """

    print('********   Extracting INFO   ************')
    response = session_request(base['URL'])
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    name_arabic = soup.find('h2', {"class": "person_name"}).text.strip()
    base['Name_Arabic'] = name_arabic
    if mapping_method == "translating":
        base['Name_English'] = translate_content(name_arabic)
    elif mapping_method == "mapping":
        base['Name_English'] = mapping_to_english(name_arabic)
    else:
        base['Name_English'] = mapping_to_english(name_arabic)
    print(base['Name_English'] + ", " + base['Name_Arabic'])
    base['Government_Arabic'], base['Government_English'] = find_gov(
        soup.find('p', {'class': 'date_loss'}).text)
    cnt = soup.find_all('h4', {"class": "date_loss"})
    base['Missing_Date'] = cnt[0].text.replace("\n", "").strip()
    base['Current_Age'] = cnt[1].text.replace("\n", "").strip()
    base['image'] = []
    for photo in soup.find_all('img', {"class": "img-fluid"}):
        if photo['alt'].strip() == base['Name_Arabic'].strip():
            base['image'].append("https://atfalmafkoda.com/" + photo['src'])

    return base


def downlad_extracted_img(base, save_path):
    """
    Download the images that are extracted from the person content. 
    Parameters
    ----------
    base : dict
         the information data about the person..
    save_path : str
        the path (directory) the data will be saved in it.
    Returns
    -------
    None.
    """
    imageURLs = base['image']
    id = base['id']
    sub = len(str(id))
    fileName = base['Name_Arabic']
    os.makedirs((f'{save_path}/{fileName}'), exist_ok=True)
    imgName = (4 - sub) * '0' + str(id) + '_'
    base['imageRef'] = imgName + '0' + '.jpg'
    base['imageRefExtra'] = []
    n = len(imageURLs)
    # Prevent any duplicated images by just downloading half of them
    if n % 2 == 0:
        n = n//2
    else:
        n = n//2 + 1
    for i in range(n):
        imageURL = imageURLs[i]
        r = session_request(imageURL, stream=True)
        r.raw.decode_content = True
        currentImagName = imgName + str(i) + '.jpg'
        print(f"Downloading {fileName} ---- {currentImagName} .....")
        base['imageRefExtra'].append(currentImagName)
        with open(f'{save_path}/{fileName}/{currentImagName}', 'wb') as f:
            shutil.copyfileobj(r.raw, f)


def extract_people_info_download_image(pageURL, save_path):
    """
    Extract and download the people information in the page. 
    Parameters
    ----------
    pageURL : str
        the page url to be extracted.
    save_path : str
        the path (directory) the data will be saved in it.
    Returns
    -------
    peapleInfo : list
        list of all the people information in the page.
    """
    cnt = extract_people_url(pageURL)
    peapleInfo = []
    for base in cnt:
        personInfo = extract_people_info(base)
        downlad_extracted_img(personInfo, save_path)
        peapleInfo.append(personInfo)
        sleep(20)
    return peapleInfo


def extract_missing_people_info_to_json(save_path="dataset", number_of_pages=-1):
    """
    Extract the information from all pages (limited bt number_of_pages) and save 
    to JSON file in the same directory. 
    Parameters
    ----------
    save_path : str, optional
        the path (directory) the data will be saved in it.
        default: the current director/Scrapped_Data.
    number_of_pages : int, optional
        number of pages you want to scrape. The default is 1.
    Returns
    -------
    None.
    """
    page = 1
    data = []
    if number_of_pages == -1:
        number_of_pages = 90
    while page <= number_of_pages:
        data = extract_people_info_download_image(
            f'https://atfalmafkoda.com/ar/seen-him?page={page}&per-page=18', f'{save_path}/images')
        write_json(data, f"{save_path}/missing_people.json")
        print("\n==>JSON file with page {} scrapped data is successfully scraped in directory".format(page))
        page += 1
        sleep(100)
        print("="*70)
    print("\n==>All images are scrapped and downloaded successfully in directory: {}".format(save_path))
    print("\n==>JSON file with all scrapped data is successfully downloaded in directory")


# function to add to JSON
def write_json(new_data, filename):
    with open(filename, 'a+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        for i in new_data:
            file_data.append(i)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    # You may need to change the SAVE_DIR to another directory
    SAVE_DIR = r"data_not_ready"
    extract_missing_people_info_to_json(SAVE_DIR)
