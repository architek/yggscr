import json
import requests
import cfscrape
import robobrowser


class SBrowser:
    """ General scrapper browser with cloudFlare bypass """
    def __init__(self, log, scraper=None,
                 browser=None, proxy=None, **kwargs):

        self.log = log
        # BUG Limnoria vs Python requests or cfscrape
        # self.scraper = scraper or cfscrape.create_scraper()
        self.scraper = requests.Session()
        self.browser = browser or robobrowser.RoboBrowser(session=self.scraper, **kwargs)
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
        except robobrowser.exceptions.RoboError:
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
        self.log.debug("Proxy set to %s", self.browser.session.proxies)

    def connection_details(self):
        """
        Return WAN connection detail
        """
        try:
            self.open("https://ipinfo.io/json")
            self.log.debug("IPINFO Server returned (%s)", self.response().content)
            res = json.loads(self.response().content.decode('utf-8'))
        except (requests.exceptions.ProxyError,
                requests.exceptions.ConnectionError):
            return {'ip': 'Unknown'}
        except ValueError:
            self.log.error("Server returned no JSON (%s)", self.response().content)
            return {'ip': 'Unknown'}
        except Exception as exc:  # TODO
            self.log.error("Unknown exception %s", exc)
            return {'ip': 'Unknown'}
        else:
            return res

    def parsed(self):
        return self.browser.parsed

    def response(self):
        return self.browser.response

    def open(self, url, **kwargs):
        self.log.debug(">>> %s", url)
        self.browser.open(url, **kwargs)
