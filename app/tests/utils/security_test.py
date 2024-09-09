from app.utils.security import encrypt_password, verify_password

def test_encrypt_password():
  password = "mysecretpassword"
  hashed_password = encrypt_password(password)
  
  assert password != hashed_password
  assert verify_password(password, hashed_password) is True

def test_wrong_verify_password():
  password = "mysecretpassword"
  hashed_password = encrypt_password(password)
  
  assert password != hashed_password
  assert verify_password("wrongpassword", hashed_password) is False 
