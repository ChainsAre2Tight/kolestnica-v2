Here be dragons

- Routes 80
    - / - welcome page
    - /auth
        - /register
        - /login
        - /logout
    - /app - application page
    - /api
        - /auth - auth server 5020
        - /data - feed server 5010
            - /chats - returns list of chats by user and their respective encryption keys
            - /chats/users
            - /chats/<chat-id>/messages - returns list of messages within a chat
        - /ws - websocket server 5030

- Models
    - User
        - userid
        - username
        - alias
        - date of creation (/)
        - image_id (href)

        - chats
        - sessions

    - user_login
        - userid
        - login
        - password

    - session
        - init date (/)
        - uuid
        - socketid
        - refresh_token

    - chat
        - id
        - name
        - image (href)
        
        - users
        - messages

    - chat_encryption
        - id
        - key

    - message
        - id
        - body
        - timestamp

        - author


- Token
    - sessionId
    - exp