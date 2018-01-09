import urllib.parse
import http.client
import wsgiref.util

REDIRECT_LIST = {}
REDIRECT_LIST["http://go.microsoft.com/fwlink/?LinkID=616995"] = "http://adamrdriscoll.gallerycdn.vsassets.io/extensions/adamrdriscoll/powershelltoolsforvisualstudio2015/3.0.582/1504150209811/199313/7/PowerShellTools.14.0.vsix"

class VS2015InstallProxy:
    def __call__(self, environ, start_response):
        url = environ["PATH_INFO"]
        if environ["QUERY_STRING"]:
            url += "?" + environ["QUERY_STRING"]
        req = urllib.parse.urlparse(url)

        if url in REDIRECT_LIST:
            start_response("302 Moved Temporarily", [("Location", REDIRECT_LIST[url])])
            return [b""]
        elif req.hostname:
            path = req.path
            if req.query:
                path += "?" + req.query
            body = None
            if environ["CONTENT_LENGTH"]:
                body = environ["wsgi.input"].read(int(environ["CONTENT_LENGTH"]))

            con = http.client.HTTPConnection(req.hostname, port=req.port)
            try:
                con.request(environ["REQUEST_METHOD"], path, body=body, headers=get_request_headers(environ))
                res = con.getresponse()
                start_response("%d %s" % (res.status, res.reason), get_response_headers(res.getheaders()))
                return [res.read()]
            finally:
                con.close()
        else:
            return proxy_pac(start_response)

def get_request_headers(environ):
    request_headers = {}
    for k, v in environ.items():
        if not k.startswith("HTTP_"):
            continue

        words = k.split("_")
        words.pop(0)
        for i in range(len(words)):
            words[i] = words[i].lower().capitalize()
        request_headers["-".join(words)] = v
    return request_headers

def get_response_headers(headers):
    response_headers = []
    for k, v in headers:
        if wsgiref.util.is_hop_by_hop(k):
            continue

        if k == "Location" and v.startswith("https://"):
            v = v.replace("https://", "http://", 1)
        response_headers.append((k, v))
    return response_headers

def proxy_pac(start_response):
    start_response("200 OK", [("Content-Type", "text/plain")])
    return [b"""function FindProxyForURL(url, host){
    if(shExpMatch(url, "http://go.microsoft.com/*")){
        return "PROXY localhost:8080";
    }
    else{
        return "DIRECT";
    }
}
"""]

application = VS2015InstallProxy()

def run():
    import wsgiref.simple_server
    httpd = wsgiref.simple_server.make_server("", 8080, application)
    httpd.serve_forever()

if __name__ == "__main__":
    run()
