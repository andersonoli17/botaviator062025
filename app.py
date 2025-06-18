from flask import Flask, render_template, Response
import subprocess
import threading
import time

app = Flask(__name__)

output = []

def run_worker():
    global output
    # Chama o script AviatorApostaganha.py e redireciona a saída
    process = subprocess.Popen(['python', 'AviatorApostaganha.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Lê a saída do processo em tempo real
    for line in iter(process.stdout.readline, b''):
        output.append(line.decode('utf-8'))  # Adiciona a saída à lista
        print(line.decode('utf-8'), end="")  # Imprime no console

    process.stdout.close()
    process.wait()

@app.route('/')
def index():
    return render_template('index.html', output=output)

def generate_output():
    while True:
        if output:
            yield ''.join(output)
        time.sleep(1)  # Espera um pouco antes de verificar novamente

@app.route('/output')
def output_stream():
    return Response(generate_output(), mimetype='text/plain')

if __name__ == '__main__':
    threading.Thread(target=run_worker, daemon=True).start()  # Inicia o worker em uma thread separada
    app.run(host='0.0.0.0', port=5000)  # Inicia o servidor Flask
