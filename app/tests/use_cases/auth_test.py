from app.use_cases.auth import generate_jwt, decode_jwt

def test_generate_jwt():
  data = {'id': 1, 'username': "usermax", 'email': "email@email", "role_id": 1}
  
  token = generate_jwt(data)
  
  assert token is not None
  
  decoded = decode_jwt(token)
    
  assert 'data' in decoded
  assert 'exp' in decoded
  