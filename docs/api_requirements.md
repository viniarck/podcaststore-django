
## API requirements

Visiting users should be able to:

- Create a login
- Authenticate
- List all podcasts or a specific podcast
- List all tracks or a specific track
- List all tracks of a specific podcast
- List all tracks with a specific tag
- List all tags
- List all tags used in any track of a podcast
- List all tags used in a track
- List all reactions in a track

Authenticated users should be able to:

- Create, delete or update their podcasts

### General back-end requirements

- Use a relational database such as PostgreSQL
- Use a caching such as Redis to optimize podcasts resource query lookups
