from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cambiar-esta-clave-antes-de-publicar'

@app.route('/')
def inicio():
    return render_template('index.html', tareas=[])

if __name__ == '__main__':
    app.run(debug=True)
