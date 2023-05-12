from flask import Flask
from flask import render_template, request, redirect
from flaskext.mysql import MySQL

app=Flask(__name__)

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

@app.route('/books')
def books():
    return render_template('site/books.html')

@app.route('/about')
def all():
    return render_template('site/about.html')

#---------------------------Rutas y menu de administrador
@app.route('/admin/')
def admin_index():
    return render_template('admin/index.html')

@app.route('/admin/login')
def admin_login():
    return render_template('admin/login.html')

#--------------------------- Funciones de BD
@app.route('/admin/books')
def admin_books():
    
    connection=mysql.connect()
    cursor=connection.cursor()
    cursor.execute("SELECT * FROM libros")
    connection.commit()
    
    data=cursor.fetchall()
    print(data)
    
    return render_template('admin/books.html', books=data)

""" Guardar Registro """
@app.route('/admin/books/save', methods=['POST'])
def admin_books_save():
    _name=request.form['txtName']
    _image=request.files['txtImage']
    _url=request.form['txtUrl']
    
    # print(_name)
    # print(_url)
    # print(_image)
    
    # sql="INSERT INTO `libros` (`id`, `nombre`, `imagen`, `url`) VALUES (NULL, 'php', 'imagen.png', 'http://php.org');"
    # sql="INSERT INTO libros VALUES(NULL,?,?,?)"
    sql="INSERT INTO libros (id, nombre, imagen, url) VALUES (NULL,%s,%s,%s);"
    
    data=_name, _image.filename, _url

    connection=mysql.connect()
    cursor=connection.cursor()
    
    cursor.execute(sql, data)
    connection.commit()
        
    return redirect('/admin/books')


@app.route('/admin/books/delete', methods=['POST'])
def admin_books_delete():
    
    _id=request.form['txtID']
    # print(_id)
    
    # connection=mysql.connect()
    # cursor=connection.cursor()
    # cursor.execute("SELECT * FROM libros WHERE id=%s", (_id))
    # connection.commit()
    
    # data=cursor.fetchall()
    # print(data)
    
    connection=mysql.connect()
    cursor=connection.cursor()
    cursor.execute("DELETE FROM libros WHERE id=%s", (_id))
    connection.commit()
    
    return redirect('/admin/books')


if __name__=='__main__':
    app.run(debug=True, port=5000)