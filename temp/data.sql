drop table users;

drop table document_types;

drop table documents;

-----

select * from users;

select * from document_types;


select * from documents;

----
delete from documents;

delete from document_types;

delete from users;

--

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