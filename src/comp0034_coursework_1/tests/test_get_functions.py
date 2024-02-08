def test_get_player_status_code(cilent):
    response=cilent.get('player/<code>')
    assert 