import mysql.connector

app = {
    'host' : 'localhost',
    'user' : 'root',
    'password' : '',
    'database' : 'pro_psicologo',
    'port' : '3306' 
}
conexion = mysql.connector.connect(**app)
cursor = conexion.cursor()