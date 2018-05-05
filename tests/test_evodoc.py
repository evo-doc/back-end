import pytest
from flask import url_for

class TestApp:
    def test_home(self, client):
        """First and best test, this just test, that Blueprint and homepage are working"""
        res = client.get(url_for('miscapi.home'))
        assert res.status_code == 200
        assert res.json == {"data": "This is evodoc backend api."}

