# Reddit parser
This project is a Reddit parser. It can get a list of subreddits with keywords, download first posts from each subreddit, filter posts and show if each post has image or not. You can use it in the browser via a simple form which includes a button, just set subreddit's name and enter keywords with limit.

There is loading state while fetching. If some error happens, it will show red error message.

This tool uses retrying for smoother parsing. If a request fails, the parser will try again after a few seconds.

## Usage
To build the project, run this command in the project root:
```bash 
docker compose up --build
```
Backend will run on `http://localhost:8000` and frontend will run on `http://localhost:3000`. 

To start using it, open frontend on `localhost:3000.`

### Example responses
Example request to API (POST `/parse`):
```bash
{
"items": [
{
"subreddit": "aww",
"keywords": ["cat", "dog", "forest", "river"]
},
{
"subreddit": "nature",
"keywords": ["cat", "dog", "forest", "river"]
}
],
"limit": 5
}
```
Example response:
```bash
{
"/r/aww": [
{"title": "Cute cat picture", "has_image": true},
{"title": "Dog playing outside", "has_image": false}
],
"/r/nature": []
}
```

## Potential problems
This tool uses HTTP to parse pages' HTML and extract data. This can lead to some problems, e.g. if HTML structure changes or posts get deleted/hidden, it won't get info correctly. Reddit also can probably block these requests. To fix it, using official API would be a good solution. Using retry with delays also can help.
