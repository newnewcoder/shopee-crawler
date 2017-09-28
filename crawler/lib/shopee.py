class Shopee:
    home = 'https://seller.shopee.tw/'

    login_page_url = 'https://seller.shopee.tw/account/signin'

    account_input_css_selector = "input[placeholder='email/ 手機號碼/ 使用者名稱']"

    password_input_css_selector = "input[placeholder='密碼']"

    login_button_xpath = "//div[contains(., '登入')][contains(@class, 'shopee-button')]"

    verify_code_input_css_selector = "input[placeholder='驗證碼']"

    verify_code_input_css_selector = "input[placeholder='驗證碼']"

    verify_button_xpath = "//div[contains(., '進行驗證')][contains(@class, 'shopee-button')]"

    general_header = {  'authority':'seller.shopee.tw',
                        'scheme':'https',
                        'accept':'application/json, text/javascript, */*; q=0.01',
                        'accept-encoding':'gzip, deflate, br',
                        'accept-language':'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4',
                        'dnt': ';',
                        'referer':'https://seller.shopee.tw/portal/product/new',
                        'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}