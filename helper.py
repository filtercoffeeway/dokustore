import jwt

# Token, secret key, and algorithms
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwdWJsaWNfaWQiOiJ4VXRNZ2RSTFdrWUpPWmdaczJWRUk0aU1wYVFvNXJlVHA2YkF1eE9KTFJxZzRScmh5cSJ9.jL0_pL86JgajKr85BhfUJdOi4lmPLmFuC0kwHWE-kDo"
secret_key = "ac8fa875-146d-4567-b1cb-0da6aaaa9963"
algorithms = ["HS256"]

# Decode the JWT
decoded_token = jwt.decode(token, secret_key, algorithms=algorithms)

# Print the decoded token
print(decoded_token)