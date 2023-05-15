from flask import Flask

# Renderizado de vistas
# Consultar peticiones y redireccionar vistas
from flask import render_template, request, redirect, session

# Consultar informacion de una imagen
from flask import send_from_directory

# Conexion y operaciones a la DB MySql
from flaskext.mysql import MySQL

# Consulta de fechas
from datetime import datetime

# Impoirtar manejo de archivos
import os

app=Flask(__name__)
app.secret_key="develoteca"

#---------------------------Conexión a MySQL
mysql=MySQL()

app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='site'
mysql.init_app(app)

#---------------------------Rutas y menu de clientes
@app.route('/')
def inicio():
    return render_template('site/index.html')

@app.route('/img/<image>')
def image(image):
    # print(image)
    return send_from_directory(os.path.join('templates/site/img'), image)

@app.route('/books')
def books():
    connection=mysql.connect()
    cursor=connection.cursor()
    cursor.execute("SELECT * FROM libros")
    connection.commit()
    data=cursor.fetchall()   
    return render_template('site/books.html', books=data)

@app.route('/about')
def all():
    return render_template('site/about.html')

#---------------------------Rutas y menu de administrador
@app.route('/admin/')
def admin_index():
    if not 'login' in session:
        return redirect('/admin/login')    
    return render_template('admin/index.html')

@app.route('/admin/login')
def admin_login():
    return render_template('admin/login.html')

@app.route('/admin/login', methods=['POST'])
def admin_login_post():
    _user=request.form['txtUser']
    _password=request.form['txtPassword']
    # print(_user)
    # print(_password)
    
    if _user=="admin" and _password=="12345":
        session['login']=True
        session['user']="Administrador"
        return redirect("/admin")        
    return render_template('admin/login.html')

@app.route('/admin/close')
def admin_login_close():
    session.clear()
    return redirect('/admin/login')
    
#--------------------------- Funciones de BD
@app.route('/admin/books')
def admin_books():
    if not 'login' in session:
        return redirect('/admin/login')
        
    connection=mysql.connect()
    cursor=connection.cursor()
    cursor.execute("SELECT * FROM libros")
    connection.commit()
    
    data=cursor.fetchall()
    # print(data)
    
    return render_template('admin/books.html', books=data)

""" Guardar Registro """
@app.route('/admin/books/save', methods=['POST'])
def admin_books_save():
    if not 'login' in session:
        return redirect('/admin/login')
    
    _name=request.form['txtName']
    _file=request.files['txtImage']
    _url=request.form['txtUrl']
    
    time=datetime.now()
    currentTime=time.strftime("%Y%H%M%S")
    if _file.filename!="":
        newFilename=currentTime+"_"+_file.filename
        _file.save("sitioweb/templates/site/img/"+newFilename)
            
    # print(_name)
    # print(_url)
    # print(_file)
    
    # sql="INSERT INTO `libros` (`id`, `nombre`, `imagen`, `url`) VALUES (NULL, 'php', 'imagen.png', 'http://php.org');"
    # sql="INSERT INTO libros VALUES(NULL,?,?,?)"
    sql="INSERT INTO libros (id, nombre, imagen, url) VALUES (NULL,%s,%s,%s);"
    
    data=_name, newFilename, _url

    connection=mysql.connect()
    cursor=connection.cursor()
    
    cursor.execute(sql, data)
    connection.commit()
        
    return redirect('/admin/books')


@app.route('/admin/books/delete', methods=['POST'])
def admin_books_delete():
    
    if not 'login' in session:
        return redirect('/admin/login')
    
    _id=request.form['txtID']
    # print(_id)
    
    connection=mysql.connect()
    cursor=connection.cursor()
    cursor.execute("SELECT imagen FROM libros WHERE id=%s", (_id))
    connection.commit()
    
    data=cursor.fetchall()
    
    # Borrar imagen del repo
    if os.path.exists("sitioweb/templates/site/img/"+str(data[0][0])):
        os.unlink("sitioweb/templates/site/img/"+str(data[0][0]))
    
    connection=mysql.connect()
    cursor=connection.cursor()
    cursor.execute("DELETE FROM libros WHERE id=%s", (_id))
    connection.commit()
    
    return redirect('/admin/books')


if __name__=='__main__':
    app.run(debug=True, port=5000)