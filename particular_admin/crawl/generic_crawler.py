from datetime import datetime
from urllib.parse import urlparse

from newsplease import NewsPlease
from pyspider.libs.base_handler import BaseHandler, config, every

from particular_admin import logger
from particular_admin.app import app, db
from particular_admin.models.user import User  # noqa: F401
from particular_admin.models.website import Website
from particular_admin.settings import ADMIN_URL

PAGE_TIMEOUT_SECONDS = 3600
START_PAGE_TIMEOUT_SECONDS = 60

CRAWL_INTERVAL_MINUTES = 1

# Lifted from scrapy
# https://github.com/scrapy/scrapy/blob/master/scrapy/linkextractors/__init__.py
STATIC_EXTENSIONS = {
    # archives
    '7z', '7zip', 'bz2', 'rar', 'tar', 'tar.gz', 'xz', 'zip',

    # images
    'mng', 'pct', 'bmp', 'gif', 'jpg', 'jpeg', 'png', 'pst', 'psp', 'tif',
    'tiff', 'ai', 'drw', 'dxf', 'eps', 'ps', 'svg', 'cdr', 'ico',

    # audio
    'mp3', 'wma', 'ogg', 'wav', 'ra', 'aac', 'mid', 'au', 'aiff',

    # video
    '3gp', 'asf', 'asx', 'avi', 'mov', 'mp4', 'mpg', 'qt', 'rm', 'swf', 'wmv',
    'm4a', 'm4v', 'flv', 'webm',

    # office suites
    'xls', 'xlsx', 'ppt', 'pptx', 'pps', 'doc', 'docx', 'odt', 'ods', 'odg',
    'odp',

    # other
    'css', 'pdf', 'exe', 'bin', 'rss', 'dmg', 'iso', 'apk',
}


class GenericCrawler(BaseHandler):
    crawl_config = {
        'headers': {
            'User-Agent': f'ParticularBot/1.0 ({ADMIN_URL}/about/bot)',
        },
    }

    @every(minutes=CRAWL_INTERVAL_MINUTES)
    def on_start(self):
        now = datetime.utcnow()

        with app.app_context():
            active_websites = Website.query.filter_by(active=True)

            active_websites.update({Website.date_crawled_utc: now})
            db.session.commit()

            websites = active_websites.all()

        for website in websites:
            logger.info(f'Starting crawl for {website}')
            self.crawl(
                website.root_url,
                callback=self.handle_start_page,
                save={'allowed_domains': website.allowed_domains_list},
            )

    def crawl_other_links(self, response):
        for link in response.doc('a[href^="http"]').items():
            url = urlparse(link.attr.href)

            if '.' in url.path and url.path.rsplit('.')[-1] in STATIC_EXTENSIONS:
                continue

            if url.netloc not in response.save['allowed_domains']:
                continue

            url = f'{url.scheme}://{url.netloc}{url.path}'

            self.crawl(
                url,
                callback=self.handle_page,
                save={'allowed_domains': response.save['allowed_domains']},
            )

    def crawl_page(self, response):
        self.crawl_other_links(response)

        article = NewsPlease.from_html(response.content, url=response.url)
        data = article.get_dict()
        data.pop('maintext')

        yield data

    @config(age=START_PAGE_TIMEOUT_SECONDS)
    def handle_start_page(self, response):
        yield from self.crawl_page(response)

    @config(age=PAGE_TIMEOUT_SECONDS)
    def handle_page(self, response):
        yield from self.crawl_page(response)
