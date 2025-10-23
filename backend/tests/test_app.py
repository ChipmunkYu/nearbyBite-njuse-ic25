# tests/test_app.py

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from app import create_app  

def test_index_route():
    app = create_app()
    client = app.test_client()
    res = client.get('/')
    data = res.get_json()

    assert res.status_code == 200
    assert isinstance(data, dict)
    assert "message" in data
