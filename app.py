from flask import Flask, render_template, request, redirect, url_for, session, flash
from tarea import Tarea

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cambiar-esta-clave-antes-de-publicar'

def obtener_tareas():
    return [Tarea.desde_diccionario(d) for d in session.get('tareas', [])]

def guardar_tareas(tareas):
    # Flask serializa diccionarios en una cookie de sesión firmada.
    session['tareas'] = [t.a_diccionario() for t in tareas]

@app.route('/')
def inicio():
    return render_template('index.html', tareas=session.get('tareas', []))

@app.route('/crear', methods=['POST'])
def crear():
    tareas = obtener_tareas()
    siguiente_id = session.get('siguiente_id', 1)
    tarea = Tarea(siguiente_id, request.form.get('titulo', ''))
    tareas.append(tarea)
    guardar_tareas(tareas)
    session['siguiente_id'] = siguiente_id + 1
    flash('Tarea añadida.', 'exito')
    return redirect(url_for('inicio'))

if __name__ == '__main__':
    app.run(debug=True)
