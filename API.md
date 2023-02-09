# API Reference

## Table APIs

- GET `/api/list/tables`
    - Returns an array of table names.
    - Response Body:
        - Type: JSON
        - Format: `[name0, name1, ...]`

- GET `/api/create/table/<table_name>`
    - Creates a new table.

- GET `/api/rename/table/<source>/<destination>`
    - Renames specific table.

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

## Export APIs

TODO:

## Import APIs

- POST `/api/import/preview`
    - Gets the import preview of uploaded files.
    - Request Body: table files
        - Type: `multipart/form-data`
    - Response Body: preview data
        - Type: JSON
        - Format: `[{ key -> value, ...}, ...]`

- POST `/api/import/records`
    - Imports the given records.
    - Request Body: records to import
        - Type: JSON

## Backup APIs

- GET `/api/list/backups`
    - Returns an array of backup names.
    - Response Body:
        - Type: JSON
        - Format: `[name0, name1, ...]`

- GET `/api/create/backup/<backup_name>`
    - Creates a backup.

- GET `/api/rename/backup/<source>/<destination>`
    - Renames specific backup.

TODO: load backup

- GET `/api/delete/backup/<backup_name>`
    - Deletes specific backup.
