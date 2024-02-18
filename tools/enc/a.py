from flask import Flask, request, jsonify
from datetime import datetime
import sqlite3

app = Flask(__name__)

# 创建 SQLite 数据库
def create_table():
    conn = sqlite3.connect('encrypted_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS data
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, input TEXT, key TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()

# 将加密数据存储到数据库
def store_data(input_data, key):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect('encrypted_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO data (input, key, timestamp) VALUES (?, ?, ?)", (input_data, key, timestamp))
    conn.commit()
    conn.close()

# 从数据库中获取所有数据
def get_all_data():
    conn = sqlite3.connect('encrypted_data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM data")
    data = [{'id': row[0], 'input': row[1], 'key': row[2], 'timestamp': row[3]} for row in c.fetchall()]
    conn.close()
    return data

create_table()

@app.route('/encrypt', methods=['GET'])
def encrypt_data():
    input_data = request.args.get('input')
    key = request.args.get('key')

    store_data(input_data, key)
    return '{message:"信息无风险",ok:"1"}'

@app.route('/all_data', methods=['GET'])
def get_all_encrypted_data():
    data = get_all_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8001,debug=True)