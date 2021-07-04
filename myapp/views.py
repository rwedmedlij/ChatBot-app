from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
import urllib
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC, expected_conditions
from time import sleep
from urllib.request import urlopen
import bs4 as bs
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json


def index(request):
    return render(request, 'myapp/index.html')


def newClick(request):

    phone = ""
    itsnadlan = True
    website_driver = 'https://www.nadlan.com/properties?type=1'
    # website_driver = 'https://www.madlan.co.il/'
    # website_driver = 'https://www.homely-mls.co.il/'

    # website_driver = 'https://www.onmap.co.il/homes/buy'
    withOptions = True

    if(website_driver.__eq__('https://www.nadlan.com/properties?type=1')):
        itsnadlan = True
    else:
        itsnadlan = False
        withOptions = False
    print("Running :" + website_driver)
    nadlan_found = False
    onmap_found = False
    # withOptions = True
    withdisplay = True

    ##################-----------INIT-----------#############
    isParking = False
    isBalcony = True
    isElevator = False

    isShelter = False
    isGarbage_chute = False
    isAccessible = False
    iswareHouse = False
    isGym = False
    isStroller_room = False
    Area_Website = 'תל אביב והמרכז'
    # City_Website = 'קריית ביאליק'
    City_Website = 'חריש'
    # City_Website = 'אשדוד'

    FromNumRooms_Website = '1'
    ToNumRoom_Website = '10'
    FromPrice_Website = '400'
    ToPrice_Website = '3800000'
    From_Floor_Website = '1'
    To_Floor_Website = '6'
    # INIT DRIVER FIREFOX
    options = Options()
    if(withdisplay == False):
        options.add_argument('--headless')
        driver = webdriver.Firefox(options=options)
    else:
        driver = webdriver.Firefox()
    driver.get(website_driver)

    # FILE FOR -> ALL LINK AND INFO (FOR ROOMS)

    def check_exists_by_xpath(xpath):
        try:
            driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True

    file_info_links = open("linksinfo.txt", "w", encoding="utf-8")
    file_house_nadlan = open("nadlan_house.txt", "w+", encoding="utf-8")
    file_house_onmap = open("onMap_house.txt", "w+", encoding="utf-8")
    file_nadlan = open("nadlan.txt", "w+", encoding="utf-8")

    file = open("ratehouse.txt", "w+", encoding="utf-8")

    # END INIT###################33

    # NADLAN  ################333333
    Area_Website_nadlan = Area_Website.replace(" ", "_")

    if(int(ToNumRoom_Website) > 15 or int(FromNumRooms_Website) > 15):
        print(
            "SYSTEM >>> attention [(max or min) Number of [ROOMS] is too large]")
    if(int(To_Floor_Website) > 99 or int(From_Floor_Website) > 99):
        print(
            "SYSTEM >>> attention [(max or min) Number of [FLOORS] is too large]")

    if(withOptions):
        # remove read only Area
        driver.execute_script(
            'document.getElementsByName("area")[0].removeAttribute("readonly")')
    # remove read only city
        driver.execute_script(
            'document.getElementsByName("city")[0].removeAttribute("readonly")')  # city
    # value of area
        driver.execute_script(
            'document.getElementsByName("area")[0].setAttribute("data-id","'+Area_Website_nadlan+'") ')  # area
    # value of city
        Area_input = driver.find_element(
            By.XPATH, '//*[@id="property-search"]/div/div[2]/div/input')
        Area_input.clear()
        Area_input.send_keys(Area_Website_nadlan)
        driver.execute_script(
            'document.getElementsByName("city")[0].setAttribute("data-id","'+City_Website+'")')
    # value of price
    # driver.execute_script('document.getElementsByName("price-from")[0].setAttribute("value","400") ')
    # value of price
    # driver.execute_script('document.getElementsByName("price-to")[0].setAttribute("value","1000000") ')
    # remove read only Rooms
        driver.execute_script(
            'document.getElementsByName("rooms")[0].removeAttribute("readonly")')
    # value of rooms
        driver.execute_script(
            'document.getElementsByName("rooms")[0].setAttribute("data-id","'+FromNumRooms_Website+'")')  # area

        city_input = driver.find_element(
            By.XPATH, '/html/body/div[6]/div/div[4]/div/div[3]/div/input')
        city_input.clear()
        city_input.send_keys(City_Website)

        FromPrice_input = driver.find_element(
            By.XPATH, '/html/body/div[6]/div/div[4]/div/div[4]/input')
        FromPrice_input.send_keys(FromPrice_Website)

        ToPrice_input = driver.find_element(
            By.XPATH, '/html/body/div[6]/div/div[4]/div/div[5]/input')
        ToPrice_input.send_keys(ToPrice_Website)

        if isParking:
            driver.find_element(
                By.XPATH, '/html/body/div[6]/div/div[4]/div/div[7]/div[1]/label').click()

        if iswareHouse:
            driver.find_element(
                By.XPATH, '/html/body/div[6]/div/div[4]/div/div[7]/div[2]/label').click()

        Rooms_input = driver.find_element(
            By.XPATH, '/html/body/div[6]/div/div[4]/div/div[6]/div/input')
        Rooms_input.clear()
        Rooms_input.send_keys(FromPrice_Website)

        searchButton_ForClick = driver.find_element_by_link_text('חפש')
        searchButton_ForClick.click()

    url_scarpy = driver.current_url
    if(itsnadlan):
        source = urllib.request.urlopen(url_scarpy).read()
        soup = bs.BeautifulSoup(source, 'lxml')
        table = soup.find('table')
        table_rows = table.find_all('tr')

        count_rows = 1
        number_rows = -1
        for tr in table_rows:
            td = tr.find_all('td')
            row = [i.text for i in td]
            str1 = ""
            for ele in row:
                str1 += ele
            scrap_city = ""
            if len(row) > 0:
                scrap_city = row[1].strip()
                scrap_price = row[2].strip()
                scrap_floor = row[3].strip()
                scrap_rooms = row[4].strip()
                scrap_adress = row[5].strip()
                scrap_asset = row[6].strip()
                scrap_date = row[7].strip()
                scrap_advertise = row[8].strip()
                file_house_nadlan.write(str(count_rows)+":"+str(scrap_city)+":"+str(scrap_price)+":"+str(scrap_floor)
                                        + ":" + str(scrap_rooms) + ":" + str(scrap_adress) + ":" + str(scrap_asset) + ":" + str(scrap_date) + ":" + str(scrap_advertise)+"\n")

                # print(driver.current_url)
                # print(elemente.text)
                # driver.execute_script("window.history.go(-1)")
                # print(driver.current_url)
                # sleep(3)
                # driver.execute_script("window.scrollTo(2,document.body.scrollHeight)")
            # driver.forward()
                count_rows = count_rows+1
                number_rows = number_rows+1
            # driver.close()  # Switch back to the first tab with URL A
            # driver.switch_to.window(driver.window_handles[0])

        for c in range(1, number_rows+1):
            elemente = driver.find_element(
                By.XPATH, '/html/body/div[9]/div/div/div/div/div[1]/div[1]/div/div/div/div/table/tbody/tr['+str(c)+']')
            file_info_links.writelines("https://www.nadlan.com/property/" + elemente.get_attribute(
                "data-property-id") + "=" + elemente.get_attribute("data-property-id")+"\n")

    file_info_links.close()

    file_house_nadlan.close()
    c = 1
    f10 = open("linksinfo.txt", "r+", encoding="utf-8")
    count = 1
    for line in f10:
        splitline = line.split("=")
        link = splitline[0]
        driver = webdriver.Firefox()
        driver.get(link)
        time.sleep(2)
        floorN = "unknown"
        sizeN = "unknown"
        roomsN = "unknown"
        cityN = "unknown"
        addressN = "unknown"
        priceN = "unknown"
        for i in range(1, 30):
            # 3time.sleep(2)
            try:
                namespan = driver.find_element(
                    By.XPATH, '/html/body/div[8]/div/div/ul/li['+str(i)+']/span[1]')
                name = str(namespan.get_attribute("innerHTML")).strip()
            except:
                break

            if(name.__eq__("קומה:")):
                try:
                    spanflor = driver.find_element(
                        By.XPATH, '/html/body/div[8]/div/div/ul/li['+str(i)+']/span[2]')
                    floorN = str(spanflor.get_attribute("innerHTML")).strip()
                except:
                    floorN = "unknown"

            if (name.__eq__("שטח בנוי:")):
                try:
                    spansize = driver.find_element(
                        By.XPATH, '/html/body/div[8]/div/div/ul/li['+str(i)+']/span[2]')
                    sizeN = str(spansize.get_attribute("innerHTML")).strip()
                except:
                    sizeN = "unknown"

            if (name.__eq__("מס' חדרים:")):
                try:
                    spanrooms = driver.find_element(
                        By.XPATH, '/html/body/div[8]/div/div/ul/li['+str(i)+']/span[2]')
                    roomsN = str(spanrooms.get_attribute("innerHTML")).strip()
                except:
                    roomsN = "unknown"

            if (name.__eq__("עיר\ישוב:")):
                try:
                    spancity = driver.find_element(
                        By.XPATH, '/html/body/div[8]/div/div/ul/li['+str(i)+']/span[2]')
                    cityN = str(spancity.get_attribute("innerHTML")).strip()
                except:
                    cityN = "unknown"

            if (name.__eq__("כתובת:")):
                try:
                    spanaddress = driver.find_element(
                        By.XPATH, '/html/body/div[8]/div/div/ul/li['+str(i)+']/span[2]')
                    addressN = str(
                        spanaddress.get_attribute("innerHTML")).strip()
                except:
                    addressN = "unknown"

            if (name.__eq__("מחיר:")):
                try:
                    spanprice = driver.find_element(
                        By.XPATH, '/html/body/div[8]/div/div/ul/li['+str(i)+']/span[2]')
                    priceN = str(spanprice.get_attribute("innerHTML")).strip()
                except:
                    priceN = "unknown"

            try:
                phone = driver.find_element(
                    By.XPATH, '/html/body/div[7]/div[2]/div/div[2]/div[1]/div[2]')
            except:
                phone = "unknown"

        file_nadlan.write(str(c) + "-----" + str(priceN) + "-----" + str(cityN) + "-----" + str(floorN) + "-----" + str(
            roomsN) + "-----" + str(addressN) + "-----" + str(phone).strip() + "-----" + str(sizeN) + "-----" + str(link))

        for info in range(1, 30):
            try:
                informationspan = driver.find_element(
                    By.XPATH, '/html/body/div[8]/div/div/div[4]/ul/li['+str(info)+']/span[2]')
                information = str(
                    informationspan.get_attribute("innerHTML")).strip()
                file_nadlan.write("-----" + str(information))
            except:
                break
        c = c+1
        file_nadlan.write("\n")
    f10.close()
    file_nadlan.close()

    # homely-mls. ############################33333
    ## INIIT#####"#

    homelymls_found = True
    isAccessible = False
    isElevator = True
    isSafe = False

    # 333
    website_driver = 'https://www.homely-mls.co.il/'
    driver.get(website_driver)
    time.sleep(5)
    area_homely = driver.find_element(By.XPATH, '//*[@id="searchByPlace"]')
    area_homely.clear()
    area_homely.send_keys(City_Website)

    time.sleep(2)
    element1 = WebDriverWait(driver, 20).until(expected_conditions.presence_of_element_located(
        (By.XPATH, "/html/body/div[5]/div")))
    suggestion_option_homely = driver.find_element(
        By.XPATH, '/html/body/div[5]/div')
    suggestion_option_homely.click()

    # open more options
    driver.find_element(
        By.XPATH, '/html/body/div[4]/section[1]/div[1]/div/div/label/i').click()

    # check if we have result of this city

    text_result = driver.find_element(By.XPATH, '//*[@id="totalText"]')
    # no results
    if(text_result.text == "לא נמצאו דירות למכירה"):
        homelymls_found = False
    else:
        # /html/body/div[4]/section[1]/div[2]/div/form/div[2]/ul/li[1]/ul/li[1]/div[1]/span
        # yes results :
        homelymls_found = True
        if(isParking):
            driver.find_element(
                By.XPATH, '/html/body/div[4]/section[1]/div[2]/div/form/div[2]/ul/li[2]/ul/li[1]/label').click()
        if(isElevator):
            driver.find_element(
                By.XPATH, '/html/body/div[4]/section[1]/div[2]/div/form/div[2]/ul/li[2]/ul/li[3]/label').click()
        if(isAccessible):
            driver.find_element(
                By.XPATH, '/html/body/div[4]/section[1]/div[2]/div/form/div[2]/ul/li[2]/ul/li[2]/label').click()
        if(isSafe):
            driver.find_element(
                By.XPATH, '/html/body/div[4]/section[1]/div[2]/div/form/div[2]/ul/li[2]/ul/li[4]/label').click()

        driver.find_element(
            By.XPATH, '/html/body/div[4]/section[1]/div[2]/div/form/div[2]/ul/li[1]/ul/li[1]/div[1]').click()
        driver.find_element(
            By.XPATH, '/html/body/div[4]/section[1]/div[2]/div/form/div[2]/ul/li[1]/ul/li[1]/div[1]/ul/li['+str(int(From_Floor_Website)+1)+']').click()

        driver.find_element(
            By.XPATH, '/html/body/div[4]/section[1]/div[2]/div/form/div[2]/ul/li[1]/ul/li[1]/div[2]').click()
        driver.find_element(
            By.XPATH, '/html/body/div[4]/section[1]/div[2]/div/form/div[2]/ul/li[1]/ul/li[1]/div[2]/ul/li['+str(int(To_Floor_Website)+1)+']').click()

        driver.find_element(
            By.XPATH, '/html/body/div[4]/section[1]/div[2]/div/form/div[2]/ul/li[1]/ul/li[2]/div[1]').click()
        driver.find_element(
            By.XPATH, '/html/body/div[4]/section[1]/div[2]/div/form/div[2]/ul/li[1]/ul/li[2]/div[1]/ul/li['+str(int(FromNumRooms_Website)+1)+']').click()

        driver.find_element(
            By.XPATH, '/html/body/div[4]/section[1]/div[2]/div/form/div[2]/ul/li[1]/ul/li[2]/div[2]').click()
        driver.find_element(
            By.XPATH, '/html/body/div[4]/section[1]/div[2]/div/form/div[2]/ul/li[1]/ul/li[2]/div[2]/ul/li['+str(int(ToNumRoom_Website)+1)+']').click()

        priceFrom_homelyls = str(FromPrice_Website)
        priceTo_homelyls = str(ToPrice_Website)

        if(int(FromPrice_Website) < 500000):
            priceFrom_homelyls = "500000"

        if (int(ToPrice_Website) > 15000000):
            priceTo_homelyls = "15000000"

        spanfromprice = driver.find_element(By.XPATH, '//*[@id="fromPrice"]')
        driver.execute_script(
            'arguments[0].innerHTML = '+str(priceFrom_homelyls)+';', spanfromprice)

        spantoprice = driver.find_element(By.XPATH, '//*[@id="toPrice"]')
        driver.execute_script(
            'arguments[0].innerHTML = ' + str(priceTo_homelyls) + ';', spantoprice)

        searchmore = driver.find_element(
            By.XPATH, '/html/body/div[4]/section[1]/div[2]/div/form/div[3]/input').click()

        filelinks = open("linkshomely.txt", "w+", encoding="utf-8")

        loop_house = 1
        while (True):
            try:
                house = driver.find_element(
                    By.XPATH, '/html/body/div[4]/section[2]/div/div/div/ul[2]/li['+str(loop_house)+']/div/a')
            except:
                break
            linkhouse = house.get_attribute("href")
            filelinks.write(linkhouse+"\n")
            loop_house = loop_house + 1

        loop_house = 1
        filelinks.close()
        filelinks = open("linkshomely.txt", "r+")
        for line in filelinks:
            linkh = line
            driver = webdriver.Firefox()
            driver.get(linkh)
            # sleep(2)
            # driver.close()

            mprice = driver.find_element(
                By.XPATH, '/html/body/div[4]/section[2]/div/div[1]/div[1]/div/h2')
            splitprice = str(mprice.text).split(" ")
            getprice = splitprice[0]

            aphone = driver.find_element(
                By.XPATH, '/html/body/div[4]/section[2]/div/div[2]/div[1]/div/ul/li[2]/a')
            splithphone = str(aphone.get_attribute("href")).split(":")
            getphone = splithphone[1]  # 2
            # print("price:" + getprice)
            # print("phone:"+getphone)
            # toop 5 rooms and metter .....
            for infoline in range(1, 10):
                try:
                    argument = driver.find_element(
                        By.XPATH, '/html/body/div[4]/section[2]/div/div[1]/div[2]/ul/li['+str(infoline)+']')
                except:
                    break
                # print(argument.text)

        filelinks.close()

    # /html/body/div[4]/section[1]/div[2]/div/form/div[2]/ul/li[1]/ul/li[1]/div[2]/ul/li[1]
    # /html/body/div[4]/section[1]/div[2]/div/form/div[2]/ul/li[1]/ul/li[1]/div[2]/ul/li[2]
    # from_rooms_input_2.clear()
        #  to_rooms_input_2 = driver.find_element(By.XPATH, '//*[@id="totalText"]')
        # to_rooms_input_2.clear()

    website_driver = 'https://www.onmap.co.il/homes/buy'
    driver.get(website_driver)
    # time.sleep(5)

    element1 = WebDriverWait(driver, 20).until(expected_conditions.presence_of_element_located(
        (By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[2]/div/div/div/input")))
    city_input2 = driver.find_element(
        By.XPATH, '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[2]/div/div/div/input')
    city_input2.send_keys(City_Website)

    element2 = WebDriverWait(driver, 20).until(expected_conditions.presence_of_element_located(
        (By.XPATH, '//*[@id="react-autowhatever-1--item-0"]/div')))
    location_input__suggestion = driver.find_element(
        By.XPATH, '//*[@id="react-autowhatever-1--item-0"]/div')
    location_input__suggestion.click()

    time.sleep(1)

    buttonroom = driver.find_element(
        By.XPATH, '/html/body/div[1]/div/div[1]/div/div[1]/div/div[1]/div[4]/button')
    buttonroom.click()

    # rooms select
    fromNumRoomsInteger = int(FromNumRooms_Website)
    endNumRoomsInteger = int(ToNumRoom_Website)
    if(fromNumRoomsInteger > 6):
        driver.find_element(
            By.XPATH, '/html/body/div[1]/div/div[1]/div/div[1]/div/div[1]/div[4]/ul/li[7]/label').click()
    else:
        for i in range(fromNumRoomsInteger, (endNumRoomsInteger+1)):
            if(i < 7):
                driver.find_element(
                    By.XPATH, '/html/body/div[1]/div/div[1]/div/div[1]/div/div[1]/div[4]/ul/li['+str(i+1)+']/label').click()
    file_info_links.close()

    # price min
    price_min = driver.find_element(
        By.XPATH, '/html/body/div[1]/div/div[1]/div/div[1]/div/div[1]/div[5]/div/div[1]/input')
    price_min.send_keys(FromPrice_Website)

    # price max
    price_max = driver.find_element(
        By.XPATH, '/html/body/div[1]/div/div[1]/div/div[1]/div/div[1]/div[5]/div/div[2]/input')
    price_max.send_keys(ToPrice_Website)

    # addition propretiotn
    driver.find_element(
        By.XPATH, '/html/body/div[1]/div/div[1]/div/div[1]/div/div[1]/div[6]').click()

    # Park and balcony #elevator
    if(isParking):
        driver.find_element(
            By.XPATH, '/html/body/div[4]/div/div/div[2]/div[1]/label[1]').click()
    if(isBalcony):
        driver.find_element(
            By.XPATH, '/html/body/div[4]/div/div/div[2]/div[1]/label[2]').click()
    if(isElevator):
        driver.find_element(
            By.XPATH, '/html/body/div[4]/div/div/div[2]/div[1]/label[3]').click()
    if(iswareHouse):
        driver.find_element(
            By.XPATH, '/html/body/div[4]/div/div/div[2]/div[2]/div[2]/div[1]/div[6]/label').click()
    if(isGarbage_chute):
        driver.find_element(
            By.XPATH, '/html/body/div[4]/div/div/div[2]/div[2]/div[2]/div[2]/div[1]/label').click()
    if(isAccessible):
        driver.find_element(
            By.XPATH, '/html/body/div[4]/div/div/div[2]/div[2]/div[2]/div[2]/div[3]/label').click()
    if(isGym):
        driver.find_element(
            By.XPATH, '/html/body/div[4]/div/div/div[2]/div[2]/div[2]/div[2]/div[2]/label').click()
    if(isStroller_room):
        driver.find_element(
            By.XPATH, '/html/body/div[4]/div/div/div[2]/div[2]/div[2]/div[2]/div[4]/label').click()

    # Floor from
    floor_From = driver.find_element(
        By.XPATH, '/html/body/div[4]/div/div/div[2]/div[1]/div[1]/div/div[2]/div[1]/input')
    floor_From.send_keys(From_Floor_Website)
    floor_To = driver.find_element(
        By.XPATH, '/html/body/div[4]/div/div/div[2]/div[1]/div[1]/div/div[2]/div[3]/input')
    floor_To.send_keys(To_Floor_Website)
    driver.find_element(
        By.XPATH, '/html/body/div[4]/div/div/div[3]/button[2]').click()

    element1 = WebDriverWait(driver, 20).until(expected_conditions.presence_of_element_located(
        (By.XPATH, "/html/body/div[1]/div/div[1]/div/div[2]/div[1]/div[1]/div/div/div[1]/div[2]/h2/span")))

    span = driver.find_element(
        By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]/div[1]/div[1]/div/div/div[1]/div[2]/h2/span')
    lineFound = span.get_attribute("innerHTML")

    number_rows_onmap = lineFound[5]

    int_number_rows_onmap = int(number_rows_onmap)
    for c in range(1, int_number_rows_onmap+1):
        if(check_exists_by_xpath('/html/body/div[1]/div/div[1]/div/div[2]/div[1]/div[1]/div/div/div[2]/div['+str(c)+']/div[1]/div/div[1]/img')):
            element = driver.find_element(
                By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]/div[1]/div[1]/div/div/div[2]/div['+str(c)+']/div[1]/div/div[1]/img')
        else:
            element = driver.find_element(
                By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]/div[1]/div[1]/div/div/div[2]/div['+str(c)+']/div[1]/div/div[1]/div/div/div[1]/div[1]/img')

        element.click()
        sleep(1)
        location = driver.find_element(
            By.XPATH, '/html/body/div[4]/div/div/div[2]/div[2]/div[2]/div[1]/div/div[2]/h1')

        pricespan = driver.find_element(
            By.XPATH, '/html/body/div[4]/div/div/div[2]/div[2]/div[2]/div[1]/div/div[2]/div[1]/span[1]')
        lineprice = pricespan.get_attribute("innerHTML")
        splitrpice = str(lineprice).split(" ")
        priceline = splitrpice[3]
        firstindex1 = priceline.index(">")
        secondindex1 = priceline.index("<")
        price_website = priceline[firstindex1+1:secondindex1]

        numberofroomsspan = driver.find_element(
            By.XPATH, '/html/body/div[4]/div/div/div[2]/div[2]/div[2]/div[1]/div/div[2]/div[2]/div[1]/span[2]')
        numberofrooms = numberofroomsspan.get_attribute("innerHTML")
        splitnumberofrooms = str(numberofrooms).split(" ")
        linenumberr = splitnumberofrooms[14]
        firstindex = linenumberr.index(">")
        secondindex = linenumberr.index("<")
        numberofrooms_website = linenumberr[firstindex+1:secondindex]
        # print("number rooms:" + numberofrooms_website)

        metterspan = driver.find_element(
            By.XPATH, '/html/body/div[4]/div/div/div[2]/div[2]/div[2]/div[1]/div/div[2]/div[2]/div[3]/span[2]')
        metterall = metterspan.get_attribute("innerHTML")
        metter_website = metterall[5:]

        numberoffloorspan = driver.find_element(
            By.XPATH, '/html/body/div[4]/div/div/div[2]/div[2]/div[2]/div[1]/div/div[2]/div[2]/div[2]/span[2]')
        numberoffloor = numberoffloorspan.get_attribute("innerHTML")
        splitnumberoffloor = str(numberoffloor).split(" ")
        linefloor = splitnumberoffloor[14]
        firstindex = linefloor.index(">")
        secondindex = linefloor.index("<")
        numberoffloor_website = linefloor[firstindex+1:secondindex]
        # print("number of floor :" + numberoffloor_website)

        g = 1
        tcount = 1
        # m3let
        elevatorspan = driver.find_element(
            By.XPATH, '/html/body/div[4]/div/div/div[2]/div[2]/div[2]/div[4]/div/div[1]/div[1]/div/span[2]')
        numberelevator = elevatorspan.get_attribute("innerHTML")
        sleep(2)
        # click phone

        if(check_exists_by_xpath('/html/body/div[4]/div/div/div[2]/div[2]/div[1]/div/div[1]/div[1]/div[2]')):
            phone = driver.find_element(
                By.XPATH, '/html/body/div[4]/div/div/div[2]/div[2]/div[1]/div/div[1]/div[1]/div[2]')
            phone.click()
            phone_website = phone.text
        else:
            phone = driver.find_element(
                By.XPATH, '/html/body/div[4]/div/div/div[2]/div[2]/div[1]/div/div[1]/div[2]/div[2]')
            phone.click()
            phone_website = phone.text

        link_Tab = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/a')
        link_website = link_Tab.get_attribute("href")

        file_house_onmap.write(str(c) + "-----"+str(City_Website)+"-----"+str(price_website)+"-----"+str(numberoffloor_website) + "-----"+str(numberofrooms_website)+"-----"+str(location.text).replace('\n', '-')
                               + "-----"+str(phone_website) + "-----"+str(metter_website) + "-----" + str(link_website)+"-----")
        # 3al benyan
        while True:
            flag = check_exists_by_xpath(
                '/html/body/div[4]/div/div/div[2]/div[2]/div[2]/div[4]/div/div[2]/div/span['+str(tcount)+']')
            if(flag == True):
                addtion = driver.find_element(
                    By.XPATH, '/html/body/div[4]/div/div/div[2]/div[2]/div[2]/div[4]/div/div[2]/div/span['+str(tcount)+']')
                textadd = str(addtion.get_attribute("innerHTML"))
                textadde2 = textadd.split(" ")
                t = textadde2[3]
                t4 = textadde2[4]
                if(not t4.__eq__("/react-text")):
                    t = t+" "+t4
                firstindex = t.index(">")
                secondindex = t.index("<")
                add2 = t[firstindex + 1:secondindex]
                file_house_onmap.write(add2 + ":")
            else:
                break
            tcount = tcount+1
    # 3al ne5es
        while True:
            flag = check_exists_by_xpath(
                '/html/body/div[4]/div/div/div[2]/div[2]/div[2]/div[4]/div/div[3]/div/span['+str(g)+']')
            if(flag == True):
                addtion1 = driver.find_element(
                    By.XPATH, '/html/body/div[4]/div/div/div[2]/div[2]/div[2]/div[4]/div/div[3]/div/span['+str(g)+']')
                textadd2 = str(addtion1.get_attribute("innerHTML"))
                textadde = textadd2.split(" ")
                t2 = str(textadde[3])
                t21 = str(textadde[4])
                if (not t21.__eq__("/react-text")):
                    t2 = t2 + " "+t21
                firstindex = t2.index(">")
                secondindex = t2.index("<")
                add1 = t2[firstindex + 1:secondindex]
                file_house_onmap.write(add1 + ":")
            else:
                break
            g = g+1

        driver.find_element(
            By.XPATH, '/html/body/div[4]/div/div/span/span').click()
        file_house_onmap.write("\n")
    file_house_onmap.close()

    f = open("nadlan_house.txt", "r+", encoding="utf-8")
    f2 = open("onMap_house.txt", "r+", encoding="utf-8")
    f3 = open("ratehouse.txt", "w+", encoding="utf-8")
    f4 = open("onMap_house.txt", "r+", encoding="utf-8")

    # for linenadlan in f:
    # arrayndlan = linenadlan.split(":")
    # address_nadlan = arrayndlan[5]
    # address_nadln = ''.join([i for i in address_nadlan if not i.isdigit()]).strip()
    # address_nadlan_number1 = [int(s) for s in str.split() if s.isdigit()]
    # address_nadlan_number = str(address_nadlan_number1)

    s = 1
    for lineOnmap in f2:
        arrayomap = lineOnmap.split("-----")
        if(s > 1):
            f3.write("\n")
        # print(arrayomap[0])
        f3.write(arrayomap[0]+":")
        location_onmap = arrayomap[5].split("-")
        address_onmap = str(location_onmap[0])
        city_onmap = str(location_onmap[1])
        address_map = ''.join(
            [i for i in address_onmap if not i.isdigit()]).strip()
        metter_map = arrayomap[7]
        firstprice = int(arrayomap[2].replace(",", ""))
        s = s+1
        f4 = open("onMap_house.txt", "r+", encoding="utf-8")
        add = arrayomap[9:]
        for i in range(1, len(add)):
            if (str(add[i]).strip().__eq__("ממ״ד") or str(add[i]).strip().__eq__("משופץ") or str(add[i]).strip().__eq__("מיזוג") or str(add[i]).strip().__eq__("יחידת הורים") or str(add[i]).strip().__eq__("מחסן") or str(add[i]).strip().__eq__("בריכה") or str(add[i]).strip().__eq__("סורגים") or str(add[i]).__eq__("משופצת")):
                f3.write("1 ")

        for secondline in f4:
            if(not lineOnmap.__eq__(secondline)):
                secondarray = secondline.split("-----")
                # print(secondline)
                secondmetter = secondarray[7]
                secondprice = int(secondarray[2].replace(",", ""))
                if(int(metter_map) > int(secondmetter)):
                    if(firstprice < secondprice):
                        f3.write("1 ")

    f3.close()
    f3 = open("ratehouse.txt", "r+", encoding="utf-8")

    max = 0
    lene = 0

    stringmax = ""
    for line2 in f3:
        numbermax = line2.split("-----")
        lineee = line2.split(" ")
        lene = len(lineee)
        if(lene > max):
            max = lene
            stringmax = numbermax[0]
    # check if the

    f3 = open("onMap_house.txt", "r+", encoding="utf-8")
    besthouse = ""
    for line3 in f3:
        lines = line3.strip("-----")
        if(stringmax.__eq__(lines[0])):
            besthouse = line3

    print(besthouse)
    f.close()
    f2.close()
    f3.close()
    f4.close()
    time.sleep(1)
    driver.close()

    return render(request, "myapp/newPage.html")
