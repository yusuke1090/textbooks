# 2. The browser and HTTP

**HTTP** (HyperText Transfer Protocol) is the set of rules for how a browser and a server talk. The browser sends a **request** ("please send me this page") and the server returns a **response** ("here you are"). Every exchange on the web has this shape.

## Reading a URL

A **URL** says in one line which server to go to, which data to get, and how.

```text
https://example.com:443/news/list.html?page=2#top
```

| Part | Example | Meaning |
| --- | --- | --- |
| Scheme | `https` | How to fetch it. `https` is encrypted HTTP (Chapter 9) |
| Host name | `example.com` | Which server. DNS turns it into an IP address (Chapter 3) |
| Port number | `443` | Which application on the server (Chapter 4). 443 for `https` and 80 for `http`, so it is usually left out |
| Path | `/news/list.html` | Which data on the server |
| Query | `?page=2` | Extra values for the server, joined with `&` |
| Fragment | `#top` | A place inside the page. It is not sent to the server; only the browser uses it |

## Requests and responses

An HTTP/1.1 exchange is just text. You can see it with `curl -v` (`>` is what was sent and `<` is what came back).

```bash
curl -v http://example.com/ -o /dev/null
```

```text
> GET / HTTP/1.1
> Host: example.com
> User-Agent: curl/8.18.0
> Accept: */*
>
< HTTP/1.1 200 OK
< Content-Type: text/html; charset=utf-8
< Server: cloudflare
< Age: 13682
< cf-cache-status: HIT
```

- **Request**: the first line is "**method** path version". **Headers** (`Name: value`) follow, ending with an empty line. For POST and similar methods, a **body** (the data being sent) comes after that
- **Response**: the first line is "version **status code** description". After the headers and an empty line comes the **body** (the HTML or image itself)

Thanks to `Host:`, one server (one IP address) can serve many sites with different names.

### Common methods

| Method | Meaning | Example |
| --- | --- | --- |
| `GET` | Get data | Open a page, load an image |
| `POST` | Send data and have something done | Submit a form, send a sensor reading |
| `PUT` / `PATCH` | Replace data / change part of it | Change a setting |
| `DELETE` | Delete data | Remove a record |
| `HEAD` | Get only the headers | When you only want the size or date (`curl -I`) |

### Status codes

The first digit tells you the general meaning.

| Code | Meaning | Ones you often see |
| --- | --- | --- |
| 2xx | It worked | `200 OK` |
| 3xx | Look somewhere else | `301 Moved Permanently` (it moved), `304 Not Modified` (use the copy you have) |
| 4xx | A mistake by **the side that asked** | `400` badly formed, `401` log in first, `403` not allowed, `404 Not Found` |
| 5xx | Trouble on **the server's side** | `500` error inside the server, `502` and `504` the server behind it did not answer, `503` busy or down for maintenance |

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://example.com/nothing-here
```

```text
404
```

## What headers tell you

| Header | Direction | Meaning |
| --- | --- | --- |
| `Host` | Request | Which site |
| `User-Agent` | Request | Which browser or app |
| `Cookie` | Request | Sends back a cookie received earlier (below) |
| `Content-Type` | Both | The kind of body (`text/html`, `application/json`, `image/jpeg` and so on) |
| `Cache-Control` | Response | How long the copy may be kept and reused |
| `Set-Cookie` | Response | Asks the browser to remember a cookie |
| `Location` | Response | The new address for a 3xx response |

## HTTP does not remember: cookies

Each HTTP exchange stands alone, and HTTP does not remember earlier requests (it is **stateless**). You can still stay logged in thanks to **cookies**.

1. When you log in successfully, the server returns `Set-Cookie: session=abc123`
2. The browser remembers it and adds `Cookie: session=abc123` to every request to that site
3. From that value, the server knows "this is the person who just logged in"

If someone steals the cookie, they can pretend to be that person. That is why encrypting with HTTPS (Chapter 9) matters.

## One page means dozens of requests

HTML contains links to images, CSS, JavaScript and fonts. As the browser reads the HTML, it fetches each of them. A big news site can make more than 100 requests for one page.

In Chrome on a computer, press **F12** (Developer Tools) and open the "Network" tab to see every request with its time, status code and headers.

## HTTP/1.1, HTTP/2 and HTTP/3

| Version | Year | Features |
| --- | --- | --- |
| HTTP/1.1 | 1997 | Exchanged as text. One request at a time on each TCP connection |
| HTTP/2 | 2015 | Many requests flow at once inside one TCP connection. Headers are compressed |
| HTTP/3 | 2022 | Uses **QUIC** (on top of UDP, Chapter 4) instead of TCP. Connects faster and survives a phone switching from Wi-Fi to 4G/5G |

What applications see (methods, status codes, headers) is the same; only the way it is carried differs.

## Web APIs: apps talk HTTP too

HTTP is not only for browsers. Phone apps and IoT devices also send and receive JSON over HTTP to use a server's features. This is called a **web API**.

```bash
curl -s -X POST -H "Content-Type: application/json" \
     -d '{"barn": 1, "temp": 21.5}' https://httpbin.org/post
```

```text
{
  "headers": {
    "Content-Length": "25",
    "Content-Type": "application/json",
    "Host": "httpbin.org",
    ...
  },
  "json": {
    "barn": 1,
    "temp": 21.5
  },
  "method": "POST",
  "origin": "203.0.113.45",
  ...
}
```

httpbin.org is a test server that sends back the request it received. `origin` is your IP address as the server sees it (your home router's global IP address, Chapter 7).

## The first web server

![The NeXT computer that became the first web server at CERN](images/first-web-server.jpg)

In 1990, Tim Berners-Lee ran the first web server and browser on a NeXT computer at CERN. A note stuck on it said: "This machine is a server. DO NOT POWER IT DOWN!!"

## Summary

- A URL has a scheme, host name, port, path and query
- HTTP is an exchange of requests (method, headers, body) and responses (status code, headers, body)
- 4xx means a problem on the asking side; 5xx means a problem on the server's side
- HTTP does not remember earlier exchanges, so logins are kept with cookies
- Apps and IoT devices use HTTP too, through web APIs

## Exercises

```quiz
Q: Which HTTP method is used to get data?
A: GET
E: POST is used to send data and have something done.

Q: Which status code means "page not found"?
A: 404
E: 4xx is a problem on the asking side; 5xx is a problem on the server's side.

Q: For an https URL with no port written, which port number is used?
A: 443
E: For http it is 80.

Q: HTTP does not remember earlier exchanges. What does the browser send back every time to stay logged in?
A: cookie | cookies
E: The server hands it over with Set-Cookie and the browser returns it in the Cookie header.

Q: Which protocol, running on top of UDP, does HTTP/3 use instead of TCP?
A: QUIC
E: It connects quickly and copes well when the connection switches.
```
