import pytest
from flask import json
from app import app, queue_client


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_send_message(client):
    response = client.post('/send_message', json={"message": "Test message"})
    assert response.status_code == 200
    assert response.json["message"] == "Message sent successfully"


def test_receive_messages(client):
    # Ensure the queue has at least one message
    queue_client.send_message("Test message for receiving")

    response = client.get('/receive_messages')
    assert response.status_code == 200
    assert len(response.json) > 0
    assert "id" in response.json[0]
    assert "content" in response.json[0]