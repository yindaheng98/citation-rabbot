# citation-rabbot

A telegram bot jumping in your citation database like a rabbit!

## Index in Neo4J

For faster search, you can add text index for title:

```cql
CREATE TEXT INDEX publication_title_hash_text_index FOR (p:Publication) ON (p.title_hash);
```
