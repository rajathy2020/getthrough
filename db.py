import pymysql
import pymysql.cursors

conn = pymysql.connect(
                    host="rajattest2.mysql.database.azure.com",
                    user="adminrajattest",
                    password="Rajatccna1990@",
                    database="getthrough",
                    ssl={'ca': '/var/www/html/DigiCertGlobalRootCA.crt.pem'}
                )
                




