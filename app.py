from flask import Flask, request, jsonify
from azure.storage.queue import QueueServiceClient
from flask_swagger_ui import get_swaggerui_blueprint
import os

app = Flask(__name__)

queue_name = os.getenv('AZURE_QUEUE_NAME')
connection_string = os.getenv('AZURE_QUEUE_CONNECTION_STRING')

queue_service_client = QueueServiceClient.from_connection_string(connection_string)

queue_client = queue_service_client.get_queue_client(queue_name)

# Swagger UI configuration
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Azure Queue API"
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        message_text = request.json.get('message')
        if not message_text:
            return jsonify({"error": "Message text is required"}), 400
        queue_client.send_message(message_text)
        return jsonify({"message": "Message sent successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/receive_messages', methods=['GET'])
def receive_messages():
    try:
        messages = queue_client.receive_messages(messages_per_page=10)
        result = [{"id": message.id, "content": message.content} for message in messages]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)