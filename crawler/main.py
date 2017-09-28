from lib import Browser
from lib import Shopee
from selenium.common.exceptions import TimeoutException as TE
import configparser
import requests
import json
from urllib import parse


def login(persist_cookie):
    cookie_file = './tmp/cookies.pkl'
    config = configparser.ConfigParser()
    config.read('./crawler/app.cnf')
    account = config['shopee']['account']
    password = config['shopee']['password']
    browser = Browser()
    try:
        browser.go(Shopee.login_page_url)
        browser.load_cookie_from(cookie_file)  #
        browser.send_by_css(Shopee.account_input_css_selector, account)
        browser.send_by_css(Shopee.password_input_css_selector, password)
        browser.click_by_xpath(Shopee.login_button_xpath)
        try:
            browser.wait_for(lambda driver: driver.find_element_by_css_selector(Shopee.verify_code_input_css_selector))
            browser.send_by_css(Shopee.verify_code_input_css_selector, input('input verify code: '))
            browser.click_by_xpath(Shopee.verify_button_xpath)
        except TE:
            pass
        browser.wait_for(lambda driver: driver.current_url == Shopee.home)
        if persist_cookie:
            browser.dump_cookie(cookie_file)
        return browser.get_cookies()
    finally:
        browser.quit()


def save_json(data, save_to):
    with open(save_to, 'w') as outfile:
        json.dump(data, outfile, ensure_ascii=False)


def main():
    cookie = login(True)
    cookie_string = ';'.join(['{}={}'.format(item.get('name'), item.get('value')) for item in cookie])
    spc_cds = [item.get('value') for item in cookie if item.get('name') == 'SPC_CDS'][0]

    # get categories
    conn = requests.Session()
    path = '/api/v1/categories/?SPC_CDS={}&SPC_CDS_VER=2'.format(spc_cds)
    cat_header = Shopee.general_header.copy()
    cat_header['method'] = 'GET'
    cat_header['path'] = path
    cat_header['cookie'] = cookie_string
    res = conn.get(Shopee.home + path, headers=cat_header)
    save_json(res.json(), './json/categories.json')

    # get attributes
    for cat in res.json()['categories']:
        try:
            cat_id = cat['id']
            catids_encoded = parse.quote('[{}]'.format(cat_id))
            path = '/api/v1/categories/attributes/?catids={}&SPC_CDS={}&SPC_CDS_VER=2'.format(catids_encoded, spc_cds)
            attr_header = Shopee.general_header.copy()
            attr_header['method'] = 'GET'
            attr_header['path'] = path
            attr_header['cookie'] = cookie_string
            res = conn.get(Shopee.home + path, headers=attr_header)
            save_json(res.json(), './json/attributes/' + str(cat_id) + '.json')

            # get items
            meta = res.json()['categories'][0]['meta']
            if 'modelid' in meta:
                model_id = str(meta['modelid'])
                path = '/api/v1/categories/attributes/?SPC_CDS={}&SPC_CDS_VER=2'.format(spc_cds)
                item_header = Shopee.general_header.copy()
                item_header['method'] = 'POST'
                item_header['path'] = path
                item_header['cookie'] = cookie_string
                item_header['content-length'] = '30'
                item_header['content-type'] = 'application/json'
                item_header['origin'] = 'https://seller.shopee.tw'
                res = conn.post(Shopee.home + path, headers=item_header,
                                json=json.loads('[{"values":[],"modelid":' + model_id + '}]'))
                save_json(res.json(), './json/items/' + model_id + '.json')

        except ValueError:
            print('Decoding JSON has failed \r\n {}'.format(res.text()))


if __name__ == '__main__':
    main()
