import json
import logging
import requests
import cfscrape
from robobrowser import RoboBrowser
from robobrowser import exceptions as robo

# from pprint import (PrettyPrinter, pprint)
# pp = PrettyPrinter(indent=4)


class SBrowser:

    def __init__(self, scraper=None,
                 browser=None, proxy=None, loglevel=logging.INFO, **kwargs):
        self.log = self.consolelog(loglevel)
        self.log.info("Starting Ygg Scraper")
        self.scraper = scraper or cfscrape.create_scraper()
        self.browser = browser or RoboBrowser(session=self.scraper, **kwargs)
        self.proxify(proxy)
        self.log.debug("Created SBrowser")

    def __str__(self):
        cd = self.connection_details()
        return "[Browser] - CF was {}, UA {}, Proxy {}, Local {} Host {}".format(
            "active" if self.is_cloudflare() else "inactive",
            self.browser.session.headers['User-Agent'],
            "none" if self.proxy is None else self.proxy,
            cd["ip"],
            cd["hostname"] if "hostname" in cd else "none")

    def consolelog(self, loglevel):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s "
                                      "- %(message)s [%(filename)s:%(lineno)s]")
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(loglevel)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        return logger

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
        self.browser.open(url, **kwargs)
