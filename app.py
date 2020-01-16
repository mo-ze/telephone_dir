import csv
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import admin
ff = webdriver.Firefox()
URL=admin.URL
ff.get(URL)


def data_entry(keys):
    last = ff.find_element_by_class_name("dataentrytable") \
        .find_element_by_class_name("dedefault") \
        .find_element_by_tag_name("input")
    last.send_keys(keys)
    submit = ff.find_element_by_tag_name("pre") \
        .find_element_by_css_selector("input[type='submit']")
    submit.click()


def copy_table():
    content = ff.find_element_by_tag_name('table') \
        .get_attribute('innerHTML')

    def remove_attrs(soup):
        for tag in soup():
            for attribute in ["class", "nowrap", "href"]:  # You can also add id,style,etc in the list
                del tag[attribute]
        return soup;

    soup = BS(content, 'lxml')
    soup = remove_attrs(soup)
    rows = []
    for tr in soup.findAll('tr'):
        m = tr.findAll('td')
        m = [str(i).replace('<td>', '').replace('</td>', '').replace('<a>', '').replace('</a>', '')
             for i in m]
        rows.append(m)

    with open("output.csv", "a") as fp:
        for i in range(0, len(rows)):
            wr = csv.writer(fp, dialect='excel')
            wr.writerow(rows[i])


def next_page():
    try:

        x = ff.find_element_by_xpath("//a[contains(.,'Next >')]")
        copy_table()
        x.click()
    except NoSuchElementException:
        try:
            y = ff.find_element_by_xpath("//a[contains(.,'New Search')]")
            copy_table()
            y.click()
        except NoSuchElementException:
            # break the infinite loop in the do()
            raise NoSuchElementException("")


def do():
    list1 = ['a', 'b', 'c', 'd', 'e', 'f', 'g',
             'h', 'i', 'j', 'k', 'l', 'm',
             'n', 'o', 'p', 'q', 'r', 's',
             't', 'u', 'v', 'w', 'x', 'y', 'z']
    for i in list1:
        data_entry(i)

        while True:
            try:
                next_page()
            except NoSuchElementException:
                break


do()

ff.close()
