# Simple HTTP File Server Specification

## Purpose

`simple_http.py` provides a local HTTP service for uploading, retrieving, and deleting files. Clients interact with it using tools such as curl.

## Running the server

The server shall run with Python 3 and require no third-party packages:

```bash
python3 simple_http.py
```

By default, it shall listen at `http://127.0.0.1:8000`. It shall support an alternative port through `--port`. Ctrl+C shall stop the server.

## File storage

- Each file shall be identified by its URL path, such as `/text.txt`.
- File contents shall be stored in memory. Uploaded files need not survive a server restart.
- Uploading or deleting a file shall not create or remove files on the host filesystem.
- The server shall preserve uploaded bytes exactly, including line breaks.

## POST: Upload a file

1. A POST request to a file path shall store the request body as that file's contents.
2. Creating a new file shall return `201 Created`.
3. Uploading to an existing file path shall replace its contents and return `200 OK`.
4. A successful response shall include a `Location` header identifying the file path and an empty response body.
5. Requests to `/`, or requests without a valid nonnegative `Content-Length`, shall return `400 Bad Request`.

### Example: Upload text.txt

Create a local file:

```bash
printf 'Hello from text.txt\n' > text.txt
```

Upload its contents:

```bash
curl -i -X POST --data-binary @text.txt http://127.0.0.1:8000/text.txt
```

If `/text.txt` does not already exist, the response shall have status `201 Created`, a `Location: /text.txt` header, and no response body. Repeating the upload shall return `200 OK`.

`--data-binary @text.txt` sends the local file's contents as the raw request body. Multipart form uploads are outside this specification.

## GET: Retrieve a file

1. A GET request for an existing file shall return `200 OK` and the exact stored contents in the response body.
2. The response shall include a `Content-Length` header matching the number of bytes returned.
3. A GET request for a nonexistent file shall return `404 Not Found`.

### Example: Retrieve text.txt

After the successful upload above:

```bash
curl -i -X GET http://127.0.0.1:8000/text.txt
```

The response shall have status `200 OK` and this body, including the final newline:

```text
Hello from text.txt
```

To download the contents into a local file:

```bash
curl -o downloaded-text.txt http://127.0.0.1:8000/text.txt
```

`downloaded-text.txt` shall contain exactly the bytes uploaded from `text.txt`.

## DELETE: Delete a file

1. The server shall implement the DELETE method.
2. A DELETE request for an existing file shall remove that file from in-memory storage and return `204 No Content` with no response body.
3. After successful deletion, a GET request for that path shall return `404 Not Found`.
4. A DELETE request for a nonexistent file shall return `404 Not Found`.
5. Deleting one file shall not change any other stored file.

### Example: Delete text.txt

After uploading `/text.txt`:

```bash
curl -i -X DELETE http://127.0.0.1:8000/text.txt
```

Expected status: `204 No Content`, with no response body.

Then request the file again:

```bash
curl -i -X GET http://127.0.0.1:8000/text.txt
```

Expected status: `404 Not Found`. The original contents shall no longer be accessible.

Repeating the DELETE request shall also return `404 Not Found`.

## Acceptance sequence

Starting with no `/text.txt` stored:

| Request | Expected status | Expected result |
| --- | --- | --- |
| POST `/text.txt` with file contents | 201 | File is stored. |
| GET `/text.txt` | 200 | Body matches the uploaded bytes. |
| POST `/text.txt` with new contents | 200 | File contents are replaced. |
| GET `/text.txt` | 200 | Body matches the replacement bytes. |
| DELETE `/text.txt` | 204 | File is removed. |
| GET `/text.txt` | 404 | File is unavailable. |
| DELETE `/text.txt` | 404 | File remains unavailable. |

The `-i` option in the examples displays response headers, including the HTTP status, alongside any response body.
