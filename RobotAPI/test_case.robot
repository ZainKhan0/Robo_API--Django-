*** Settings ***
Library    SeleniumLibrary

*** Test Cases ***
Open facebook.com
    Open Browser    url=about:blank    browser=chrome
    Open Browser    url=https://www.facebook.com    browser=chrome
