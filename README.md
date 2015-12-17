## BLST
BLST is a RESTful API service for managing bucket lists and their constituent items. It is built using Flask and uses JSON objects for information interchange.

#### Specificaitons
The following endpoints are accessible

| Endpoint  | Functionality  |
| --- | --- |
| POST &nbsp;&nbsp;`/auth/login`  |  Logs a user in |
| GET &nbsp;&nbsp;&nbsp;&nbsp;`/auth/logout`  |  Logs a user out |
| POST &nbsp;&nbsp;`/bucketlists/` |  Creates a new bucket list |
| GET &nbsp;&nbsp;&nbsp;`/bucketlists/`  |  Lists all the created bucket lists |
| GET &nbsp;&nbsp;&nbsp;`/bucketlists/<id>`  |  Returns single bucket list matching `<id>`|
| PUT &nbsp;&nbsp;&nbsp;`/bucketlists/<id>`  |  Update bucketlist matching `<id>` |
| DELETE &nbsp;`/bucketlists/<id>`  |  Delete bucketlist matching `<id>` |
| POST &nbsp;&nbsp;&nbsp;&nbsp;`/bucketlists/<id>/items` |  Creates a new item in bucket list with matching `<id>` |
| PUT &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`/bucketlists/<id>/items/<item_id>` |  Update item in bucket list with matching `<id>` |
| DELETE `/bucketlists/<id>/items/<item_id>` |  Delete item in bucket list with matching `<id>` |
