-- Enable the pgvector extension to work with embedding vectors
create extension if not exists vector;

-- Create a table to store your memories
create table memgraph_memories (
  id uuid default gen_random_uuid() primary key,
  content text,
  embedding vector(128), -- Matching the 128 dim in memgraph_core.py mock
  tier text,
  metadata jsonb,
  created_at timestamp with time zone default timezone('utc'::text, now())
);

-- Create a function to search for memories
create or replace function match_memories (
  query_embedding vector(128),
  match_threshold float,
  match_count int
)
returns table (
  id uuid,
  content text,
  tier text,
  metadata jsonb,
  similarity float
)
language plpgsql
as $$
begin
  return query(
    select
      memgraph_memories.id,
      memgraph_memories.content,
      memgraph_memories.tier,
      memgraph_memories.metadata,
      1 - (memgraph_memories.embedding <=> query_embedding) as similarity
    from memgraph_memories
    where 1 - (memgraph_memories.embedding <=> query_embedding) > match_threshold
    order by memgraph_memories.embedding <=> query_embedding
    limit match_count
  );
end;
$$;
