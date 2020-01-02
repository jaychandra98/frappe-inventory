from flask import Flask, abort,render_template
from flask import request
from flask import jsonify
from flask_cors import CORS, cross_origin
import json
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="chandra",
    database="invent"
)
cur = mydb.cursor()

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/addProduct', methods=['POST'])
def addProduct():
    req = request.get_json()
    cur.execute("INSERT INTO Product(product_name) values(%s)",
                (req["name"]))
    mydb.commit()
    return getProduct()


@app.route('/getProduct', methods=['POST'])
def getProduct():
    cur.execute("SELECT * FROM product")
    res = cur.fetchall()
    mydb.commit()
    jsonArr = []

    for i in res:
        jsonArr.append({"id": i[0], "name": i[1], "quantity": i[2]})
    jsonRes = {}
    jsonRes["products"] = jsonArr
    return jsonify(jsonRes)


@app.route('/editProduct', methods=['POST'])
def editProduct():
    req = request.get_json()
    cur.execute("UPDATE Product set product_name = %s, quantity = %s where product_id = %s",
                (req["name"], req["quantity"], req["id"]))
    mydb.commit()
    return getProduct()


@app.route('/addLocation', methods=['POST'])
def addLocation():
    req = request.get_json()
    cur.execute("INSERT INTO location(location_name) values(%s)",
                (req["name"],))
    mydb.commit()
    return getLocation()


@app.route('/getLocation', methods=['POST'])
def getLocation():
    cur.execute("SELECT * FROM location")
    res = cur.fetchall()
    mydb.commit()
    jsonArr = []
    for i in res:
        jsonArr.append({"id": i[0], "name": i[1]})
    jsonRes = {}
    jsonRes["locations"] = jsonArr
    return jsonify(jsonRes)


@app.route('/editLocation', methods=['POST'], endpoint='editLocation')
def editLocation():
    req = request.get_json()
    cur.execute("UPDATE location set location_name = %s where location_id = %s",
                (req["name"], req["id"]))
    mydb.commit()
    return getLocation()


@app.route('/move/getProduct', methods=['POST'], endpoint='move_getProduct')
def move_getProduct():
    req = request.get_json()
    cur.execute(
        """SELECT TWO.product_id,Product.product_name,ifnull(TWO.got_quantity,0)-ifnull(ONE.given_quantity,0) as quantity from
            (SELECT product_id,m1.from_loc as from_loc,sum(m1.quantity) as given_quantity from movement as m1 where from_loc=%s  group by m1.product_id) as ONE
            RIGHT JOIN
            (SELECT product_id, m2.to_loc as to_loc,sum(m2.quantity) as got_quantity from movement as m2 where to_loc=%s group by m2.product_id) as TWO
            on ONE.product_id=TWO.product_id, Product where Product.product_id = TWO.product_id;
        """, (int(req["location"]), int(req["location"])))
    res = cur.fetchall()
    mydb.commit()
    jsonArr = []
    print(res)
    for i in res:
        jsonArr.append({"id": i[0], "name": i[1], "quantity": str(i[2])})
    jsonRes = {}
    jsonRes["products"] = jsonArr
    return jsonify(jsonRes)


def move_getProduct(location):
    # 367 character query :")
    cur.execute("""SELECT TWO.product_id,Product.product_name,ifnull(TWO.got_quantity,0)-ifnull(ONE.given_quantity,0) as quantity from
            (SELECT product_id,m1.from_loc as from_loc,sum(m1.quantity) as given_quantity from movement as m1 where from_loc=%s  group by m1.product_id) as ONE
            RIGHT JOIN
            (SELECT product_id, m2.to_loc as to_loc,sum(m2.quantity) as got_quantity from movement as m2 where to_loc=%s group by m2.product_id) as TWO
            on ONE.product_id=TWO.product_id, Product where Product.product_id = TWO.product_id; """, (int(location), int(location)))
    res = cur.fetchall()
    mydb.commit()
    jsonArr = []
    # print(res)
    for i in res:
        jsonArr.append({"id": i[0], "name": i[1], "quantity": int(i[2])})
    jsonRes = {}
    jsonRes["products"] = jsonArr
    # print(jsonRes)
    return jsonRes


@app.route('/move/import', methods=['POST'])
def importProduct():
    req = request.get_json()
    # print(req)
    cur.execute("INSERT INTO movement(to_loc, product_id, quantity) values(%s,%s,%s)", (int(
        req["location"]), int(req["product"]), int(req["quantity"])))
    mydb.commit()
    return jsonify(move_getProduct(req["location"]))


@app.route('/move/export', methods=['POST'])
def exportProduct():
    req = request.get_json()
    if checkProduct(req["location"], req["product"], req["quantity"]):
        cur.execute("INSERT INTO movement(from_loc, product_id, quantity) values(%s,%s,%s)", (int(
            req["location"]), int(req["product"]), int(req["quantity"])))
        mydb.commit()
        return jsonify(move_getProduct(req["location"]))
    return abort(403)


@app.route('/move/movement', methods=['POST'])
def moveProduct():
    req = request.get_json()

    if checkProduct(req["from"], req["product"], req["quantity"]):
        print("mera h?   " + str(req))
        cur.execute("INSERT INTO movement(from_loc, to_loc, product_id, quantity) values(%s,%s,%s,%s)", (int(
            req["from"]), int(req["to"]), int(req["product"]), int(req["quantity"])))
        mydb.commit()
        print("mera h?   " + str(move_getProduct(req["to"])))

        return jsonify(move_getProduct(req["to"]))
    return abort(403)


def checkProduct(location, product, quantity):
    # print(move_getProduct(location))
    list = move_getProduct(location)["products"]
    # print(list)
    # print(location, product, quantity)
    for i in list:
        if i["id"] == product and int(i["quantity"]) >= int(quantity):
            print(i["id"], i["quantity"], quantity)
            return True
    return False


@app.route('/', methods=['GET'])
def prod():
    return render_template("products.html")


@app.route('/movements', methods=['GET'])
def move():
    return render_template("movement.html")


@app.route('/locations', methods=['GET'])
def loc():
    return render_template("location.html")





@app.route('/getcrashlocs', methods=['POST'])
def crash():
    req = request.get_json()
    print(req["name"])
    query="SELECT location_name FROM location WHERE location_name NOT LIKE %s"
    cur.execute(query,("%" + req["name"] + "%",))
    res = cur.fetchall()
    mydb.commit()
    jsonRes =[]
    for i in res:
        jsonRes.append({"location" :i[0]})
    dic={}
    dic["locs"]=jsonRes
    return jsonify(dic)

@app.route('/getcrashids', methods=['POST'])
def crashlocid():
    req = request.get_json()
    print(req["id"])
    cur.execute("SELECT location_id,location_name FROM location WHERE NOT location_id=%s",(req['id'],))
    res = cur.fetchall()
    mydb.commit()
    jsonRes =[]
    for i in res:
        jsonRes.append({"id" :i[0],"name" :i[1]})
    jic={}
    jic["locs"]=jsonRes
    return jsonify(jic)

@app.route('/crash', methods=['GET'])
def getLocs():
    cur.execute("SELECT location_id,location_name FROM location ")
    res=cur.fetchall()
    mydb.commit()
    jsonRes =[]
    for i in res:
        jsonRes.append({"location_id":i[0],"location_name":i[1]})
    sic={}
    sic["locs"]=jsonRes
    return jsonify(sic)



if __name__ == '__main__':
    app.run(debug=True)
