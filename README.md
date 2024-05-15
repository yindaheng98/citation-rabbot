# citation-rabbot

A telegram bot jumping in your citation database like a rabbit!

## Index in Neo4J

fulltext index for title and abstract is necessary for `/search_by_abstract`:

```cql
CREATE FULLTEXT INDEX publication_title_fulltext_index FOR (p:Publication) ON EACH [p.title];
CREATE FULLTEXT INDEX publication_abstract_fulltext_index FOR (p:Publication) ON EACH [p.abstract];
```

For faster search, you can add text index for title:

```cql
CREATE TEXT INDEX publication_title_hash_text_index FOR (p:Publication) ON (p.title_hash);
```
