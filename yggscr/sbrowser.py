import json
from logging import CRITICAL, ERROR, WARNING, INFO, DEBUG #noqa
import requests
import cfscrape
from robobrowser import RoboBrowser
from robobrowser import exceptions as robo
from yggscr import ylogging

from pprint import (PrettyPrinter, pprint) #noqa
pp = PrettyPrinter(indent=4)


class SBrowser:

    def __init__(self, scraper=None,
                 browser=None, proxy=None, loglevel=INFO, **kwargs):

        self.log = ylogging.consolelog(name=__name__, loglevel=loglevel)
        self.log.info("Starting Ygg Browser")

        self.scraper = scraper or cfscrape.create_scraper()
        self.browser = browser or RoboBrowser(session=self.scraper, **kwargs)
        self.proxify(proxy)

        self.log.debug("Created SBrowser")

    def __str__(self):
        cd = self.connection_details()
        return "[Browser] - CF was {}, UA {}, Proxy {}, \
               Local {} Host {} Country {} City {}".format(
                    "active" if self.is_cloudflare() else "inactive",
                    self.browser.session.headers['User-Agent'],
                    "none" if self.proxy is None else self.proxy,
                    cd["ip"],
                    cd["hostname"] if "hostname" in cd else "N/A",
                    cd["country"] if "country" in cd else "N/A",
                    cd["city"] if "city" in cd else "N/A",
                )

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
        self.log.debug("Proxy set to {}".format(self.browser.session.proxies))

    def connection_details(self):
        """
        Return WAN connection detail
        { "ip": "8.8.8.8", "hostname": "a.example.com",
          "city": "Paris", "country": "France", ...
        }
        """

        try:
            self.browser.open("https://ipinfo.io/json")
            self.log.error("IPINFO Server returned (%s)" % self.response().content)
            res = json.loads(self.response().content.decode('utf-8'))
        except (requests.exceptions.ProxyError,
                requests.exceptions.ConnectionError):
            return {'ip': 'Unknown'}
        except ValueError:
            self.log.error(
                "Server returned no JSON (%s)" % self.response().content)
            return {'ip': 'Unknown'}
        return res

    def parsed(self):
        return self.browser.parsed

    def response(self):
        return self.browser.response

    def get(self, url, **kwargs):
        self.log.debug(">>> {}".format(url))
        self.browser.open(url, **kwargs)
