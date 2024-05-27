from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token
from flasgger import swag_from
from werkzeug.security import check_password_hash, generate_password_hash

# Usuários fictícios para exemplo; em uma aplicação real, use um banco de dados
users = []

class UserRegister(Resource):
    """
    ---
    post:
      tags:
        - Auth
      summary: Register a new user
      description: Registers a new user with a username and password.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                username:
                  type: string
                  description: The username of the user
                  example: "user1"
                password:
                  type: string
                  description: The password of the user
                  example: "password123"
      responses:
        201:
          description: User created successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: "User created successfully"
        400:
          description: User already exists
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: "User already exists"
    """
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, help="Username cannot be blank")
        parser.add_argument('password', required=True, help="Password cannot be blank")
        data = parser.parse_args()
        
        if any(user['username'] == data['username'] for user in users):
            return {"message": "User already exists"}, 400

        hashed_password = generate_password_hash(data['password'])
        users.append({
            'username': data['username'],
            'password': hashed_password
        })
        return {"message": "User created successfully"}, 201

class UserLogin(Resource):
    """
    ---
    post:
      tags:
        - Auth
      summary: Log in a user
      description: Logs in a user and returns a JWT access token.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                username:
                  type: string
                  description: The username of the user
                  example: "user1"
                password:
                  type: string
                  description: The password of the user
                  example: "password123"
      responses:
        200:
          description: Successful login
          content:
            application/json:
              schema:
                type: object
                properties:
                  access_token:
                    type: string
                    example: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
        401:
          description: Invalid credentials
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: "Invalid credentials"
    """
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, help="Username cannot be blank")
        parser.add_argument('password', required=True, help="Password cannot be blank")
        data = parser.parse_args()
        
        user = next((user for user in users if user['username'] == data['username']), None)
        
        if user and check_password_hash(user['password'], data['password']):
            access_token = create_access_token(identity=user['username'])
            return {"access_token": access_token}, 200
        return {"message": "Invalid credentials"}, 401
