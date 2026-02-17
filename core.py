import asyncio
import httpx
from bs4 import BeautifulSoup
from flask import Flask
import threading
import re

class Webber:
    def __init__(self,
                 user_agent=None,
                 website=None,
                 custom_web=False,
                 port=8080,
                 web_requester=False,
                 web_method="get",
                 parse_html=False,
                 post_something=False,
                 post_target=None,
                 use_json=False,
                 persistent_session=True,
                 timeout=None,
                 proxies=None,
                 custom_headers=None):

        self.user_agent = user_agent
        self.website = website
        self.custom_web = custom_web
        self.port = port
        self.web_requester = web_requester
        self.web_method = web_method.lower()
        self.parse_html = parse_html
        self.post_something = post_something
        self.post_target = post_target
        self.use_json = use_json
        self.persistent_session = persistent_session
        self.timeout = timeout or 20
        self.proxies = proxies
        self.custom_headers = custom_headers or {}

        self.app = Flask(__name__)
        self.client = httpx.AsyncClient(timeout=self.timeout, proxies=self.proxies) if self.persistent_session else None

        if self.custom_web:
            self._start_server()

    def _start_server(self):
        @self.app.route("/")
        def home():
            return "Webber v1 (final) Running"
        threading.Thread(
            target=self.app.run,
            kwargs={"host": "0.0.0.0", "port": self.port},
            daemon=True
        ).start()

    def _clean(self, text):
        return re.sub(r'\s+', ' ', text).strip()

    def _parse(self, html):
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()
        title = soup.title.string.strip() if soup.title else "No Title"
        paragraphs = [self._clean(p.get_text()) for p in soup.find_all("p")]
        content = " ".join([p for p in paragraphs if len(p) > 40])
        return {"title": title, "content": content[:5000]}

    async def _make_request(self, data=None):
        headers = {"User-Agent": self.user_agent} if self.user_agent else {}
        headers.update(self.custom_headers)

        client = self.client if self.persistent_session else httpx.AsyncClient(timeout=self.timeout, proxies=self.proxies)

        target = self.website
        if self.web_method == "post" and self.post_something and self.post_target:
            target = self.post_target

        if self.web_method == "post":
            if self.use_json:
                r = await client.post(target, headers=headers, json=data)
            else:
                r = await client.post(target, headers=headers, data=data)
        else:
            r = await client.get(target, headers=headers)

        return r

    def request(self, data=None):
        if not self.web_requester:
            return None

        r = asyncio.run(self._make_request(data))

        content_type = r.headers.get("content-type", "")

        if "application/json" in content_type:
            return r.json()

        if "text/html" in content_type and self.parse_html:
            return self._parse(r.text)

        return {"status": r.status_code, "text": r.text[:3000]}
