from mysql.connector import (connection)
import json
import datetime
import re

class WebService:

    def start(self):
        from wsgiref.simple_server import make_server

        httpd = make_server('192.168.1.4', 9000, WebService.dispatcher)
        print("Serving on port 9000...")

        # Serve until process is killed
        httpd.serve_forever()

    @classmethod
    def printLog(objclass, environ):
        fwall = open("Firewall9000.log","a")
        mstring  = "[%s - " %(datetime.datetime.today().date())
        mstring += "%s] "  %(datetime.datetime.today().time())
        mstring += "[%s]" %(environ["REMOTE_ADDR"])
        mstring += "- %s \n" %(environ["PATH_INFO"])
        fwall.write(mstring)
        fwall.flush()
        fwall.close()

    @classmethod
    def dispatcher(objclass, environ, start_response):
        if environ["REQUEST_METHOD"] <> "GET":
            status = '400 Not Found' # HTTP Status
            headers = [('Content-type', 'text/plain; charset=utf-8')] # HTTP Headers
            start_response(status, headers)
            objclass.printLog(environ)
            return ""

        found = False
        #####
        res = re.search("/PruebaService/(.*)", environ["PATH_INFO"])
        if res:
            param1    = res.groups()[0]
            trn = PruebaService()
            httpResult = trn.GET(param1, environ)
            found = True
        #####
        res = re.search("/RegisterFCMToken/(.*)/(.*)/(.*)/(.*)", environ["PATH_INFO"])
        if res:
            trn = RegisterFCMToken()
            appid = res.groups()[0]
            token = res.groups()[1]
            userid = res.groups()[2]
            urlphoto = res.groups()[3]
            httpResult = trn.GET(appid, token, userid,  urlphoto, environ)
            found = True
        #####


        if found:
            status = '200 OK' # HTTP Status
            headers = [('Content-type', 'text/plain; charset=utf-8')] # HTTP Headers
            start_response(status, headers)
            return httpResult
        else:
            status = "400 Not Found"
            strObj = "400 Not Found"
            headers = [('Content-type', 'text/plain; charset=utf-8')] # HTTP Headers
            start_response(status, headers)
            objclass.printLog(environ)
            return strObj
        return ""

    def returnError(self):
        return ""


class MySQLConnection:
    db = None

    def __init__(self, host='127.0.0.1', user='root', port=3306, passwd='Edson2018', db='Android'):
        #print host, user, port, passwd, db
        self.db = connection.MySQLConnection(host=host,user=user,port=port,passwd=passwd,database=db)        # name of the data base

    def getDatabase(self):
        return self.db
        
class RegisterFCMToken:

    def GET(self, appid, token, userid, urlphoto, environ):
        conn = MySQLConnection()
        db = conn.getDatabase()
        cur = db.cursor()
        resData = {}
        resData["ErrorCode"] = ""
        resData["ErrorDescription"] = ""
        resData["Object"] = {}
        valid = True

        hlist = {}
        if valid:
            print "APPID", appid
            print "TOKEN", token
            print "USERID", userid
            print "URLPHOTO", urlphoto
            
            data  = "INSERT INTO FirebaseToken  "
            data += "(AppId, Token, UserID, UrlPhoto) "
            data += "VALUES "
            data += "('%s', '%s', '%s', '%s') " %(appid, token,userid,urlphoto)
            res = cur.execute(data)
            data = "COMMIT "
            res = cur.execute(data)

            resData["ErrorCode"]   = ""
            resData["ErrorDescription"] = "";
            resData["Object"] = "OK";
        else:
            resData["ErrorCode"]   = "10"
            resData["ErrorDescription"] = "Invalid Request";
        strObj = "%s\n" %(json.dumps(resData))
        return strObj

class PruebaService:

    def GET(self, param1, environ):
        resData = {}
        valid = True

        if valid:
            cnt = 6
            resData[cnt] = {}
            resData[cnt]["Prueba"] = "Hola Python. Parametro %s" %(param1)
            resData[cnt]["TodoPath"] = environ["PATH_INFO"]
            resData[cnt]["SistemaOperativo"] = "Usted esta en un Sistema Operativo %s " %(environ["OS"])
            for key in environ:
                print key, environ[key]
        strObj = "%s\n" %(json.dumps(resData))
        return strObj

if __name__ == "__main__":
    app = WebService()
    app.start()
