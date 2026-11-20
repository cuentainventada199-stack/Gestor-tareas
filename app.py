from flask import Flask, render_template, request, redirect, url_for, session, flash
from tarea import Tarea

app = Flask(__name__)
import os
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'clave-local-solo-desarrollo')

def obtener_tareas():
    return [Tarea.desde_diccionario(d) for d in session.get('tareas', [])]

def guardar_tareas(tareas):
    session['tareas'] = [t.a_diccionario() for t in tareas]

@app.route('/')
def inicio():
    tareas = session.get('tareas', [])
    return render_template('index.html', tareas=tareas, completadas=sum(t['completada'] for t in tareas))

@app.route('/crear', methods=['POST'])
def crear():
    try:
        titulo = request.form.get('titulo', '')
        tarea_nueva = Tarea(session.get('siguiente_id', 1), titulo)
    except (ValueError, TypeError) as error:
        flash(str(error), 'error')
        return redirect(url_for('inicio'))
    tareas = obtener_tareas()
    siguiente_id = session.get('siguiente_id', 1)
    tareas.append(tarea_nueva)
    guardar_tareas(tareas)
    session['siguiente_id'] = siguiente_id + 1
    flash('Tarea añadida.', 'exito')
    return redirect(url_for('inicio'))

@app.route('/alternar/<int:identificador>', methods=['POST'])
def alternar(identificador):
    tareas = obtener_tareas()
    encontrado = False
    for tarea in tareas:
        if tarea.get_id() == identificador:
            encontrado = True
            tarea.set_completada(not tarea.get_completada())
            guardar_tareas(tareas)
            break
    if not encontrado:
        flash('No existe esa tarea.', 'error')
    return redirect(url_for('inicio'))

@app.route('/eliminar/<int:identificador>', methods=['POST'])
def eliminar(identificador):
    anteriores = obtener_tareas()
    tareas = [t for t in anteriores if t.get_id() != identificador]
    if len(tareas) == len(anteriores):
        flash('No existe esa tarea.', 'error')
    else:
        guardar_tareas(tareas)
        flash('Tarea eliminada.', 'exito')
    return redirect(url_for('inicio'))

@app.route('/editar/<int:identificador>', methods=['GET', 'POST'])
def editar(identificador):
    tareas = obtener_tareas()
    tarea = next((t for t in tareas if t.get_id() == identificador), None)
    if tarea is None:
        flash('No existe esa tarea.', 'error')
        return redirect(url_for('inicio'))
    if request.method == 'POST':
        try:
            tarea.set_titulo(request.form.get('titulo', ''))
        except (ValueError, TypeError) as error:
            flash(str(error), 'error')
            return render_template('editar.html', tarea=tarea.a_diccionario()), 400
        guardar_tareas(tareas)
        flash('Tarea actualizada.', 'exito')
        return redirect(url_for('inicio'))
    return render_template('editar.html', tarea=tarea.a_diccionario())

if __name__ == '__main__':
    app.run(debug=True)
