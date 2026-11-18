from app.security import hash_password, verify_password

# Original password
password = "TestPassword123!"

# Generate hash
hashed = hash_password(password)

print("Original Password:", password)
print("Hashed Password:", hashed)

# Verify correct password
print("Correct Password:", verify_password(password, hashed))

# Verify incorrect password
print("Wrong Password:", verify_password("WrongPassword", hashed))

from app.security import create_access_token

# JWT Token Test
token_data = {
    "sub": "test@example.com"
}

access_token = create_access_token(token_data)

print("\nGenerated JWT Token:")
print(access_token)

from app.security import verify_access_token

# Verify JWT Token
verified_email = verify_access_token(access_token)

print("\nJWT Verification:")
print("Verified Email:", verified_email)

# Test Invalid Token
invalid_email = verify_access_token("invalid_token")

print("Invalid Token Result:", invalid_email)