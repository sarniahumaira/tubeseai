from database import *
from flask import Flask, request, jsonify, make_response, render_template, redirect
import requests
import json

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def searchProduk():
    if request.method == "POST":
        nama_produk = request.form.get("nama_produk")
        sql = f"SELECT * FROM produk WHERE produk.nama LIKE '%{nama_produk}%'"
        data = getData(query=sql)
        if data:
            return render_template('show_produk.html', produk=data[0])
        else:
            return render_template('show_produk.html', produk=None)
    return render_template('search.html')

@app.route("/produk/<id>", methods=["GET"])
def getProduk(id):
    sql = f"SELECT * FROM produk WHERE produk.id = {id}"
    data = getData(query=sql)
    if data is not None:
        return make_response(
            jsonify({
                "status": 200,
                "message": f"query berhasil, id produk {id} terdaftar",
                "result": {
                    "id_penjual": data[0][1],
                    "harga": data[0][2],
                    "berat": data[0][3],
                    "nama_produk": data[0][4],
                    "gambar_produk": data[0][5]
                }
            })
        )
    else:
        return make_response(
            jsonify({
                "status": 404,
                "message": f"query gagal, id produk {id} tidak terdaftar"
            })
        )

@app.route("/penjual/<id>", methods=["GET"])
def getKotaPenjual(id):
    sql = f"SELECT id_kota FROM `penjual` WHERE penjual.id = {id}"
    data = getData(query=sql)
    if data is not None:
        return make_response(
            jsonify({
                "status": 200,
                "message": f"query berhasil, id penjual {id} terdaftar",
                "result": {
                    "id_kota": data[0][0]
                }
            })
        )
    else:
        return make_response(
            jsonify({
                "status": 404,
                "message": f"query gagal, id penjual {id} tidak terdaftar"
            })
        )

@app.route("/show_produk/<id>", methods=["GET"])
def showProduk(id):
    sql = f"SELECT * FROM produk WHERE produk.id = {id}"
    data = getData(query=sql)
    if data is not None:
        return render_template('show_produk.html', produk=data[0])
    else:
        return make_response(
            jsonify({
                "status": 404,
                "message": f"query gagal, id produk {id} tidak terdaftar"
            })
        )

@app.route("/show_penjual/<id>", methods=["GET"])
def showPenjual(id):
    sql = f"SELECT id_kota FROM `penjual` WHERE penjual.id = {id}"
    data = getData(query=sql)
    if data is not None:
        return render_template('show_penjual.html', penjual=data[0])
    else:
        return make_response(
            jsonify({
                "status": 404,
                "message": f"query gagal, id penjual {id} tidak terdaftar"
            })
        )

if __name__ == "__main__":
    app.run(port=5002, debug=True)
