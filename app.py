from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Dicionário para armazenar os dados dos dispositivos
# Estrutura: { "device1": {"contador": valor, "temperatura": valor, "timestamp": datetime} }
devices_data = {}

# Página inicial com a tabela de dispositivos
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint para receber dados de dispositivos via POST em JSON
@app.route('/data', methods=['POST'])
def update_device():
    data = request.get_json()
    print(data)
    device_id = data.get("id")
    contador = data.get("contador")
    temperatura = data.get("tempAmbiente")

    if device_id and contador is not None and temperatura is not None:
        # Atualiza o dispositivo com os dados recebidos
        devices_data[device_id] = {
            "contador": contador,
            "temperatura": temperatura,
            "timestamp": datetime.now()
        }
        return jsonify({"status": "success", "message": "Dados atualizados com sucesso"}), 200
    else:
        return jsonify({"status": "error", "message": "Dados inválidos"}), 400

# Endpoint para fornecer a lista de dispositivos e o último valor de contador
@app.route('/devices')
def get_devices():
    return jsonify(devices_data)

# Página para gráficos específicos de um dispositivo
@app.route('/device/<device_id>')
def device_page(device_id):
    if device_id not in devices_data:
        return "Dispositivo não encontrado", 404
    return render_template('device.html')

# Endpoint para fornecer dados específicos de um dispositivo (contador e temperatura)
@app.route('/device_data/<device_id>')
def get_device_data(device_id):
    if device_id in devices_data:
        return jsonify(devices_data[device_id])
    else:
        return jsonify({"error": "Dispositivo não encontrado"}), 404

if __name__ == '__main__':
    app.run(host='192.168.115.253')
