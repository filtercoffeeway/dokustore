INSERT INTO users (first_name, last_name, email, phone, status)
VALUES ('poorna', 'chandrika', 'poorna@example.com', 1234567890, 'active');

--drop table users;

--drop table document_types;

select * from users;

select * from document_types;

SELECT id
                                ,document_type
                                ,user_id
                                ,status
                                ,created_at
                                ,updated_at
                            FROM document_types
                            WHERE user_id = 3 ORDER BY LOWER(document_type) ASC;