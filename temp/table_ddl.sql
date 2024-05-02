-- Create a sequence
CREATE SEQUENCE user_id_seq
    START WITH 1
    INCREMENT BY 1
    NOCACHE
    NOCYCLE;

-- Create the users table with the auto-incremented id column
CREATE TABLE users (
    id NUMBER DEFAULT user_id_seq.NEXTVAL PRIMARY KEY,
    first_name VARCHAR2(255),
    last_name VARCHAR2(255),
    email VARCHAR2(255),
    phone VARCHAR2(20),
    status VARCHAR2(255),
    username VARCHAR2(255),
    password VARCHAR2(255),
    verified_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT SYSTIMESTAMP,
    updated_at TIMESTAMP,
    deactivated_at TIMESTAMP,
    CONSTRAINT unique_username UNIQUE (username),
    CONSTRAINT unique_email UNIQUE (email)
);

-- Create a sequence
CREATE SEQUENCE document_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NOCACHE
    NOCYCLE;

CREATE TABLE document_types (
  id NUMBER DEFAULT document_type_id_seq.NEXTVAL PRIMARY KEY,
  document_type VARCHAR2(255) UNIQUE,
  user_id NUMBER,
  status VARCHAR2(50),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP,
  CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id)
);


-- Create a sequence
CREATE SEQUENCE document_id_seq
    START WITH 1
    INCREMENT BY 1
    NOCACHE
    NOCYCLE;

CREATE TABLE documents (
  id NUMBER DEFAULT document_id_seq.NEXTVAL PRIMARY KEY,
  document_name VARCHAR2(255) UNIQUE,
  document_type_id INTEGER,
  user_id NUMBER,
  status VARCHAR2(100),
  file_id VARCHAR2(255),
  file_path VARCHAR2(255),
  file_size FLOAT,
  file_type VARCHAR2(50),
  due_date TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_document_type_id FOREIGN KEY (document_type_id) REFERENCES document_types(id),
  CONSTRAINT fk_document_user_id FOREIGN KEY (user_id) REFERENCES users(id)
);