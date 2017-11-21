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

*extra steps for RHEL7:
    - start/stop/restart: service mysql start
    - /var/lib/mysql/mysql.sock (where socket file is)
    - nano /etc/my.cnf (may need to modify. add [mysqld] port=3306, protocol=tcp, host=127.0.0.1, skip-name-resolve  [mysql] max_allowed_packet=64M
    - restart mysql
    - run systemctl status mysqld.service
    - run journalctl -xe
	You can generate a local policy module to allow this a
          Do allow this access for now by executing:
		# ausearch -c 'mysqld' --raw | audit2allow -M my-mysql
                # semodule -i my-mysqld.pp
    - SELECT User, Host FROM mysql.user; (run in mysql)
    
2. Running jupyter notebook:
    - Install pymysql from your terminal (sudo pip install PyMySQL. If anaconda installed, launch it, go to env, click the arrow next to root, open terminal and run the commands here)
    - Install sqlalchemy from command line (sudo pip install sqlalchemy)
    - Install pandas
    - Install nltk (run python, import nltk nltk.download())
    - Install folium (conda install -c ioos folium)
    - Install mysqlconnection

