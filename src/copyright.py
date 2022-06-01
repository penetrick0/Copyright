# copyright.py

import pandas as pd
import pynput
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_extension("adguard.crx")  # AdGuard
# options.add_argument("headless")
options.add_argument("--start-maximized")
options.add_argument("--mute-audio")

driver01 = webdriver.Chrome("chromedriver.exe", options=options)
driver02 = webdriver.Chrome("chromedriver.exe", options=options)
driver03 = webdriver.Chrome("chromedriver.exe", options=options)
driver04 = webdriver.Chrome("chromedriver.exe", options=options)

nums = ('1', '2', '3', '4', '5')
contents = pd.read_csv("list/contents.csv")


def mouse_click():
    mouse_drag = pynput.mouse.Controller()
    mouse_button = pynput.mouse.Button

    mouse_drag.position = (695, 425)

    mouse_drag.press(mouse_button.left)
    mouse_drag.release(mouse_button.left)
    time.sleep(1)

    mouse_drag.press(mouse_button.left)
    mouse_drag.release(mouse_button.left)
    time.sleep(1)

    mouse_drag.press(mouse_button.left)
    mouse_drag.release(mouse_button.left)
    time.sleep(3)


class BayDrama:
    def __init__(self, url):
        with open("result/baydrama.csv", 'a') as file:
            file.write("SITE_URL,NAME,DOWNLOAD_URL\n")
        for content_name, content_type in zip(contents["NAME"], contents["TYPE"]):
            if content_type == 'D':  # Drama
                for num in nums:
                    name = content_name.replace(' ', '')
                    print(name)
                    try:
                        driver01.get(url + "bbs/board.php"
                                           "?bo_table=tvdrama&sca=&sfl=wr_subject&stx={}&sop=and"
                                     .format(name + ' ' + num + "회"))
                        site_urls = driver01.find_elements(By.XPATH, "//ul[@id='list-body']//li//a")
                    except Exception as error:
                        print("[driver01 exception]\n", error)
                        continue
                    for site_url in site_urls:
                        if ' ' + num + "회" in site_url.text:
                            try:
                                driver02.get(site_url.get_attribute("href"))
                                redirect_urls = driver02.find_elements(By.XPATH, "//div[@class='view-content']//a")
                            except Exception as error:
                                print("[driver02 exception]\n", error)
                                continue
                            for redirect_url in redirect_urls:  # Redirect URL
                                try:
                                    driver03.get(redirect_url.get_attribute("href"))
                                    time.sleep(3)
                                    mouse_click()
                                    download = driver03.find_element(By.XPATH, "//video").get_attribute("src")
                                    if "blob" not in download and download:
                                        with open("result/baydrama.csv", 'a', encoding="utf-8") as file:
                                            file.write(url + ',' + name + ' ' + num + "화," + download + '\n')
                                except Exception as error:
                                    print("[driver03 exception]\n", error)
                                    continue
            else:  # Movie
                name = content_name.replace(' ', '')
                print(name)
                try:
                    driver01.get(url + "bbs/board.php?bo_table=kmovie&sca=&sfl=wr_subject&stx={}&sop=and".format(name))
                    site_url = driver01.find_element(By.XPATH, "//div[@class='list-desc']//a")
                except Exception as error:
                    print("[driver01 exception]\n", error)
                    continue
                if name in site_url.text:
                    try:
                        driver02.get(site_url.get_attribute("href"))
                        redirect_urls = driver02.find_elements(By.XPATH, "//div[@id='movie_bt']//a")
                    except Exception as error:
                        print("[driver02 exception]", error)
                        continue
                    for redirect_url in redirect_urls:
                        try:
                            driver03.get(redirect_url.get_attribute("href"))
                            time.sleep(3)
                            mouse_click()
                            download = driver03.find_element(By.XPATH, "//video").get_attribute("src")
                            if "blob" not in download and download:
                                with open("result/baydrama.csv", 'a', encoding="utf-8") as file:
                                    file.write(url + ',' + name + ',' + download + '\n')
                        except Exception as error:
                            print("[driver03 exception]\n", error)
                            continue


class NewsDaum:
    def __init__(self, url):
        with open("result/newsdaum.csv", 'a') as file:
            file.write("SITE_URL,NAME,DOWNLOAD_URL\n")
        for content_name, content_type in zip(contents["NAME"], contents["TYPE"]):
            name = content_name.replace(' ', '')
            print(name)

            if content_type == 'D':
                try:
                    driver01.get(url + "bbs/board.php?bo_table=c09&sca=&sfl=wr_subject&stx={}&sop=and".format(name))
                    site_url = driver01.find_element(By.XPATH, "//div[@class='list-desc']//a").get_attribute("href")
                except Exception as error:
                    print("[driver01 exception]", error)
                    continue

                try:
                    driver02.get(site_url)
                    redirect_urls = driver02.find_elements(By.XPATH, "//div[@class='view-content']/p[2]/span/a")
                except Exception as error:
                    print("[driver02 exception]", error)
                    continue

                for index, redirect_url in enumerate(redirect_urls):
                    if index < 5:
                        try:
                            driver03.get(redirect_url.get_attribute("href"))
                            time.sleep(3)
                            mouse_click()
                            iframe = driver03.find_element(By.XPATH, "//iframe")
                            driver03.switch_to.frame(iframe)
                            download = driver03.find_element(By.XPATH, "//video").get_attribute("src")
                            if "blob" not in download and download:
                                with open("result/newsdaum.csv", 'a', encoding="utf-8") as file:
                                    file.write(url + ',' + name + ' ' + str(index + 1) + "화," + download + '\n')
                        except Exception as error:
                            print("[driver03 exception]", error)
                            continue
            else:  # M
                try:
                    driver01.get(url + "bbs/board.php?bo_table=a01&sca=&sfl=wr_subject&stx={}&sop=and".format(name))
                    site_url = driver01.find_element(By.XPATH, "//div[@class='list-desc']//a").get_attribute("href")
                except Exception as error:
                    print("[driver01 exception]", error)
                    continue

                try:
                    driver02.get(site_url)
                    redirect_urls = driver02.find_elements(By.XPATH, "//div[@class='view-content']//a")
                except Exception as error:
                    print("[driver02 exception]", error)
                    continue

                for redirect_url in redirect_urls:
                    try:
                        driver03.get(redirect_url.get_attribute("href"))
                        time.sleep(3)
                        mouse_click()
                        iframe = driver03.find_element(By.XPATH, "//iframe")
                        driver03.switch_to.frame(iframe)
                        download = driver03.find_element(By.XPATH, "//video").get_attribute("src")
                        if "blob" not in download and download:
                            with open("result/newsdaum.csv", 'a', encoding="utf-8") as file:
                                file.write(url + ',' + name + ',' + download + '\n')
                    except Exception as error:
                        print("[driver03 exception]", error)
                        continue


class TakiTv:
    def __init__(self, url):
        with open("result/takitv.csv", 'a') as file:
            file.write("SITE_URL,NAME,DOWNLOAD_URL\n")
        for content_name, content_type in zip(contents["NAME"], contents["TYPE"]):
            if content_type == 'D':
                name = content_name.replace(' ', '')
                print(name)
                try:
                    driver01.get(url + "?s={}".format(name))
                    site_urls = driver01.find_elements(By.XPATH, "//div[@class='item-details']//a")
                except Exception as error:
                    print("[driver01 exception]", error)
                    continue

                for site_url in site_urls:
                    for num in nums:
                        if ' ' + num + "화" in site_url.text:
                            try:
                                driver02.get(site_url.get_attribute("href"))
                                redirect_urls = driver02.find_elements(By.XPATH, "//div[@class='linkcontents']//li/a")
                            except Exception as error:
                                print("[driver02 exception]", error)
                                continue

                            for redirect_url in redirect_urls:
                                try:
                                    driver03.get(redirect_url.get_attribute("href"))
                                    time.sleep(3)
                                    mouse_click()
                                    iframe = driver03.find_element(By.XPATH, "//iframe")
                                    driver03.switch_to.frame(iframe)
                                    download = driver03.find_element(By.XPATH, "//video").get_attribute("src")
                                    if "blob" not in download and download:
                                        with open("result/takitv.csv", 'a', encoding="utf-8") as file:
                                            file.write(url + ',' + name + ' ' + num + "화," + download + '\n')
                                except Exception as error:
                                    print("[driver03 exception]", error)
                                    continue
            else:  # M
                break


class Koreanz:
    def __init__(self, url):
        with open("result/koreanz.csv", 'a') as file:
            file.write("SITE_URL,NAME,DOWNLOAD_URL\n")
        for content_name, content_type in zip(contents["NAME"], contents["TYPE"]):
            name = content_name.replace(' ', '')
            print(name)
            if content_type == 'D':
                for num in nums:
                    try:
                        driver01.get(url + "bbs/search.php"
                                           "?sfl=wr_subject&stx={}&sop=and&gr_id=&onetable=kd"
                                     .format(name + ' ' + num + "화"))
                        site_urls = driver01.find_elements(By.XPATH, "//div[@class='media-content']//a")
                    except Exception as error:
                        print("[driver01 exception]", error)
                        continue

                    for site_url in site_urls:
                        if ' ' + num + "화" in site_url.text:
                            try:
                                driver02.get(site_url.get_attribute("href"))
                                redirect_urls = driver02.find_elements(By.XPATH, "//div[@id='movie_bt']//a")
                            except Exception as error:
                                print("[driver02 exception]", error)
                                continue

                            for redirect_url in redirect_urls:
                                try:
                                    driver03.get(redirect_url.get_attribute("href"))
                                    time.sleep(3)
                                    mouse_click()
                                    download = driver03.find_element(By.XPATH, "//video").get_attribute("src")
                                    if "blob" not in download and download:
                                        with open("result/koreanz.csv", 'a', encoding="utf-8") as file:
                                            file.write(url + ',' + name + ' ' + num + "화," + download + '\n')
                                except Exception as error:
                                    print("[driver03 exception]", error)
                                    continue
            else:  # M
                try:
                    driver01.get(url + "bbs/search.php"
                                       "?sfl=wr_subject&stx={}&sop=and&gr_id=&onetable=kmovie".format(name))
                    site_urls = driver01.find_elements(By.XPATH, "//div[@class='media-content']//a")
                except Exception as error:
                    print("[driver01 exception]", error)
                    continue

                for site_url in site_urls:
                    if name in site_url.text:
                        try:
                            driver02.get(site_url.get_attribute("href"))
                            redirect_urls = driver02.find_elements(By.XPATH, "//div[@id='movie_bt']//a")
                        except Exception as error:
                            print("[driver02 exception]", error)
                            continue

                        for redirect_url in redirect_urls:
                            try:
                                driver03.get(redirect_url.get_attribute("href"))
                                time.sleep(3)
                                mouse_click()
                                download = driver03.find_element(By.XPATH, "//video").get_attribute("src")
                                if "blob" not in download and download:
                                    with open("result/koreanz.csv", 'a', encoding="utf-8") as file:
                                        file.write(url + ',' + name + ',' + download + '\n')
                            except Exception as error:
                                print("[driver03 exception]", error)
                                continue


class SonagiTv:
    def __init__(self, url):
        with open("result/sonagitv.csv", 'a') as file:
            file.write("SITE_URL,NAME,DOWNLOAD_URL\n")
        for content_name, content_type in zip(contents["NAME"], contents["TYPE"]):
            name = content_name.replace(' ', '')
            print(name)
            if content_type == 'D':
                try:
                    driver01.get(url + "?s={}".format(name))
                    site_urls = driver01.find_elements(By.XPATH, "//div[@class='row video-section meta-maxwidth-230']"
                                                                 "//div//h3//a")
                except Exception as error:
                    print("[driver01 exception]", error)
                    continue
                for site_url in site_urls:
                    for num in nums:
                        if ' ' + num + "회" in site_url.text:
                            try:
                                driver02.get(site_url.get_attribute("href"))
                                redirect_url = driver02.find_element(By.XPATH, "//a[@class='MVepisodebt']")
                            except Exception as error:
                                print("[driver02 exception]", error)
                                continue
                            try:
                                driver03.get(redirect_url.get_attribute("href"))
                                links = driver03.find_elements(By.XPATH, "//ul[@class='pagination post-tape']//a")
                            except Exception as error:
                                print("[driver03 exception]", error)
                                continue
                            for link in links:
                                try:
                                    driver04.get(link.get_attribute("href"))
                                    time.sleep(3)
                                    mouse_click()
                                    iframe = driver04.find_element(By.XPATH, "//iframe")
                                    driver04.switch_to.frame(iframe)
                                    download = driver04.find_element(By.XPATH, "//video").get_attribute("src")
                                    if "blob" not in download and download:
                                        with open("result/sonagitv.csv", 'a', encoding="utf-8") as file:
                                            file.write(url + ',' + name + ' ' + num + "화," + download + '\n')
                                except Exception as error:
                                    print("[driver04 exception]", error)
                                    continue
            else:
                try:
                    driver01.get(url + "?s=영화 {}".format(name))
                    site_url = driver01.find_element(By.XPATH, "//div[@class='row video-section meta-maxwidth-230']"
                                                               "//div//h3//a")
                except Exception as error:
                    print("[driver01 exception]", error)
                    continue

                try:
                    driver02.get(site_url.get_attribute("href"))
                    redirect_url = driver02.find_element(By.XPATH, "//a[@class='MVepisodebt']")
                except Exception as error:
                    print("[driver02 exception]", error)
                    continue

                try:
                    driver03.get(redirect_url.get_attribute("href"))
                    links = driver03.find_elements(By.XPATH, "//ul[@class='pagination post-tape']//a")
                except Exception as error:
                    print("[driver03 exception]", error)
                    continue

                for link in links:
                    try:
                        driver04.get(link.get_attribute("href"))
                        time.sleep(3)
                        mouse_click()
                        iframe = driver04.find_element(By.XPATH, "//iframe")
                        driver04.switch_to.frame(iframe)
                        download = driver04.find_element(By.XPATH, "//video").get_attribute("src")
                        if "blob" not in download and download:
                            with open("result/sonagitv.csv", 'a', encoding="utf-8") as file:
                                file.write(url + ',' + name + ',' + download + '\n')
                    except Exception as error:
                        print("[driver04 exception]", error)
                        continue


class DanbiMovie:
    def __init__(self, url):
        with open("result/danbimovie.csv", 'a') as file:
            file.write("SITE_URL,NAME,DOWNLOAD_URL\n")
        for content_name, content_type in zip(contents["NAME"], contents["TYPE"]):
            name = content_name.replace(' ', '')
            print(name)
            if content_type == 'D':
                try:
                    driver01.get(url + "?s=드라마 {}".format(name))
                    site_url = driver01.find_element(By.XPATH, "//div[@class='row video-section meta-maxwidth-230']//a")
                    driver01.get(site_url.get_attribute("href"))
                    redirect_url = driver02.find_element(By.XPATH, "//a[@class='MVdramabt']")
                    driver01.get(redirect_url.get_attribute("href"))
                    site_urls = driver01.find_elements(By.XPATH, "//div[@class='row video-section meta-maxwidth-230']"
                                                                 "//h3//a")
                except Exception as error:
                    print("[driver01 exception]", error)
                    continue
                for site_url in site_urls:
                    for num in nums:
                        if name + ' ' + num + "회" in site_url.text:
                            try:
                                driver02.get(site_url.get_attribute("href"))
                                redirect_url = driver02.find_element(By.XPATH, "//a[@class='MVepisodebt']")
                            except Exception as error:
                                print("[driver02 exception]", error)
                                continue

                            try:
                                driver03.get(redirect_url.get_attribute("href"))
                                links = driver03.find_elements(By.XPATH, "//ul[@class='pagination post-tape']//a")
                            except Exception as error:
                                print("[driver03 exception]", error)
                                continue

                            for link in links:
                                try:
                                    driver04.get(link.get_attribute("href"))
                                    time.sleep(3)
                                    mouse_click()
                                    iframe = driver04.find_element(By.XPATH, "//iframe")
                                    driver04.switch_to.frame(iframe)
                                    download = driver04.find_element(By.XPATH, "//video").get_attribute("src")
                                    if "blob" not in download and download:
                                        with open("result/danbimovie.csv", 'a', encoding="utf-8") as file:
                                            file.write(url + ',' + name + ' ' + num + "화," + download + '\n')
                                except Exception as error:
                                    print("[driver04 exception]", error)
                                    continue
            else:
                try:
                    driver01.get(url + "?s=영화 {}".format(name))
                    site_url = driver01.find_element(By.XPATH, "//div"
                                                               "[@class='row video-section meta-maxwidth-230']//h3//a")
                except Exception as error:
                    print("[driver01 exception]", error)
                    continue

                try:
                    driver02.get(site_url.get_attribute("href"))
                    redirect_url = driver02.find_element(By.XPATH, "//div[@class='player player-small"
                                                                   " embed-responsive embed-responsive-16by9']//a")
                except Exception as error:
                    print("[driver02 exception]", error)
                    continue

                try:
                    driver03.get(redirect_url.get_attribute("href"))
                    links = driver03.find_elements(By.XPATH, "//ul[@class='pagination post-tape']//a")
                except Exception as error:
                    print("[driver03 exception]", error)
                    continue

                for link in links:
                    try:
                        driver04.get(link.get_attribute("href"))
                        time.sleep(3)
                        mouse_click()
                        iframe = driver04.find_element(By.XPATH, "//iframe")
                        driver04.switch_to.frame(iframe)
                        download = driver04.find_element(By.XPATH, "//video").get_attribute("src")
                        if "blob" not in download and download:
                            with open("result/danbimovie.csv", 'a', encoding="utf-8") as file:
                                file.write(url + ',' + name + ',' + download + '\n')
                    except Exception as error:
                        print("[driver04 exception]", error)
                        continue


class TvMeka:
    def __init__(self, url):
        with open("result/tvmeka.csv", 'a') as file:
            file.write("SITE_URL,NAME,DOWNLOAD_URL\n")
        for content_name, content_type in zip(contents["NAME"], contents["TYPE"]):
            name = content_name.replace(' ', '')
            if content_type == 'D':
                for num in nums:
                    try:
                        driver01.get(url + "bbs/search.php?sfl=wr_subject%7C%7Cwr_content"
                                           "&stx={} {}회&sop=and&gr_id=&onetable=tvdrama".format(name, num))
                        site_urls = driver01.find_elements(By.XPATH, "//div[@class='media']"
                                                                     "//div[@class='media-heading']//a")
                    except Exception as error:
                        print("[driver01 exception]", error)
                        continue

                    for site_url in site_urls:
                        if ' ' + num + "회" in site_url.text:
                            try:
                                driver02.get(site_url.get_attribute("href"))
                                redirect_urls = driver02.find_elements(By.XPATH, "//div[@class='view-content']//a")
                            except Exception as error:
                                print("[driver02 exception]", error)
                                continue

                            for redirect_url in redirect_urls:
                                try:
                                    driver03.get(redirect_url.get_attribute("href"))
                                    time.sleep(3)
                                    mouse_click()
                                    download = driver03.find_element(By.XPATH, "//video").get_attribute("src")
                                    if "blob" not in download and download:
                                        with open("result/tvmeka.csv", 'a', encoding="utf-8") as file:
                                            file.write(url + ',' + name + ' ' + num + "화," + download + '\n')
                                except Exception as error:
                                    print("[driver03 exception]", error)
                                    continue
            else:
                try:
                    driver01.get(url + "bbs/search.php?sfl=wr_subject%7C%7Cwr_content"
                                       "&stx={}&sop=and&gr_id=&onetable=kmovie".format(name))
                    site_url = driver01.find_element(By.XPATH, "//div[@class='media-heading']//a")
                except Exception as error:
                    print("[driver01 exception]", error)
                    continue

                try:
                    driver02.get(site_url.get_attribute("href"))
                    redirect_urls = driver02.find_elements(By.XPATH, "//div[@id='movie_bt']//a")
                except Exception as error:
                    print("[driver02 exception]", error)
                    continue

                for redirect_url in redirect_urls:
                    try:
                        driver03.get(redirect_url.get_attribute("href"))
                        time.sleep(3)
                        mouse_click()
                        download = driver03.find_element(By.XPATH, "//video").get_attribute("src")
                        if "blob" not in download and download:
                            with open("result/tvmeka.csv", 'a', encoding="utf-8") as file:
                                file.write(url + ',' + name + ',' + download + '\n')
                    except Exception as error:
                        print("[driver03 exception]", error)
                        continue


class TvUsan:
    def __init__(self, url):
        with open("result/tvusan.csv", 'a') as file:
            file.write("SITE_URL,NAME,DOWNLOAD_URL\n")
        for content_name, content_type in zip(contents["NAME"], contents["TYPE"]):
            name = content_name.replace(' ', '')
            if content_type == 'D':
                for num in nums:
                    try:
                        driver01.get(url + "bbs/search.php?sfl=wr_subject%7C%7Cwr_content"
                                           "&stx={} {}회&sop=and&gr_id=&onetable=tvdrama".format(name, num))
                        site_urls = driver01.find_elements(By.XPATH, "//div[@class='clearfix']//a")
                    except Exception as error:
                        print("[driver01 exception]", error)
                        continue

                    for site_url in site_urls:
                        if ' ' + num + "회" in site_url.text:
                            try:
                                driver02.get(site_url.get_attribute("href"))
                                redirect_urls = driver02.find_elements(By.XPATH, "//div[@class='view-content']//a")
                            except Exception as error:
                                print("[driver02 exception]", error)
                                continue

                            for redirect_url in redirect_urls:
                                try:
                                    driver03.get(redirect_url.get_attribute("href"))
                                    time.sleep(3)
                                    mouse_click()
                                    download = driver03.find_element(By.XPATH, "//video").get_attribute("src")
                                    if "blob" not in download and download:
                                        with open("result/tvusan.csv", 'a', encoding="utf-8") as file:
                                            file.write(url + ',' + name + ' ' + num + "화," + download + '\n')
                                except Exception as error:
                                    print("[driver03 exception]", error)
                                    continue
            else:
                try:
                    driver01.get(url + "bbs/search.php?sfl=wr_subject%7C%7Cwr_content"
                                       "&stx={}&sop=and&gr_id=&onetable=kmovie".format(name))
                    site_url = driver01.find_element(By.XPATH, "//div[@class='clearfix']//a")
                except Exception as error:
                    print("[driver01 exception]", error)
                    continue

                try:
                    driver02.get(site_url.get_attribute("href"))
                    redirect_urls = driver02.find_elements(By.XPATH, "//div[@id='movie_bt']//a")
                except Exception as error:
                    print("[driver02 exception]", error)
                    continue

                for redirect_url in redirect_urls:
                    try:
                        driver03.get(redirect_url.get_attribute("href"))
                        time.sleep(3)
                        mouse_click()
                        download = driver03.find_element(By.XPATH, "//video").get_attribute("src")
                        if "blob" not in download and download:
                            with open("result/tvusan.csv", 'a', encoding="utf-8") as file:
                                file.write(url + ',' + name + ',' + download + '\n')
                    except Exception as error:
                        print("[driver03 exception]", error)
                        continue


class MyBinu:
    def __init__(self, url):
        with open("result/mybinu.csv", 'a') as file:
            file.write("SITE_URL,NAME,DOWNLOAD_URL\n")
        for content_name, content_type in zip(contents["NAME"], contents["TYPE"]):
            if content_type == 'D':  # Drama
                for num in nums:
                    name = content_name.replace(' ', '')
                    print(name)
                    try:
                        driver01.get(url + "bbs/board.php"
                                           "?bo_table=tvdrama&sca=&sfl=wr_subject&stx={}&sop=and"
                                     .format(name + ' ' + num + "회"))
                        site_urls = driver01.find_elements(By.XPATH, "//ul[@id='list-body']//li//a")
                    except Exception as error:
                        print("[driver01 exception]\n", error)
                        continue
                    for site_url in site_urls:
                        if ' ' + num + "회" in site_url.text:
                            try:
                                driver02.get(site_url.get_attribute("href"))
                                redirect_urls = driver02.find_elements(By.XPATH, "//div[@class='view-content']//a")
                            except Exception as error:
                                print("[driver02 exception]\n", error)
                                continue
                            for redirect_url in redirect_urls:  # Redirect URL
                                try:
                                    driver03.get(redirect_url.get_attribute("href"))
                                    time.sleep(3)
                                    mouse_click()
                                    download = driver03.find_element(By.XPATH, "//video").get_attribute("src")
                                    if "blob" not in download and download:
                                        with open("result/mybinu.csv", 'a', encoding="utf-8") as file:
                                            file.write(url + ',' + name + ' ' + num + "화," + download + '\n')
                                except Exception as error:
                                    print("[driver03 exception]\n", error)
                                    continue
            else:  # Movie
                name = content_name.replace(' ', '')
                print(name)
                try:
                    driver01.get(url + "bbs/board.php?bo_table=kmovie&sca=&sfl=wr_subject&stx={}&sop=and".format(name))
                    site_url = driver01.find_element(By.XPATH, "//div[@class='list-desc']//a")
                except Exception as error:
                    print("[driver01 exception]\n", error)
                    continue
                if name in site_url.text:
                    try:
                        driver02.get(site_url.get_attribute("href"))
                        redirect_urls = driver02.find_elements(By.XPATH, "//div[@id='movie_bt']//a")
                    except Exception as error:
                        print("[driver02 exception]", error)
                        continue
                    for redirect_url in redirect_urls:
                        try:
                            driver03.get(redirect_url.get_attribute("href"))
                            time.sleep(3)
                            mouse_click()
                            download = driver03.find_element(By.XPATH, "//video").get_attribute("src")
                            if "blob" not in download and download:
                                with open("result/mybinu.csv", 'a', encoding="utf-8") as file:
                                    file.write(url + ',' + name + ',' + download + '\n')
                        except Exception as error:
                            print("[driver03 exception]\n", error)
                            continue


class MovieHolic:
    def __init__(self, url):
        with open("result/movieholic.csv", 'a') as file:
            file.write("SITE_URL,NAME,DOWNLOAD_URL\n")
        for content_name, content_type in zip(contents["NAME"], contents["TYPE"]):
            if content_type == 'D':  # Drama
                for num in nums:
                    name = content_name.replace(' ', '')
                    print(name)
                    try:
                        driver01.get(url + "bbs/board.php"
                                           "?bo_table=tvdrama&sca=&sfl=wr_subject&stx={}&sop=and"
                                     .format(name + ' ' + num + "회"))
                        site_urls = driver01.find_elements(By.XPATH, "//ul[@id='list-body']//li//a")
                    except Exception as error:
                        print("[driver01 exception]\n", error)
                        continue
                    for site_url in site_urls:
                        if ' ' + num + "회" in site_url.text:
                            try:
                                driver02.get(site_url.get_attribute("href"))
                                redirect_urls = driver02.find_elements(By.XPATH, "//div[@class='view-content']//a")
                            except Exception as error:
                                print("[driver02 exception]\n", error)
                                continue
                            for redirect_url in redirect_urls:  # Redirect URL
                                try:
                                    driver03.get(redirect_url.get_attribute("href"))
                                    time.sleep(3)
                                    mouse_click()
                                    download = driver03.find_element(By.XPATH, "//video").get_attribute("src")
                                    if "blob" not in download and download:
                                        with open("result/movieholic.csv", 'a', encoding="utf-8") as file:
                                            file.write(url + ',' + name + ' ' + num + "화," + download + '\n')
                                except Exception as error:
                                    print("[driver03 exception]\n", error)
                                    continue
            else:  # Movie
                name = content_name.replace(' ', '')
                print(name)
                try:
                    driver01.get(url + "bbs/board.php?bo_table=kmovie&sca=&sfl=wr_subject&stx={}&sop=and".format(name))
                    site_url = driver01.find_element(By.XPATH, "//div[@class='list-desc']//a")
                except Exception as error:
                    print("[driver01 exception]\n", error)
                    continue
                if name in site_url.text:
                    try:
                        driver02.get(site_url.get_attribute("href"))
                        redirect_urls = driver02.find_elements(By.XPATH, "//div[@id='movie_bt']//a")
                    except Exception as error:
                        print("[driver02 exception]", error)
                        continue
                    for redirect_url in redirect_urls:
                        try:
                            driver03.get(redirect_url.get_attribute("href"))
                            time.sleep(3)
                            mouse_click()
                            download = driver03.find_element(By.XPATH, "//video").get_attribute("src")
                            if "blob" not in download and download:
                                with open("result/movieholic.csv", 'a', encoding="utf-8") as file:
                                    file.write(url + ',' + name + ',' + download + '\n')
                        except Exception as error:
                            print("[driver03 exception]\n", error)
                            continue


if __name__ == "__main__":
    # driver01.quit()
    # driver02.quit()
    # driver03.quit()
    # driver04.quit()
