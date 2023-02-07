# API Reference

## Table APIs

- GET `/api/list/tables`
    - Returns an array of table names.
    - Response Body:
        - Type: JSON
        - Format: `[name0, name1, ...]`

- GET `/api/create/table/<table_name>`
    - Creates a new table.

- GET `/api/view/table/<table_name>`
    - Returns data in specific table.
    - Response Body:
        - Type: JSON
        - Format: `[{ key -> value, ... }, ...]`

- POST `/api/append/<table_name>`
    - Append the given data to specific table.
    - Request Body: data to append
        - Type: JSON
        - Format: `{ key -> value, ... }`

- GET `/api/delete/<table_name>/<record_id>`
    - Deletes specific record.

- POST `/api/update/<table_name>/<record_id>`
    - Updates the specific record.
    - Request Body: data to update
        - Type: JSON
        - Format: `{ key -> value, ... }`

## Backup APIs

- GET `/api/list/backups`
    - Returns an array of backup names.
    - Response Body:
        - Type: JSON
        - Format: `[name0, name1, ...]`

- GET `/api/create/backup/<backup_name>`
    - Creates a backup.

TODO: load backup
