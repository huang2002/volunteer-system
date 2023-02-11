# API Reference

## Table APIs

- GET `/api/table/list`
    - Returns an array of table names.
    - Response Body:
        - Type: JSON
        - Format: `[name0, name1, ...]`

- GET `/api/table/create/<table_name>`
    - Creates a new table.

- GET `/api/table/rename/<source>/<destination>`
    - Renames specific table.

- GET `/api/table/view/<table_name>`
    - Returns data in specific table.
    - Response Body:
        - Type: JSON
        - Format: `[{ key -> value, ... }, ...]`

- POST `/api/table/append/<table_name>`
    - Append the given data to specific table.
    - Request Body: data to append
        - Type: JSON
        - Format: `[{ key -> value, ... }, ...]`

- GET `/api/record/delete/<table_name>/<record_id>`
    - Deletes specific record.

- POST `/api/record/update/<table_name>/<record_id>`
    - Updates the specific record.
    - Request Body: data to update
        - Type: JSON
        - Format: `{ key -> value, ... }`

- GET `/api/table/delete/<table_name>`
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

- GET `/api/backup/list`
    - Returns an array of backups.
    - Response Body:
        - Type: JSON
        - Format: `[{ "name": "foo", "tables": [...] }, ...]`

- GET `/api/backup/create/<backup_name>`
    - Creates a backup.

- GET `/api/backup/rename/<source>/<destination>`
    - Renames specific backup.

- GET `/api/backup/load/<backup_name>`
    - Loads specific backup.

- GET `/api/backup/delete/<backup_name>`
    - Deletes specific backup.

## Miscellaneous

- GET `/api/close`
    - Close the backend.
