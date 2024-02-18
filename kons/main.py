from selenium import webdriver #line:1
from selenium .webdriver .chrome .service import Service as ChromeService #line:2
from webdriver_manager .chrome import ChromeDriverManager #line:4
from webdriver_manager .core .os_manager import ChromeType #line:5
from selenium .common .exceptions import WebDriverException ,NoSuchDriverException #line:7
import time #line:9
import requests #line:10
import os #line:11
import re #line:12
import base64 #line:13
from flask import Flask #line:14
import hashlib #line:15
import sys #line:16
extensionId ='ilehaonighjijnmpnagapkhpcdbhclfg'#line:18
CRX_URL ="https://clients2.google.com/service/update2/crx?response=redirect&prodversion=98.0.4758.102&acceptformat=crx2,crx3&x=id%3D~~~~%26uc&nacl_arch=x86-64"#line:19
USER_AGENT ="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"#line:20
try :#line:22
    USER =os .environ ['GRASS_USER']#line:23
    PASSW =os .environ ['GRASS_PASS']#line:24
except :#line:25
    USER =''#line:26
    PASSW =''#line:27
try :#line:29
    ALLOW_DEBUG =os .environ ['ALLOW_DEBUG']#line:30
    if ALLOW_DEBUG =='True':#line:31
        ALLOW_DEBUG =True #line:32
    else :#line:33
        ALLOW_DEBUG =False #line:34
except :#line:35
    ALLOW_DEBUG =False #line:36
if USER ==''or PASSW =='':#line:39
    print ('Please set GRASS_USER and GRASS_PASS env variables')#line:40
    exit ()#line:41
if ALLOW_DEBUG ==True :#line:43
    print ('Debugging is enabled! This will generate a screenshot and console logs on error!')#line:44
def download_extension (O00O0O000O0OO0O0O ):#line:48
    OOO00OOOOO000000O =CRX_URL .replace ("~~~~",O00O0O000O0OO0O0O )#line:49
    OO00OOOOOO00000O0 ={"User-Agent":USER_AGENT }#line:50
    O0000OOOOOOO00O00 =requests .get (OOO00OOOOO000000O ,stream =True ,headers =OO00OOOOOO00000O0 )#line:51
    with open ("grass.crx","wb")as OOOO0OOO0O0000O00 :#line:52
        for OO000OOO0O0OO00O0 in O0000OOOOOOO00O00 .iter_content (chunk_size =128 ):#line:53
            OOOO0OOO0O0000O00 .write (OO000OOO0O0OO00O0 )#line:54
    if ALLOW_DEBUG ==True :#line:55
        OO0OO00OO0OOOOOOO =hashlib .md5 (open ('grass.crx','rb').read ()).hexdigest ()#line:57
        print ('Extension MD5: '+OO0OO00OO0OOOOOOO )#line:58
def generate_error_report (O0O000000OOOOOOO0 ):#line:62
    if ALLOW_DEBUG ==False :#line:63
        return #line:64
    O0O000000OOOOOOO0 .save_screenshot ('error.png')#line:66
    O0OO00OOOO0O000O0 =O0O000000OOOOOOO0 .get_log ('browser')#line:68
    with open ('error.log','w')as OO00OOO000OO0O0O0 :#line:69
        for O00OOO0O0O00OO00O in O0OO00OOOO0O000O0 :#line:70
            OO00OOO000OO0O0O0 .write (str (O00OOO0O0O00OO00O ))#line:71
            OO00OOO000OO0O0O0 .write ('\n')#line:72
    OOOO00O0O0OO0O000 ='https://imagebin.ca/upload.php'#line:74
    O0O0O0OOOOO0O0OOO ={'file':('error.png',open ('error.png','rb'),'image/png')}#line:75
    O0OO0O00OOOOO0O00 =requests .post (OOOO00O0O0OO0O000 ,files =O0O0O0OOOOO0O0OOO )#line:76
    print (O0OO0O00OOOOO0O00 .text )#line:77
    print ('Error report generated! Provide the above information to the developer for debugging purposes.')#line:78
print ('Downloading extension...')#line:80
download_extension (extensionId )#line:81
print ('Downloaded! Installing extension and driver manager...')#line:82
options =webdriver .ChromeOptions ()#line:84
options .add_argument ("--headless=new")#line:86
options .add_argument ("--disable-dev-shm-usage")#line:87
options .add_argument ('--no-sandbox')#line:88
options .add_extension ('grass.crx')#line:90
print ('Installed! Starting...')#line:92
try :#line:93
    driver =webdriver .Chrome (options =options )#line:94
except (WebDriverException ,NoSuchDriverException )as e :#line:95
    print ('Could not start with Manager! Trying to default to manual path...')#line:96
    try :#line:97
        driver_path ="/usr/bin/chromedriver"#line:98
        service =ChromeService (executable_path =driver_path )#line:99
        driver =webdriver .Chrome (service =service ,options =options )#line:100
    except (WebDriverException ,NoSuchDriverException )as e :#line:101
        print ('Could not start with manual path! Exiting...')#line:102
        exit ()#line:103
print ('Started! Logging in...')#line:106
driver .get ('https://app.getgrass.io/')#line:107
sleep =0 #line:109
while True :#line:110
    try :#line:111
        driver .find_element ('xpath','//*[@name="user"]')#line:112
        driver .find_element ('xpath','//*[@name="password"]')#line:113
        driver .find_element ('xpath','//*[@type="submit"]')#line:114
        break #line:115
    except :#line:116
        time .sleep (1 )#line:117
        print ('Loading login form...')#line:118
        sleep +=1 #line:119
        if sleep >15 :#line:120
            print ('Could not load login form! Exiting...')#line:121
            generate_error_report (driver )#line:122
            driver .quit ()#line:123
            exit ()#line:124
user =driver .find_element ('xpath','//*[@name="user"]')#line:127
passw =driver .find_element ('xpath','//*[@name="password"]')#line:128
submit =driver .find_element ('xpath','//*[@type="submit"]')#line:129
user .send_keys (USER )#line:132
passw .send_keys (PASSW )#line:133
submit .click ()#line:134
sleep =0 #line:139
while True :#line:140
    try :#line:141
        e =driver .find_element ('xpath','//*[contains(text(), "Dashboard")]')#line:142
        break #line:143
    except :#line:144
        time .sleep (1 )#line:145
        print ('Logging in...')#line:146
        sleep +=1 #line:147
        if sleep >30 :#line:148
            print ('Could not login! Double Check your username and password! Exiting...')#line:149
            generate_error_report (driver )#line:150
            driver .quit ()#line:151
            exit ()#line:152
print ('Logged in! Waiting for connection...')#line:154
driver .get ('chrome-extension://'+extensionId +'/index.html')#line:155
sleep =0 #line:156
while True :#line:157
    try :#line:158
        driver .find_element ('xpath','//*[contains(text(), "Open dashboard")]')#line:159
        break #line:160
    except :#line:161
        time .sleep (1 )#line:162
        print ('Loading connection...')#line:163
        sleep +=1 #line:164
        if sleep >30 :#line:165
            print ('Could not load connection! Exiting...')#line:166
            generate_error_report (driver )#line:167
            driver .quit ()#line:168
            exit ()#line:169
print ('Connected! Starting API...')#line:171
app =Flask (__name__ )#line:173
@app .route ('/')#line:175
def get ():#line:176
    try :#line:177
        OOOOOO00OOOOO00OO =driver .find_element ('xpath','//*[contains(text(), "Network quality")]').text #line:178
        OOOOOO00OOOOO00OO =re .findall (r'\d+',OOOOOO00OOOOO00OO )[0 ]#line:179
    except :#line:180
        OOOOOO00OOOOO00OO =False #line:181
        print ('Could not get network quality!')#line:182
        generate_error_report (driver )#line:183
    try :#line:185
        O0O00OO0O0OO0O00O =driver .find_element ('xpath','//*[@alt="token"]')#line:186
        O0O00OO0O0OO0O00O =O0O00OO0O0OO0O00O .find_element ('xpath','following-sibling::div')#line:187
        O00OOO0OO0OOOO00O =O0O00OO0O0OO0O00O .text #line:188
    except Exception as OOOO0O0000O00OOOO :#line:189
        O00OOO0OO0OOOO00O =False #line:190
        print ('Could not get earnings!')#line:191
        generate_error_report (driver )#line:192
    try :#line:194
        OO0000OOO0OO0O000 =driver .find_elements ('xpath','//*[@class="chakra-badge"]')#line:196
        OO000OOOOO0000O00 =False #line:198
        for O0OO0O0O0OO00OO00 in OO0000OOO0OO0O000 :#line:199
            OOO00O0OO00OOOO0O =O0OO0O0O0OO00OO00 .find_element_by_xpath ('child::div').text #line:200
            if 'Connected'in OOO00O0OO00OOOO0O :#line:201
                OO000OOOOO0000O00 =True #line:202
                break #line:203
    except :#line:204
        OO000OOOOO0000O00 =False #line:205
        print ('Could not get connection status!')#line:206
        generate_error_report (driver )#line:207
    return {'connected':OO000OOOOO0000O00 ,'network_quality':OOOOOO00OOOOO00OO ,'epoch_earnings':O00OOO0OO0OOOO00O }#line:209
app .run (host ='0.0.0.0',port =80 ,debug =False )#line:212
driver .quit ()
