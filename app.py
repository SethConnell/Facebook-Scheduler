from flask import Flask, render_template, url_for, session, redirect, request
from datetime import datetime
from delorean import Delorean
import pymysql.cursors, os
import pytz
app = Flask(__name__)

class DB:
    conn = None
    cursor = None

    def connect(self):
        self.conn = pymysql.connect(host="ip",
                             user="username",
                             password="password",
                             db="databasename",
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor,
                             port=3306)

    def query(self, sql, para=0):
        try:
            if para!= 0:
                if len(para) == 2:
                    listy = []
                    for i in para:
                        listy.append(i)
                    mytuple = tuple(listy)
                    para = mytuple

                cursor = self.conn.cursor()
                cursor.execute(sql, para)
            else:
                cursor = self.conn.cursor()
                cursor.execute(sql)
        except:
            self.connect()
            if para != 0:
                cursor = self.conn.cursor()
                cursor.execute(sql, para)
            else:
                cursor = self.conn.cursor()
                cursor.execute(sql)
        return cursor


# Creating new instance of DB class
db = DB()

def checkDate(year, month, day, hour, minute):
    import datetime
    try:
        newDate = datetime.datetime(year,month,day,hour,minute)
        present = datetime.now()
        if newDate > present:
            return True
        else:
            return False
    except ValueError:
        return False

# Creating a function that creates required data table.
def initTable():
    global db
    query = "CREATE TABLE IF NOT EXISTS `posts`( `datanumber` int NOT NULL AUTO_INCREMENT, `date` text NOT NULL, `content` text NOT NULL, `user` text NULL, PRIMARY KEY (datanumber)) ENGINE=MEMORY;"
    db.query(query)


@app.route('/schedule', methods = ["GET","POST"])
def schedule():
    if request.method == 'POST':
        given_timezone = request.form["timezone"]
        given_hour = request.form["hour"]
        given_minute = request.form["minute"]
        given_post = request.form["fbpost"]
        given_year = request.form["year"]
        given_day = request.form["day"]
        given_month = request.form["month"]
        if int(given_year) in range(2018, 2021) and int(given_month) in range(1,13) and int(given_day) in range(1, 32) and str(given_timezone) in pytz.all_timezones and int(given_hour) in range(1,32) and int(given_minute) in range(0,60) and given_post.replace(" ", "") != "":
            return "<h1>It worked!</h1>"
        else:
            return render_template("schedule.html")
    else:
        return render_template("schedule.html")

if __name__ == '__main__':
    app.run()
