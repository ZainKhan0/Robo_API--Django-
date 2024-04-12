*** Robot API Automation ***

1) These requirements should be full-filled Robot framework (version 7.0), Django framework (version 5.0.4).

2) Browser cookies should be enabled, in some cases not enabling the cookies causes issues.

3) Following API call format should be passed : 
	
	{
    "tests": [
        {
            "title": "Open youtube.com",
            "steps": [
                "Open Browser    url=https://www.youtube.com    browser=chrome"
            ]
        },
        {
            "title": "Open facebook.com",
            "steps": [
                "Open Browser    url=https://www.facebook.com    browser=chrome"
            ]
        }
    ]
}


*** You can add multiple operations as per the desire ***
