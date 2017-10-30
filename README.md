# yelp-data-mining


1. Setting up your environment:
    - Download the sql data from https://www.yelp.com/dataset/ and put it under the folder dataset in your local repository (the associate and structures can be found here: https://www.yelp.com/dataset/documentation/sql)
    - Install PyCharm (free for students)
    - Install MySQL server (once installed, go to system settings [on mac] and make sure it's running)
    - Open terminal and cd /usr/local/mysql/bin
    - In the directory type: mysql -u root -p (change your password)
    - In the directory type: CREATE DATABASE yelp_db; (hit enter)
    - Open PyCharm -> View -> Tool Windows -> Database
    - Click the add button, Data Source, MySQL (hostname=localhost, dataname=yelp_db, user=your_desktop_login, password=set_via_terminal). Add Driver (it prompts you for this)
    - Click Test Connection, Click OK
    - Import the yelp-data-mining project into PyCharm by navigating to dataset, Right click on the yelp_db.sql file and click Run. This will take about an hour to run on your machine
    
2. Running jupyter notebook:
    - Install pymysql from your terminal (sudo pip install PyMySQL)
    - Install sqlalchemy from command line (sudo pip install sqlalchemy)
    - Install pandas
    - Install nltk

