instructions = [
    'SET FOREIGN_KEY_CHECKS=0;',
    'DROP TABLE IF EXISTS comments;',
    'DROP TABLE IF EXISTS users;',
    'SET FOREIGN_KEY_CHECKS=0;',
    """
        CREATE TABLE users(
            id INT PRIMARY KEY AUTO_INCREMENT,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(200) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL
        )
    """,
    """
        CREATE TABLE comments(
            id INT PRIMARY KEY AUTO_INCREMENT,
            created_by INT,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            opinion TEXT NOT NULL,
            FOREIGN KEY (created_by) REFERENCES users (id) 
            ON UPDATE CASCADE
            ON DELETE SET NULL
        )
    """
]
