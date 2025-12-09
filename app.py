from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Config koneksi PostgreSQL
DB_HOST = "localhost"
DB_NAME = "belajar_python"
DB_USER = "postgres"
DB_PASS = "aditt031203"  # ganti dengan password kamu

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        cursor_factory=RealDictCursor
    )
    return conn

# READ - Tampilkan semua mahasiswa
@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM mahasiswa ORDER BY id")
    mahasiswa = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', mahasiswa=mahasiswa)

# CREATE - Tambah mahasiswa
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        nama = request.form['nama']
        nim = request.form['nim']
        jurusan = request.form['jurusan']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO mahasiswa (nama, nim, jurusan) VALUES (%s, %s, %s)",
                    (nama, nim, jurusan))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add.html')

# UPDATE - Edit mahasiswa
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM mahasiswa WHERE id = %s", (id,))
    mahasiswa = cur.fetchone()
    if request.method == 'POST':
        nama = request.form['nama']
        nim = request.form['nim']
        jurusan = request.form['jurusan']
        cur.execute("UPDATE mahasiswa SET nama=%s, nim=%s, jurusan=%s WHERE id=%s",
                    (nama, nim, jurusan, id))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))
    cur.close()
    conn.close()
    return render_template('edit.html', mahasiswa=mahasiswa)

# DELETE - Hapus mahasiswa
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM mahasiswa WHERE id=%s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
