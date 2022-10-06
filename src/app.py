
from re import template
from flask import Flask, redirect, render_template, request, session, url_for
from conexion import *

app = Flask(__name__)
app.secret_key = 'id_usuario'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/cliente.html')
def cliente():

    return render_template('cliente.html')


@app.route('/editarcita.html')
def editac():
    return render_template('editarcita.html')


@app.route('/admin.html')
def admin():
    return render_template('admin.html')


@app.route('/citascliente.html')
def citascliente():
    return render_template('citascliente.html')


@app.route('/citaspsicologo.html')
def citaspsicologo():
    return render_template('citaspsicologo.html')


@app.route('/login.html')
def login():
    return render_template('login.html')


@app.route('/psicologo.html')
def psicologo():

    return render_template('psicologo.html')


@app.route('/registro.html')
def registro():
    return render_template('registro.html')


@app.route('/perfil.html')
def per():
    return render_template('perfil.html')


@app.route('/perfilpsico.html')
def perps():
    return render_template('perfil_psico.html')


@app.route('/perfiladmin.html')
def perad():
    return render_template('perfil_admin.html')


@app.route('/registrousu', methods=['GET', 'POST'])
def registrousu():
    print("entro")

    if request.method == 'POST':
        cedula = request.form['cedula']
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        genero = request.form['genero']
        email = request.form['email']
        password = request.form['password']
        role = request.form['txt_role']

        sqlInsertar = "insert into tipo_cliente(id, sexo, nombres, apellido, correo, contraseña, id_rol)values(%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlInsertar, (cedula, genero, nombres,
                                     apellidos, email, password, role))

        cursor.execute(
            "insert into login select id, correo, contraseña, id_rol from tipo_cliente")

        if (role == "1"):
            print("entro")
            fecha_n = request.form['fechan']
            hoja = request.form['hoja']
            sqlInsertar = "insert into psicologo(id_psico,fecha_nacimiento,hoja_vida)values(%s,%s,%s)"
            cursor.execute(sqlInsertar, (cedula, fecha_n, hoja))
            conexion.commit()

            print(cursor)

        if (role == "2"):
            estado = request.form['estado_civil']
            profesion = request.form['profesion']
            tell = request.form['telefono']
            sqlInsertar = "insert into cliente(id_cliente, estado_civil, profesion,telefono)values(%s,%s,%s,%s)"
            cursor.execute(sqlInsertar, (cedula, estado, profesion, tell))
            conexion.commit()

    return redirect(url_for("index"))

    # cursor.execute('select * from tipo_cliente where id = %s', (cedula,))
    # account = cursor.fetchone()
    # # If account exists show error and validation checks
    # if account:
    #     msg = 'la cedula ya existe!'

    # elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
    #     msg = 'Dirección de correo electrónico no válida!'

    # elif not re.match(r'[A-Za-z0-9]+', password):
    #     msg = 'contraseña de usuario debe contener solo caracteres y números!'

    # elif not cedula or not nombres or not apellidos or not genero or not email or not password or not role :
    #     msg = 'porfavor complete el formulario!'

    # return render_template('/registro.html', msg=msg)


@app.route('/login', methods=['GET', 'POST'])
def loginu():
    msg = ''

    if request.method == 'POST':
        correo = request.form['correos']
        con = request.form['contraseñas']
        sele = request.form['role']

        sqlConsulta = (
            'select * from tipo_cliente where correo= %s and contraseña= %s and id_rol=%s')
        cursor.execute(sqlConsulta, (correo, con, sele))
        resultados = cursor.fetchone()
        if resultados:
            session['loggedin'] = True
            session['id'] = resultados[0]
            session['sexo'] = resultados[1]
            session['nombres'] = resultados[2]
            session['apellido'] = resultados[3]
            session['correos'] = resultados[4]
            session['contraseñas'] = resultados[5]
            session['id_rol'] = resultados[6]

            # session['rol'] = resultados['rol']
            if (sele == '1'):
                return redirect(url_for("psicolog"))
            if (sele == '2'):
                return redirect(url_for("clientelog"))
            if (sele == '3'):
                return redirect(url_for('adminlog'))

        else:

            msg = "usuario o contraseña incorrecto"

    return render_template('/index.html', msg=msg)


@app.route('/psico', methods=['GET', 'POST'])
def psicolog():

    if 'loggedin' in session:
        cursor.execute("select id_cita from citas ")
        pss = cursor.fetchall()
        pssl = pss[0]
        Correos = session['correos']
        print(Correos)
        cursor.execute(f"select id from tipo_cliente where correo='{Correos}'")
        id = cursor.fetchone()

        print(type(id))
        ide = int(id[0])
        print(type(ide))
        cursor.execute(f"SELECT * FROM historial  ")

        usuario = cursor.fetchall()
        conexion.commit()

        return render_template('/psicologo.html', correos=session['correos'], datosh=usuario, verps=pssl)

    return redirect(url_for('index'))


@app.route('/cliente', methods=['GET', 'POST'])
def clientelog():

    if 'loggedin' in session:
        Correos = session['correos']
        print(Correos)
        cursor.execute(f"select id from tipo_cliente where correo='{Correos}'")
        id = cursor.fetchone()

        print(type(id))
        ide = int(id[0])
        print(type(ide))

        cursor.execute(
            f'SELECT * FROM historial where id_cliente={ide}')
        usuario = cursor.fetchall()
        conexion.commit()

        return render_template('/cliente.html', correos=session['correos'],datosh=usuario)

    return redirect(url_for('index'))


@app.route('/admin ', methods=['GET', 'POST'])
def adminlog():

    if 'loggedin' in session:

        return render_template('/admin.html', correos=session['correos'])

    return redirect(url_for('index'))


@app.route('/perfil', methods=['GET', 'POST'])
def perfil():

    if 'loggedin' in session:

        cursor.execute(
            'select * from tipo_cliente where id = %s', (session['id'],))
        resultper = cursor.fetchone()
        return render_template('/perfil.html', resultp=resultper)
    return redirect(url_for({'index'}))


@app.route('/logout')
def logout():

    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('sexo', None)
    session.pop('nombres', None)
    session.pop('apellido', None)
    session.pop('correos', None)
    session.pop('contraseñas', None)
    return redirect(url_for('index'))


@app.route('/registrocita', methods=['GET', 'POST'])
def registrocita():
    if request.method == 'POST':
        cedula = request.form['cedula']
        cita = request.form['cita']
        fechac = request.form['fecha']

        sqlInsertar = "insert into citas( id_cliente, id_psicologo,fecha)values(%s,%s,%s)"
        cursor.execute(sqlInsertar, (cedula, cita, fechac))

    return redirect(url_for("datoscitas"))


@app.route('/registrocitapsico', methods=['GET', 'POST'])
def registrocitapp():
    if request.method == 'POST':
        cedulas = request.form['cedulas']
        citas = request.form['citas']
        fechacs = request.form['fechas']

        sqlInsertar = "insert into citas( id_cliente, id_psicologo,fecha)values(%s,%s,%s)"
        cursor.execute(sqlInsertar, (cedulas, citas, fechacs))

    return redirect(url_for("datoscitasp"))


@app.route('/registrohisto', methods=['GET', 'POST'])
def registrohisto():
    if request.method == 'POST':
        idcita = request.form['idcita']
        cedulas = request.form['cedula']
        motivo = request.form['motivo']
        habitos = request.form['habitos']
        compor = request.form['comportamiento']
        segui = request.form['seguimiento']
        alergia = request.form['alergias']
        trata = request.form['tratamiento']

        sqlInsertar = "insert into historial(id_cita,id_cliente,motivo,seguimiento,tratamiento,comportamiento,habitos,alergias)values(%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sqlInsertar, (idcita, cedulas, motivo,
                       segui, trata, compor, habitos, alergia))
        conexion.commit()

    return redirect(url_for("psicolog"))


# @app.route('/datoshh')
# def datosh():

#     cursor.execute("select id_cita from citas ")
#     pss = cursor.fetchall()
#     pssl = pss

#     # Correos = session['correos']
#     # print(Correos)
#     # cursor.execute(f"select id from tipo_cliente where correo='{Correos}'")
#     # id = cursor.fetchone()

#     # print(type(id))
#     # ide = int(id[0])
#     # print(type(ide))
#     # cursor.execute(f"SELECT * FROM citas where id_cita={ide} ")

#     # usuario = cursor.fetchall()
#     # conexion.commit()

#     return render_template('psicologo.html', verps=pssl)

@app.route('/datosusuarios')
def datosusuarios():

    cursor.execute('SELECT * FROM tipo_cliente')
    usuario = cursor.fetchall()
    conexion.commit()

    return render_template('admin.html', datostablausu=usuario)


@app.route('/datoscita')
def datoscitas():

    cursor.execute("select id_psico from psicologo ")
    pss = cursor.fetchall()
    pssl = tuple(pss)[0]

    # for x in pssl:
    #    pss[x]

    # cursor.execute("select nombres from tipo_cliente where id=%s"(pssl,))
    # pn = cursor.fetchall()

    Correos = session['correos']
    print(Correos)
    cursor.execute(f"select id from tipo_cliente where correo='{Correos}'")
    id = cursor.fetchone()

    print(type(id))
    ide = int(id[0])
    print(type(ide))
    cursor.execute(f"SELECT * FROM citas where id_cliente={ide} ")

    usuario = cursor.fetchall()
    conexion.commit()

    return render_template('citascliente.html', datoscita=usuario, verps=pssl)


@app.route('/datoscitapsico')
def datoscitasp():

    cursor.execute("select id_cliente from cliente ")
    pss = cursor.fetchall()
    pssl = tuple(pss)[0]

    # for x in pssl:
    #    pss[x]

    # cursor.execute("select nombres from tipo_cliente where id=%s"(pssl,))
    # pn = cursor.fetchall()

    Correos = session['correos']
    print(Correos)
    cursor.execute(f"select id from tipo_cliente where correo='{Correos}'")
    id = cursor.fetchone()

    print(type(id))
    ide = int(id[0])
    print(type(ide))
    cursor.execute(f"SELECT * FROM citas where id_psicologo={ide} ")

    usuario = cursor.fetchall()
    conexion.commit()

    return render_template('citaspsicologo.html', datoscitapsico=usuario, verpsico=pssl)
# @app.route('/edit/<cita.1>', methods=['POST', 'GET'])
# def get_contact(id_cita):

#     cursor.execute('SELECT * FROM citas WHERE id_cita = %s', (id_cita))
#     data = cursor.fetchall()

#     print(data[0])
#     return render_template('/editarcita.html', contact=data[0])

# @app.route('/datoscc')
# def datoscc():

#     # cursor.execute(
#     #     'select id_cliente from cliente')
#     # c = cursor.fetchall()

#     cursor.execute(
#         f'select id_psico from psicologo ')
#     ps = cursor.fetchall()

#     pss=ps

#     # cursor.execute(

#     #     f"select nombres from tipo_cliente where id={pss}")
#     # pn = cursor.fetchall()

#     conexion.commit()
#     return render_template('citascliente.html',verps=pss)


@app.route('/clientett')
def datosusclih():
    Correos = session['correos']
    print(Correos)
    cursor.execute(f"select id from tipo_cliente where correo='{Correos}'")
    id = cursor.fetchone()

    print(type(id))
    ide = int(id[0])
    print(type(ide))

    cursor.execute(
        f'SELECT id_cliente, id_cita, motivo FROM historial where id_cliente={ide}')
    usuario = cursor.fetchall()
    conexion.commit()

    return render_template('cliente.html', datostablau=usuario)


#   if request.method == 'POST':
if __name__ == '__main__':
    app.run(debug=True, port=5000)
