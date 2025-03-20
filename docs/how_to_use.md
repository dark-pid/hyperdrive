# Using the Hyperdrive API

This document explains how to use the API to load data via a POST request.

## Endpoint

* `POST http://apiurl/load`

## Content Type

* `application/json`

## Request Body (JSON)
```json
    {
      "dnam_pk": "0x9f2551016c584a21bafa4b7c4e1a3facc9720aec430748663062a308dd4bb337",
      "items": [
        {
          "oai_id": "1",
          "url": "http://ibict.br/a1"
        },
        {
          "oai_id": "2",
          "url": "http://ibict.br/a2"
        },
        {
          "oai_id": "n",
          "url": "http://ibict.br/an"
        }
      ]
    }
```

**Parameters**

* `dnam_pk`: Private key of the authority. For more information, please refer to the DARK App documentation or the main page.

* `items`: A list of objects, where each object represents an item to be loaded.
    * `oai_id`: Unique identifier of the item.
    * `url`: URL of the item.

## Code Examples

###   JavaScript (Node.js)
```js
    const axios = require('axios');

    const data = {
      "dnam_pk": "0x9f255155016c584a21bafa4b7c4e1a3facccccaec430748663062a308dd4bb337",
      "items": [
        { "oai_id": "1", "url": "http://ibict.br/a1" },
        { "oai_id": "2", "url": "http://ibict.br/a2" },
        { "oai_id": "3", "url": "http://ibict.br/a3" },
        { "oai_id": "4", "url": "http://ibict.br/a4" },
        { "oai_id": "5", "url": "http://ibict.br/a5" },
        { "oai_id": "6", "url": "http://ibict.br/a6" },
        { "oai_id": "7", "url": "http://ibict.br/a7" },
        { "oai_id": "8", "url": "http://ibict.br/a8" },
        { "oai_id": "9", "url": "http://ibict.br/a9" },
        { "oai_id": "10", "url": "http://ibict.br/a10" }
      ]
    };

    axios.post('{{apiurl}}/load', data, {
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(response => {
      console.log(response.data);
    })
    .catch(error => {
      console.error(error);
    });
```
###   Python
```python
    import requests
    import json

    url = '{{apiurl}}/load'
    data = {
      "dnam_pk": "0x955f2551016c584a21bafa4b7c4e1a3facccccaec430748663062a308dd4bb337",
      "items": [
        { "oai_id": "1", "url": "http://ibict.br/a1" },
        { "oai_id": "2", "url": "http://ibict.br/a2" },
        { "oai_id": "3", "url": "http://ibict.br/a3" },
        { "oai_id": "4", "url": "http://ibict.br/a4" },
        { "oai_id": "5", "url": "http://ibict.br/a5" },
        { "oai_id": "6", "url": "http://ibict.br/a6" },
        { "oai_id": "7", "url": "http://ibict.br/a7" },
        { "oai_id": "8", "url": "http://ibict.br/a8" },
        { "oai_id": "9", "url": "http://ibict.br/a9" },
        { "oai_id": "10", "url": "http://ibict.br/a10" }
      ]
    }
    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, data=json.dumps(data), headers=headers)

    print(response.json())
```

###   cURL

```bash
    curl -X POST \
      '{{apiurl}}/load' \
      -H 'Content-Type: application/json' \
      -d '{
        "dnam_pk": "0x923f2551016c584a21bafa4b7c4e1a3facccccaec430748663062a308dd4bb337",
        "items": [
          { "oai_id": "1", "url": "http://ibict.br/a1" },
          { "oai_id": "2", "url": "http://ibict.br/a2" },
          { "oai_id": "3", "url": "http://ibict.br/a3" },
          { "oai_id": "4", "url": "http://ibict.br/a4" },
          { "oai_id": "5", "url": "http://ibict.br/a5" },
          { "oai_id": "6", "url": "http://ibict.br/a6" },
          { "oai_id": "7", "url": "http://ibict.br/a7" },
          { "oai_id": "8", "url": "http://ibict.br/a8" },
          { "oai_id": "9", "url": "http://ibict.br/a9" },
          { "oai_id": "10", "url": "http://ibict.br/a10" }
        ]
      }'
```
