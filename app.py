from flask import Flask, jsonify, request, render_template, Response
from collections import deque
from datetime import datetime
import time
import json
import random

app = Flask(__name__)

queues = {
    'normal': {
        'queue': deque(),
        'counter': 0
    },
    'preferencial': {
        'queue': deque(),
        'counter': 0
    }
}

called_tickets = []
last_called = None
lock = False

def generate_ticket(ticket_type):
    queues[ticket_type]['counter'] += 1
    return f"{ticket_type[0].upper()}{queues[ticket_type]['counter'] % 1000:03d}"

@app.route('/')
def index():
    return render_template('emit.html')

@app.route('/call', methods=['GET'])
def call_page():
    return render_template('call.html')

@app.route('/display', methods=['GET'])
def display_page():
    return render_template('display.html')

@app.route('/emit', methods=['POST'])
def emit_ticket():
    ticket_type = request.json['type']
    ticket_number = generate_ticket(ticket_type)
    queues[ticket_type]['queue'].append(ticket_number)
    return jsonify({'ticket': ticket_number})

@app.route('/call', methods=['POST'])
def call_ticket():
    global last_called, lock
    
    if lock:
        return jsonify({'error': 'Operação em andamento'}), 423
    
    data = request.json
    guiche = data.get('guiche')
    
    if not guiche:
        return jsonify({'error': 'Número do guichê é obrigatório'}), 400

    lock = True
    try:
        for ticket_type in ['preferencial', 'normal']:
            if queues[ticket_type]['queue']:
                next_ticket = queues[ticket_type]['queue'].popleft()
                last_called = {
                    'ticket': next_ticket,
                    'guiche': guiche,
                    'timestamp': datetime.now().isoformat()
                }
                called_tickets.append(last_called)
                return jsonify({
                    'ticket': next_ticket,
                    'guiche': guiche,
                    'remaining': sum(len(q['queue']) for q in queues.values())
                })
        
        return jsonify({'error': 'Nenhuma senha na fila'}), 404
    finally:
        lock = False

@app.route('/recall', methods=['POST'])
def recall_ticket():
    global last_called
    
    if not last_called:
        return jsonify({'error': 'Nenhuma senha para chamar novamente'}), 404
    
    data = request.json
    guiche = data.get('guiche')
    
    if not guiche:
        return jsonify({'error': 'Número do guichê é obrigatório'}), 400

    called_tickets.append(last_called.copy())
    return jsonify({
        'ticket': last_called['ticket'],
        'guiche': guiche,
        'remaining': sum(len(q['queue']) for q in queues.values())
    })

@app.route('/stream')
def stream():
    def event_stream():
        last_index = 0
        while True:
            time.sleep(0.1)
            current_index = len(called_tickets)
            if current_index > last_index:
                for i in range(last_index, current_index):
                    ticket = called_tickets[i]
                    yield f"data: {json.dumps(ticket)}\n\n"
                last_index = current_index
            else:
                yield ":keep-alive\n\n"
    return Response(event_stream(), content_type='text/event-stream')

@app.route('/remaining')
def get_remaining():
    return jsonify({'remaining': sum(len(q['queue']) for q in queues.values())})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='80', debug=True)