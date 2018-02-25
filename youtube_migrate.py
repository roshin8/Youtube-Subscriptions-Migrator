"""
Automatic migration of subscriptions to another
YouTube account with Python and Selenium.

Tested with:
 - selenium 3.0
 - firefox 49.0
 - python 3.5

 1. Install selenium from pypi:
    $ pip install selenium

 2. Go to the down of page https://www.youtube.com/subscription_manager
    and download your current subscriptions feed.
    Save file as subscription_manager.xml.

 4. Run script, enter your credentials and go to drink coffee.
    It will take some time.

Note YouTube will temporary block you if you have more that 80 subscriptions.
Just restart the script in a few hours.
"""

from collections import namedtuple
from selenium import webdriver
from xml.dom import minidom
import time
import re


def main():
    driver = webdriver.Firefox()
    sign_in(driver)
    for channel in load_subcribtions():
        subscribe(driver, channel)
    driver.close()


def sign_in(driver):
    driver.get('https://www.youtube.com')

    # email, password = raw_input('Email: '), raw_input('Password: ')
    email = "roshinlistens@gmail.com"
    password = "!X5tech!"
    driver.find_element_by_css_selector('ytd-button-renderer.style-scope:nth-child(4)').click()
    time.sleep(1)

    driver.find_element_by_id('identifierId').send_keys(email)
    driver.find_element_by_id('identifierNext').click()
    time.sleep(1)

    driver.find_element_by_css_selector('#password > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)').send_keys(password)
    driver.find_element_by_id('passwordNext').click()
    time.sleep(1)


def load_subcribtions():
    xmldoc = minidom.parse('subscription_manager.xml')
    itemlist = xmldoc.getElementsByTagName('outline')
    channel_id_regexp = re.compile('channel_id=(.*)$')
    Channel = namedtuple('Channel', ['id', 'title'])
    subscriptions = []

    for item in itemlist:
        try:
            feed_url = item.attributes['xmlUrl'].value
            channel = Channel(id=channel_id_regexp.findall(feed_url)[0],
                              title=item.attributes['title'].value)
            subscriptions.append(channel)
        except KeyError:
            pass

    return subscriptions


def subscribe(driver, channel):
    channel_url = 'https://www.youtube.com/channel/' + channel.id
    driver.get(channel_url)
    time.sleep(1)
    is_subscribed = True
    try:
        button = driver.find_element_by_id('subscribe-button')
        is_subscribed = button.get_attribute('data-is-subscribed')
        if not is_subscribed:
            button.click()
    except:
        # Account has been terminated
        pass
    print('{:.<50}{}'.format(channel.title, 'SKIPPED!' if is_subscribed else 'Done'))
    time.sleep(1)


if __name__ == '__main__':
    main()