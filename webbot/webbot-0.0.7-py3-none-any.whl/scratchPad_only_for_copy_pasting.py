import webbot 

web = webbot.Browser() ; 
web.go_to("pythonanywhere.com/login") ; 
web.type("daedalcrafters") ; 
web.type("amazonmws" , "Password") ; 
web.click("Log in") ; 
web.click("Bash console" , classname="dashboard_recent_console") ; 

web.type("Hello") ; 
