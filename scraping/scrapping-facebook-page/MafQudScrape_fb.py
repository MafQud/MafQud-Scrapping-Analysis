from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time


DRIVER_PATH = 'C:/Users/yosse/chromedriver.exe'
USERNAME = "yossefalmahdey322@gmail.com"
PASSWORD = "*****"

# Our target pages from albums: https://www.facebook.com/atfalmafkoda/photos/?ref=page_internal
PAGE_MISSING = "https://www.facebook.com/media/set/?set=a.1499129867051302&type=3"  # أطفال مفقودة
# يبحثون عن أهاليهم
PAGE_FINDING = "https://www.facebook.com/media/set/?set=a.1540857199545235&type=3"
# متغيبين ومفقودين
PAGE_MISSED = "https://www.facebook.com/media/set/?set=a.1544835639147391&type=3"

# SCRAPPED_NAMES_AR = []
# SCRAPPED_GOVS_AR = []
# SCRAPPED_IMAGES_LINKS = []

# List of all Egyptian governments with nearly all the ways to write them
EGYPT_GOVS = ['الأسكندرية', 'الاسكندرية', 'الاسكندرية', 'الإسكندرية', 'اسيوط', 'أسيوط', 'اسوان', 'أسوان', 'سوهاج', 'المنيا', 'منيا', 'الجيزة', 'الجيزة', 'الجيزه', 'جيزه', 'الجيزه', 'الاسكندريه',
              'القاهرة', 'القاهره', 'قاهرة', 'قاهره', 'الدقهلية', 'الدقهليه', 'دقهلية', 'دقهليه',
              'الأقصر', 'الاقصر', 'أقصر', 'اقصر', 'كفر الشيخ', 'مرسى مطروح', 'مطروح', 'قنا', 'السويس',
              'دمياط', 'جنوب سيناء', 'البحيره', 'البحيرة', 'بحيرة', 'بحيره', 'الوادي الجديد', 'الوادى الجديد',
              'المنوفية', 'المنوفيه', 'منوفيه', 'منوفية', 'القليوبية', 'القليوبيه', 'قليوبية',
              'قليوبيه', 'الفيوم', 'فيوم', 'الغربية', 'الغربيه', 'غربية', 'غربيه', 'شمال سيناء', 'شمال سينا',
              'جنوب سينا', 'الشرقية', 'الشرقيه', 'شرقية', 'شرقيه', 'بور سعيد', 'بني سويف', 'بنى سويف',
              'البحر الأحمر', 'البحر الاحمر', 'بحر أحمر', 'بحر احمر', 'الاسماعيلية', 'الإسماعيلية', 'اسماعيلية',
              'إسماعيلية', 'الاسماعيليه', 'الإسماعيليه', 'اسماعيليه', 'إسماعيليه', 'الاسماعليه', 'اسماعليه', 'إسماعلية',
              'إسماعليه']

ARABIC_MAPPING = {
    'أ': 'a',
    'ا': 'a',
    'إ': 'e',
    'ب': 'b',
    'ت': 't',
    'ث': 'th',
    'ج': 'g',
    'ح': 'h',
    'خ': 'kh',
    'د': 'd',
    'ذ': 'th',
    'ر': 'r',
    'ز': 'z',
    'س': 's',
    'ش': 'sh',
    'ص': 's',
    'ض': 'd',
    'ط': 't',
    'ظ': 'th',
    'ع': 'a',  # or : aa
    'غ': 'gh',
    'ف': 'f',
    'ق': 'q',  # or : kh
    'ك': 'k',
    'ل': 'l',
    'م': 'm',
    'ن': 'n',
    'ه': 'h',
    'و': 'ou',
    'ي': 'i',
    'ى': 'a',
    'ؤ': 'ou',
    'ء': 'aa',
    'ئ': 'e',
    'ة': 'h',
}

GOVS_MAPPING = {
    'اسيوط': 'Assiut',
    'أسيوط': 'Assiut',
    'الجيزه': 'Giza',
    'الجيزة': 'Giza',
    'جيزة': 'Giza',
    'جيزه': 'Giza',
    'أسوان': 'Aswan',
    'اسوان': 'Aswan',
    'الاسكندرية': 'Alexandria',
    'الاسكندريه': 'Alexandria',
    'الإسكندرية': 'Alexandria',
    'الإسكندريه': 'Alexandria',
    'الأسكندرية': 'Alexandria',
    'الأسكندريه': 'Alexandria',
    'اسكندرية': 'Alexandria',
    'اسكندريه': 'Alexandria',
    'أسكندرية': 'Alexandria',
    'أسكندريه': 'Alexandria',
    'إسكندرية': 'Alexandria',
    'إسكندريه': 'Alexandria',
    'المنيا': 'Minya',
    'منيا': 'Minya',
    'القاهرة': 'Cairo',
    'القاهره': 'Cairo',
    'قاهرة': 'Cairo',
    'قاهره': 'Cairo',
    'الدقهلية': 'Dakahlia',
    'الدقهليه': 'Dakahlia',
    'دقهلية': 'Dakahlia',
    'دقهليه': 'Dakahlia',
    'سوهاج': 'Sohag',
    'الغربية': 'Gharbia',
    'الغربيه': 'Gharbia',
    'غربية': 'Gharbia',
    'غربيه': 'Gharbia',
    'البحيرة': 'Beheira',
    'البحيره': 'Beheira',
    'بحيرة': 'Beheira',
    'بحيره': 'Beheira',
    'القليوبية': 'Qualyubia',
    'القليوبيه': 'Qualyubia',
    'قليوبية': 'Qualyubia',
    'قليوبيه': 'Qualyubia',
    'الشرقية': 'Al-Sharqia',
    'الشرقيه': 'Al-Sharqia',
    'شرقية': 'Al-Sharqia',
    'شرقيه': 'Al-Sharqia',
    'المنوفية': 'Menofia',
    'المنوفيه': 'Menofia',
    'منوفية': 'Menofia',
    'منوفيه': 'Menofia',
    'بني سويف': 'Beni Suef',
    'بنى سويف': 'Beni Suef',
    'سويف': 'Beni Suef',
    'قنا': 'Qena',
    'بور سعيد': 'Port Said',
    'بور': 'Port Said',
    'سعيد': 'Port Said',
    'البحر الأحمر': 'Red Sea',
    'البحر الاحمر': 'Red Sea',
    'بحر أحمر': 'Red Sea',
    'بحر احمر': 'Red Sea',
    'البحر': 'Red Sea',
    'الأحمر': 'Red Sea',
    'الاحمر': 'Red Sea',
    'أحمر': 'Red Sea',
    'احمر': 'Red Sea',
    'دمياط': 'Damietta',
    'الفيوم': 'Fayoum',
    'فيوم': 'Fayoum',
    'كفر الشيخ': 'Kafr el-Sheikh',
    'كفر شيخ': 'Kafr el-Sheikh',
    'كفر': 'Kafr el-Sheikh',
    'شيخ': 'Kafr el-Sheikh',
    'الشيخ': 'Kafr el-Sheikh',
    'مرسى مطروح': 'Matrouh',
    'مطروح': 'Matrouh',
    'مرسى': 'Matrouh',
    'المرسى': 'Matrouh',
    'الوادي الجديد': 'New Valley',
    'الوادى الجديد': 'New Valley',
    'وادي': 'New Valley',
    'وادى': 'New Valley',
    'الوادي': 'New Valley',
    'الوادى': 'New Valley',
    'الجديد': 'New Valley',
    'جديد': 'New Valley',
    'شمال سيناء': 'North Sinai',
    'شمال سينا': 'North Sinai',
    'شمال': 'North Sinai',
    'الشمال': 'North Sinai',
    'جنوب سيناء': 'South Sinai',
    'جنوب سينا': 'South Sinai',
    'جنوب': 'South Sinai',
    'الجنوب': 'South Sinai',
    'سيناء': 'North Sinai',
    'سينا': 'North Sinai',
    'السويس': 'Suez',
    'سويس': 'Suez',
    'قناة السويس': 'Suez',
    'قناه السويس': 'Suez',
    'القناة': 'Suez',
    'القناه': 'Suez',
    'الأقصر': 'Luxor',
    'الاقصر': 'Luxor',
    'أقصر': 'Luxor',
    'اقصر': 'Luxor',
    'الاسماعيلية': 'Ismailia',
    'الاسماعيليه': 'Ismailia',
    'الإسماعيلية': 'Ismailia',
    'الإسماعيليه': 'Ismailia',
    'الأسماعيلية': 'Ismailia',
    'الأسماعيليه': 'Ismailia',
    'اسماعيلية': 'Ismailia',
    'اسماعيليه': 'Ismailia',
    'إسماعيلية': 'Ismailia',
    'إسماعيليه': 'Ismailia',
    'أسماعيلية': 'Ismailia',
    'أسماعيليه': 'Ismailia',
    'الاسماعلية': 'Ismailia',
    'الاسماعليه': 'Ismailia',
    'الإسماعلية': 'Ismailia',
    'الإسماعليه': 'Ismailia',
    'الأسماعلية': 'Ismailia',
    'الأسماعليه': 'Ismailia',
    'اسماعلية': 'Ismailia',
    'اسماعليه': 'Ismailia',
    'إسماعلية': 'Ismailia',
    'إسماعليه': 'Ismailia',
    'أسماعلية': 'Ismailia',
    'أسماعليه': 'Ismailia',
    'مفقود': 'Null'
}


# Disable chrome notifications
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)


def define_webDriver(driver_path):
    """
    Build a chrome driver to navigate to pages 

    Parameters
    ----------
    driver_path : str
        The path  of the web driver (.exe file) 

    Returns
    -------
    driver : webdriver
        the driver that wil enable to automate the navigation in web pages.

    """
    try:
        # specify the path to chromedriver.exe (download and save on your computer)
        driver = webdriver.Chrome(driver_path, chrome_options=chrome_options)

        return driver
    except:
        print("No Internet Connection")


def facebook_login(driver, username, password):
    """
    Login to your Facebook account with your username and password.

    Parameters
    ----------
    driver : webdriver
        the driver that wil enable to automate the navigation in web pages.
    username : str
        your Facebook username or email
    password : str
        your Facebook password or email (warning: keep it secret)

    Returns
    -------
    None.

    """

    try:
        # open the webpage
        driver.get("http://www.facebook.com")

        # target username (fill in the username and password imputs)
        user_name = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
        pass_word = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']")))

        # enter username and password
        user_name.clear()
        user_name.send_keys(username)
        pass_word.clear()
        pass_word.send_keys(password)

        # target the login button and click it
        button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button[type='submit']"))).click()

        print("We are logged in!")
    except:
        print("No Internet Connection")


def scroll_to_end(driver, scroll_pause_time=5):
    """
    Scroll to the far end of the pages.

    Parameters
    ----------
    driver : webdriver
        the driver that wil enable to automate the navigation in web pages.
    scroll_pause_time : float, optional
        the time between a scroll and another one. The default is 5 sec.

    Returns
    -------
    None.

    """
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(scroll_pause_time)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


# Note: Scroll on the page till the end of the page to be able to get back all photos
def scrape_page(driver, page, limit=-1, endless_scroll=False, wait_time=20):
    """
    Scrape the content of the page.
    our GOAL: images links, names in Arabic, governments.

    Parameters
    ----------
    driver : webdriver
        the driver that wil enable to automate the navigation in web pages.
    page : str
        the page url that you want to scrpe.
    limit : int, optional
        limit the scrapping process to number of retreived data. The default is -1 (no limit).
    endless_scroll : bool, optional
       scroll to the end of the page. The default is False.
    wait_time : int, optional
       the waiting time in seconds for loading the content of the page. The default is 20 sec.

    Returns
    -------
    scrapped_names_ar : list
        the scrapped names in Arabic (need some cleaning).
    scrapped_govs_ar : list
        the scrapped governments in Arabic.
    scrapped_images_links : list
        the scrapped links of the images.
    anchors : list
        the FB link of the case. 

    """

    driver.get(page)
    time.sleep(wait_time)

    if endless_scroll == True:
        # Scroll to the end of the page (doesn't work on our pages cause they have two scrollbars)
        scroll_to_end(driver, 10)

    scrapped_images_links = []       # List of links of the scrapped images
    # List of scrapped names in Arabic (need some cleaning)
    scrapped_names_ar = []
    # List of scrapped govs (if exist) in Arabic
    scrapped_govs_ar = []

    cnt = 0

    # Return all <a> tags that have href as an attribute and particullarly that have the
    # href (link) of the photo
    anchors = driver.find_elements_by_tag_name('a')
    anchors = [a.get_attribute('href') for a in anchors]
    anchors = [a for a in anchors if str(a).startswith(
        "https://www.facebook.com/atfalmafkoda/photos/a")]

    print('Found ' + str(len(anchors)) + ' links to images')

    if limit == -1:
        limit = len(anchors)

    # Looping over the links of the images saved in anchors to retrieve the photos and information
    for anchor in anchors[0:limit]:
        driver.get(anchor)  # navigate to the link
        # wait a bit (till the content of the page loads)
        time.sleep(wait_time)
        img = driver.find_elements_by_tag_name("img")

        # Goal: Find the photos that their src starts with: https://scontent.fcai21
        img_tmp = []
        for m in img:
            s = m.get_attribute("src")
            if(s.find("https://scontent.fcai21") >= 0):
                # print(s)
                img_tmp.append(s)
        # for m in img:
        #    print(m.get_attribute("src"))

        try:
            # first match is our GOAL (index = 0)
            # may change in future to img[?]
            scrapped_images_links.append(img_tmp[0])

            # For Debugging and ensure that the link is the photo link
            print("Image {} Link: {}".format(cnt+1, img_tmp[0]))
            cnt += 1
        except:
            print("Image Error")

        # Getting the <span> tag
        span = driver.find_element_by_xpath(
            "//span[@class='d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j keod5gw0 nxhoafnm aigsh9s9 d3f4x2em fe6kdd0r mau55g9w c8b282yb iv3no6db gfeo3gy3 a3bd9o3v b1v8xokw oo9gr5id']")

        # Getting the name
        post_content = span.get_attribute("innerHTML")
        missing_name = post_content[0:post_content.index("<")]
        print("Name: {}".format(missing_name))

        scrapped_names_ar.append(missing_name)

        # Getting the government (if exist)
        found = False
        for gov in EGYPT_GOVS:
            if (post_content.find(gov) >= 0):
                print("Found gov: {}".format(gov))
                scrapped_govs_ar.append(gov)
                found = True
                break
        if (found == False):
            print("Gov Not Found")
            scrapped_govs_ar.append("مفقود")

        print("==================================================================")
        print("==================================================================")

    return scrapped_names_ar, scrapped_govs_ar, scrapped_images_links, anchors


def translate_content(contents, from_language='ar', to_language='en'):
    """
    Translate the content (mostly: names, govs) list from one 
    language (mostly: 'ar') to another (mostly: 'en') using 
    translate open source library. 
    Note: has daily limited times of usage. 

    Parameters
    ----------
    contents : list
        the content list to be translated (mostly: names, govs).
    from_language : str, optional
        the language of your content. The default is 'ar'.
    to_language : str, optional
        the language you need to translate to. The default is 'en'.

    Returns
    -------
    contents_translated : list 
        list of the translated content.

    """
    from translate import Translator
    translator = Translator(from_lang=from_language, to_lang=to_language)

    contents_translated = []
    for content in contents:
        contents_translated.append(translator.translate(content))

    return contents_translated


def mapping_names_to_english(names):
    """
     Mapping the Arabic names to English using list of 
     pre-written dict according to ARABIC_MAPPING.

    Parameters
    ----------
    names : list
        list of Arabic names to be mapped.

    Returns
    -------
    names_mapped : list
        list of mapped names.

    """
    names_mapped = []
    for name in names:
        mapped_name = ""
        for c in name:
            try:
                mapped_name += ARABIC_MAPPING[c]
            except:
                mapped_name += c
        names_mapped.append(mapped_name.title())

    return names_mapped


def mapping_govs_to_english(govs):
    """
    Mapping the Arabic govs to English using list of 
    pre-written dict according to GOVS_MAPPING.

    Parameters
    ----------
    govs : list
        list of Arabic govs to be mapped.

    Returns
    -------
    govs_mapped : list
        list of mapped govs.

    """
    govs_mapped = []
    for gov in govs:
        try:
            govs_mapped.append(GOVS_MAPPING[gov])
        except:
            print("Error while mapping")
            govs_mapped.append(gov)

    return govs_mapped


def save_csv(save_path, names_en, names_ar, govs_en, govs_ar, images_links, anchors):
    """
    Save the scrapped data in a CSV file in save_path.
    Note: if it doesn't exist, it will create one. 

    Parameters
    ----------
    save_path : str
        the path you want to save your csv file (ends with the desired .csv).   
    names_en : list
        list of English names.
    names_ar : list
        list of Arabic names.
    govs_en : list
        list of English govs.
    govs_ar : list
        list of Arabic govs.
    images_links : list
        list of links of images.
    anchors : list
        list of links of the cases.

    Returns
    -------
    None.

    """
    import csv

    with open(save_path, "w") as scrapped_csv:
        wr = csv.writer(scrapped_csv)
        wr.writerow(["English_Name", "Arabic_Name", "English_Government",
                    "Arabic_Govrnment", "Image_Link", "Post_Link"])
        for i in range(len(images_links)):
            try:
                wr.writerow([names_en[i], names_ar[i], govs_en[i],
                            govs_ar[i], images_links[i], anchors[i]])
            except:
                print("Error In Row: " + str(i))

    print("The CSV file Saved Successfully in: {}".format(save_path))


def prepare_down_names(names_en):
    """
    Prepare the English names with a way to be eligable for being a name of a file 
    and a directory (replacing all spaces and special characters).

    Parameters
    ----------
    names_en : list
        list of the English names.

    Returns
    -------
    names_down : list
        list of all names eligable for naming.

    """
    names_down = []
    counter = 1
    for n in names_en:
        n = n.replace(".", "").replace(":", "").replace("?", "").replace(
            "*", "").replace("//", "").replace("<", "").replace(">", "")
        l = n.split(" ")
        # print(l)
        if(len(l) >= 3):
            names_down.append(l[0] + "_" + l[1] + "_" + l[2])
        elif(len(l) >= 2):
            names_down.append(l[0] + "_" + l[1])
        else:
            names_down.append(l[0] + str(counter))
            counter += 1

    return names_down


def download_images(images_links, names_down):
    """
    Download the scrapped images on the current directory + FB_SCRAPPED path 

    Parameters
    ----------
    images_links : list
        list of links of images.
    names_down : list
        list of eligable names for download of the English names.

    Returns
    -------
    None.

    """

    import wget
    import os

    path = os.getcwd()
    path = os.path.join(path, "FB_SCRAPPED")

    cnt = 0
    cntr = 0
    for image in images_links:
        nm = names_down[cnt]
        try:
            os.mkdir(os.path.join(path, nm))
        except:
            print("Error downloading on image {}: {}".format(cnt, image))
            nm = nm + str(cntr)
            cntr += 1
            os.mkdir(os.path.join(path, nm))

        save_as = os.path.join(os.path.join(path, nm), nm + '.jpg')
        wget.download(image, save_as)
        cnt += 1

    print("Downloaded Successfully!")


def pickle_scrapped_data(save_path, names_en, names_ar, names_down, govs_en, govs_ar, images_links, anchors):
    """
    Save the scrapped data as a list in a pickle file.

    Parameters
    ----------
    save_path : str
        the path you want to save your csv file (ends with the desired .csv).   
    names_en : list
        list of English names.
    names_ar : list
        list of Arabic names.
    names_down : list
        list of eligable English names.
    govs_en : list
        list of English govs.
    govs_ar : list
        list of Arabic govs.
    images_links : list
        list of links of images.
    anchors : list
        list of links of the cases.

    Returns
    -------
    None.

    """
    # Saving My Lists in pickles

    import pickle
    file_list = [names_en, names_ar, names_down,
                 govs_en, govs_ar, images_links, anchors]

    with open(save_path, 'wb') as f:
        pickle.dump(file_list, f)

    print("The Pickle Saved Successfully in: {}".format(save_path))
