INSERT INTO users (first_name, last_name, email, phone, status)
VALUES ('poorna', 'chandrika', 'poorna@example.com', 1234567890, 'active');

--drop table users;

--drop table document_types;

drop table documents;

drop constraint fk_document_type_id;

ALTER TABLE documents
DROP CONSTRAINT fk_document_type_id;

select * from users;

select * from document_types;


select * from documents;

delete from documents;

SELECT id
                                ,document_type
                                ,user_id
                                ,status
                                ,created_at
                                ,updated_at
                            FROM document_types
                            WHERE user_id = 3 ORDER BY LOWER(document_type) ASC;
                            
                            
SELECT  COUNT(*) AS total_documents,
                                    SUM(file_size) AS total_file_size,
                                    SUM(CASE WHEN due_date < SYSDATE THEN 1 ELSE 0 END) AS documents_past_due
                            FROM documents
                           WHERE user_id = 9;