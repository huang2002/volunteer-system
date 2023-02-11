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

- POST `/api/append/table/<table_name>`
    - Append the given data to specific table.
    - Request Body: data to append
        - Type: JSON
        - Format: `[{ key -> value, ... }, ...]`

- GET `/api/delete/record/<table_name>/<record_id>`
    - Deletes specific record.

- POST `/api/update/record/<table_name>/<record_id>`
    - Updates the specific record.
    - Request Body: data to update
        - Type: JSON
        - Format: `{ key -> value, ... }`

- GET `/api/delete/table/<table_name>`
    - Deletes entire table.

## Export APIs

TODO:

## Import APIs

- POST `/api/import/preview`
    - Gets the import preview of uploaded files.
    - Request Body: table files
        - Type: `multipart/form-data`
        - Name of the file entries: `files[]`
    - Response Body: preview data
        - Type: JSON
        - Format: `[{ key -> value, ...}, ...]`

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

- GET `/api/load/backup/<backup_name>`
    - Loads specific backup.

- GET `/api/delete/backup/<backup_name>`
    - Deletes specific backup.
