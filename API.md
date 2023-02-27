# API Reference

## Table APIs

- GET `/api/table/list`
    - Returns an array of table names.
    - Response Body:
        - Type: JSON
        - Format: `[name0, name1, ...]`

- POST `/api/table/create/<table_name>`
    - Creates a new table.

- POST `/api/table/rename/<source>/<destination>`
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

- POST `/api/table/delete`
    - Deletes specific tables.
    - Request Body: table names
        - Type: JSON
        - Format: `[name0, name1, ...]`

TODO: add table merge

## Record APIs

- POST `/api/record/delete/<table_name>/<record_id>`
    - Deletes specific record.

- POST `/api/record/update/<table_name>/<record_id>`
    - Updates the specific record.
    - Request Body: data to update
        - Type: JSON
        - Format: `{ key -> value, ... }`

## Export APIs

- POST `/api/export/create/<level>`
    - Creates an export of specific level.
    - Query Args:
        - `encoding` -- output encoding, default: `gb2312`
        - `format` -- output format, default: `xlsx`
        - `begin_date` -- filter by `activity_end <= begin_date`
        - `end_date` -- filter by `activity_begin >= end_date`
        - `suffix_encoding` -- append encoding to filenames

- POST `/api/export/show`
    - Opens file explorer at the export folder.

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

- POST `/api/backup/create/<backup_name>`
    - Creates a backup.

- POST `/api/backup/rename/<source>/<destination>`
    - Renames specific backup.

- POST `/api/backup/load/<backup_name>`
    - Loads specific backup.

- POST `/api/backup/delete/<backup_name>`
    - Deletes specific backup.

TODO: add alias backup

## Alias APIs

- GET `/api/alias/view/<column_name>`
    - Returns specific alias lists.
    - Response Body:
        - Type: JSON
        - Format: `[{ "name": "foo", "aliases": [...] }, ...]`

- POST `/api/alias/update/<column_name>/<list_name>`
    - Updates/Creates specific alias list.
    - Request Body:
        - Type: JSON
        - Format: `[aliases...]`

- POST `/api/alias/delete/<column_name>`
    - Deletes specific alias list.
    - Request Body:
        - Type: JSON
        - Format: `[listNames...]`

## Miscellaneous

- POST `/api/close`
    - Close the backend.

TODO: add search APIs
