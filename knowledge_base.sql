-- 1. Enable the required AI extensions
CREATE EXTENSION IF NOT EXISTS google_ml_integration CASCADE;
CREATE EXTENSION IF NOT EXISTS vector CASCADE;

-- 2. Create the table for your troubleshooting documents
CREATE TABLE IF NOT EXISTS documentation (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    issue_type TEXT,
    content TEXT,
    embedding vector(768)  -- 768 is the size for Gemini text-embeddings
);

-- 3. Create a function to search for resolutions
-- This is what your "Librarian Agent" will call
CREATE OR REPLACE FUNCTION get_solution(query_text TEXT)
RETURNS TABLE(issue_type TEXT, content TEXT, similarity FLOAT) AS $$
BEGIN
    RETURN QUERY
    SELECT d.issue_type, d.content, 1 - (d.embedding <=> google_ml.embedding('text-embedding-004', query_text)::vector) AS similarity
    FROM documentation d
    ORDER BY similarity DESC
    LIMIT 1;
END;
$$ LANGUAGE plpgsql;
