#Noticed Mistakes
DELETE `/squirrels/{id}` status should be 200, but the server returns 204.

POST says it returns the created squirrel or a confirmation, but the server sends an empty body.

PUT says it returns the updated squirrel, but the server sends an empty body.

POST with a missing `name` or `size` closes the connection instead of returning an error response.

GET `/squirrels/1/extra` returns squirrel 1 instead of 404.

GET `/squirrels/1?view=full` returns 404 even when squirrel 1 exists.

GET `/squirrels/` and `/squirrels//1` return the squirrel list; a trailing slash on an item path is ignored.

The API guide says to edit the server to change ports, but it also supports `SQUIRREL_SERVER_PORT`.

In my notes i put a Unix-only server cleanup command that will not work on Windows.
