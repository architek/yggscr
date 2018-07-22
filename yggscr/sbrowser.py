import json
import requests
import cfscrape
from robobrowser import RoboBrowser
from robobrowser import exceptions as robo

# from pprint import (PrettyPrinter, pprint)
# pp = PrettyPrinter(indent=4)


class SBrowser:

    def __init__(self, scraper=None,
                 browser=None):
        self.scraper = scraper or cfscrape.create_scraper()
        self.browser = browser or RoboBrowser(session=self.scraper,
                                              history=False,
                                              timeout=7)
        self.proxy = None

    def __str__(self):
        cd = self.connection_details()
        return "[Browser] - CF was {}, UA {}, Proxy {}, Local {} Host {}".format(
            "active" if self.is_cloudflare() else "inactive",
            self.browser.session.headers['User-Agent'],
            "none" if self.proxy is None else self.proxy,
            cd["ip"],
            cd["hostname"] if "hostname" in cd else "none")

    def is_cloudflare(self):
        try:
            return self.scraper.is_cloudflare_challenge(self.response())
        except robo.RoboError:
            return None

    def proxify(self, https_proxy=None):
        """
        Sets an https-only proxy:
         * https://user:pass@host:port   : HTTP  proxy
         * socks5h://user:pass@host:port : SOCKS proxy
         * socks5://user:pass@host:port  : SOCKS proxy with local DNS resolver
        """
        self.proxy = https_proxy
        self.browser.session.proxies = {'https': self.proxy}

    def connection_details(self):
        """
        Return WAN connection detail
        { "ip": "8.8.8.8", "hostname": "a.example.com",
          "city": "Paris", "country": "France", ...
        }
        """

        try:
            self.browser.open("https://ipinfo.io/json")
            res = json.loads(self.response().content.decode('utf-8'))
        except (requests.exceptions.ProxyError,
                requests.exceptions.ConnectionError):
            return {'ip': 'Unknown'}
        except ValueError:
            print("Server returned no JSON (%s)" % self.response().content)
            return {'ip': 'Unknown'}
        return res

    def parsed(self):
        return self.browser.parsed

    def response(self):
        return self.browser.response

    def get(self, url, **kwargs):
        self.browser.open(url, **kwargs)
