# Webber v1

Async Python wrapper: Flask + HTTPX + BeautifulSoup

## Features

- GET / POST requests
- Optional JSON payload
- POST to custom target
- Persistent session (cookies)
- Optional Flask server
- Optional HTML parsing
- Timeout, proxies, custom headers

## Usage

```python
from webber import Webber

web = Webber(
    website="https://httpbin.org/post",
    web_requester=True,
    web_method="post",
    use_json=True,
    post_something=True,
    post_target="https://httpbin.org/post",
    persistent_session=True
)

response = web.request(data={"username": "c4zz"})
print(response)
