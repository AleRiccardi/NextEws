import pandas as pd
import numpy as np

from newsapi import NewsApiClient
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

from os import path

from .. import app, db
from .news_formatting import NewsFormatting


class NewsScanner:
    NUM_NEWS_TO_SCRAP = 30

    m_scraper = None
    m_scraped_news = None
    m_report = None
    m_source_name = None
    m_web_scrape_sources = None

    m_num_new_authors = 0
    m_num_new_news = 0
    m_num_total_news = 0

    def __init__(self):
        self.m_scraper = Scraper()
        self.m_source_name, self.m_web_scrape_sources = get_sources()

    def run_scraper(self):
        basic_news = self.download_basic_news()
        # scrape the content
        scraped_news = self.scrap_news(basic_news, self.m_web_scrape_sources)
        scraped_news = self.set_data_type(scraped_news)
        self.upload_to_db(scraped_news)

    # web scraper
    def scrap_news(self, news, web_scrape_sources):
        """
        Permit to scrape the news and get the content.
        The scraper is limited by the number of source that are passed
        and they need to have the right tags to permit to find the blocks
        that contain them.

        :param news: pandas df with the news (without content)
        :param web_scrape_sources: the sources with the tags
        :return: return the input panda df (news) but with the content column.
        """
        report = pd.DataFrame(columns=['id', 'success', 'status'])
        contents_scraped = []
        return_news = news
        for index, the_news in news.iterrows():
            content_found = ''
            raw_html = self.m_scraper.simple_get(the_news.url)

            if raw_html is None:
                report.loc[index] = [index, False, 'no html']
            else:
                html = BeautifulSoup(raw_html, 'html.parser')
                body = self.m_scraper.get_body(the_news, html, web_scrape_sources)

                if body is None:
                    report.loc[index] = [index, False, 'no body']
                else:
                    contents = self.m_scraper.get_content(the_news, body, web_scrape_sources)
                    for content in contents:
                        if content.text is not None and len(content.text) > 50:
                            content_found += content.text.strip() + ' '
                            report.loc[index] = [index, True, '']
                    # if content retrived if empty
                    if content_found == '':
                        report.loc[index] = [index, False, 'content empty']

            contents_scraped.append(content_found)

        return_news['content'] = contents_scraped
        self.m_scraped_news = return_news

        self.m_report = self.report_status(report)  # report status
        return self.m_scraped_news

    def download_basic_news(self):
        """

        :return:
        """
        columns = ['id_source', 'name', 'author', 'title', 'description', 'url', 'urlToImage', 'publishedAt', 'content']
        request_number = self.NUM_NEWS_TO_SCRAP

        # DATA PREPARATION
        # Building and executing the request to newsapi.org
        newsapi = NewsApiClient(api_key='a11cabb5333f4ade87a27e20f28bb568')
        all_articles = newsapi.get_top_headlines(sources=self.m_source_name,
                                                 language='en',
                                                 page_size=request_number)

        # DATA FORMATTING
        data = pd.DataFrame.from_dict(all_articles)
        data = data['articles'].apply(pd.Series)
        new_news = pd.concat([data.drop(['source'], axis=1), data['source'].apply(pd.Series)], axis=1)
        new_news = new_news[['id', 'name', 'author', 'title', 'description', 'url', 'urlToImage', 'publishedAt']]
        new_news.rename(columns={'id': 'id_source'}, inplace=True)

        return new_news

    def upload_to_db(self, news):
        news_db_uploader = NewsFormatting(news)

        self.m_num_total_news = self.NUM_NEWS_TO_SCRAP
        self.m_num_new_authors = news_db_uploader.m_new_authors.shape[0]
        self.m_num_new_news = news_db_uploader.m_new_news.shape[0]

    @staticmethod
    def report_status(report):
        string_report = ''
        num_rows = report.shape[0]
        success = report[report.success == True].shape[0]
        fail = num_rows - success
        string_report = 'Websites scraped: ' + str(num_rows) + ', success: ' + str(success) + ', fail: ' + str(
            fail) + ' <br> '
        # print fail
        if fail > 0:
            for index, the_report in report[report.success == False].iterrows():
                string_report += 'Error log (' + str(index) + '): ' + the_report.status + ' <br> '

        return string_report

    def get_scraped_news(self):
        return self.m_scraped_news

    def get_report_messages(self):
        return self.m_report

    @staticmethod
    def set_data_type(news):
        # Remove unuseful information in date
        news['publishedAt'] = news['publishedAt'].apply(lambda d: d.split('.', 1)[0])
        # Remove T letter
        news['publishedAt'] = news['publishedAt'].apply(lambda d: d.replace('T', ' '))
        # Converting to Date
        news['publishedAt'] = pd.to_datetime(news['publishedAt'], format="%Y-%m-%d %H:%M:%S")

        return news


class Scraper:

    def simple_get(self, url):
        """
        Attempts to get the content at `url` by making an HTTP GET request.
        If the content-type of response is some kind of HTML/XML, return the
        text content, otherwise return None.
        """
        try:
            with closing(get(url, stream=True)) as resp:
                if self.is_good_response(resp):
                    return resp.content
                else:
                    self.log_error('Error during requests to ' + url + ' : status code ' + str(resp.status_code))
                    return None

        except RequestException as e:
            self.log_error('Error during requests to ' + url + ' : ' + str(e))
            return None

    def is_good_response(self, resp):
        """
        Returns True if the response seems to be HTML, False otherwise.
        """

        content_type = resp.headers['Content-Type'].lower()
        return (resp.status_code == 200
                and content_type is not None
                and content_type.find('html') > -1)

    def log_error(e):
        """
        It is always a good idea to log errors.
        This function just prints them, but you can
        make it do anything.
        """
        print(e)

    def get_body(self, the_news, html, web_scrape_sources, rec=1):
        """
        Get the body of the news page, where it is
        cointained the information.
        """
        body_tag = web_scrape_sources[web_scrape_sources.id == the_news.id_source]['body_tag_' + str(rec)].values[0]
        body_name = web_scrape_sources[web_scrape_sources.id == the_news.id_source]['body_name_' + str(rec)].values[0]

        # tag & class
        body = html.find(body_tag, attrs={'class': body_name})
        if body is None:
            # tag & id
            body = html.find(body_tag, attrs={'id': body_name})

        if body is None and rec == 1:
            body = self.get_body(the_news, html, web_scrape_sources, 2)

        return body

    def get_content(self, the_news, body, web_scrape_sources, rec=1):
        """
        Get the contents of the news.
        """
        content_tag = web_scrape_sources[web_scrape_sources.id == the_news.id_source]['content_tag_' + str(rec)].values[
            0]
        content_name = \
            web_scrape_sources[web_scrape_sources.id == the_news.id_source]['content_name_' + str(rec)].values[0]

        # tag & class
        content = body.findAll(content_tag, attrs={'class': content_name})
        if content is None:
            # tag & id
            content = body.findAll(content_tag, attrs={'id': content_name})

        if content is None and rec == 1:
            content = self.get_content(the_news, body, web_scrape_sources, 2)
        return content


def get_sources():
    web_scrape_sources = pd.read_csv(path.join(app.root_path, "static/util/web_scrape_tag.csv"), delimiter=',').fillna(
        '')
    source_names_list = web_scrape_sources.id.unique()
    names_string = ""
    for name in source_names_list[:-1]:
        names_string += str(name + ',')
    names_string += str(source_names_list[-1])
    return names_string, web_scrape_sources
