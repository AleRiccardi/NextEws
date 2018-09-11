from .. import db
from datetime import datetime


class News:
    """
    Model news.
    That class contain all the information the a news
    require.

    @author:    Alericcardi
    @version:   1.0.0
    """
    id = None
    title = None
    description = None
    content = None
    url = None
    url_to_image = None
    published_at = None
    id_author = None
    id_source = None
    id_category = None

    def __init__(self, the_news):
        """
        Recive a dict. object and fill all the field that
        the news class has.
        :param the_news: dictionary object
        """
        self.id = the_news['id']
        self.title = the_news['title']
        self.description = the_news['description']
        self.content = the_news['content']
        self.url = the_news['url']
        self.url_to_image = the_news['url_to_image']
        self.published_at = the_news['published_at']
        self.id_author = the_news['id_author']
        self.id_source = the_news['id_source']
        self.id_category = the_news['id_category']

    def get_dict(self):
        return {
            'id', self.id,
            'title', self.title,
            'description', self.description,
            'content', self.content,
            'url', self.url,
            'url_to_image', self.url_to_image,
            'published_at', self.published_at,
            'id_author', self.id_author,
            'id_source', self.id_source,
            'id_category', self.id_category,
        }

    def get_category(self):
        categories = db.get_categories()
        the_category = [cat for cat in categories if cat['id'] == self.id_category][0]
        return the_category

    def get_author(self):
        authors = db.get_authors()
        the_author = [author for author in authors if author['id'] == self.id_author]
        if the_author:
            return the_author[0]
        return None

    def get_source(self):
        sources = db.get_sources()
        the_source = [source for source in sources if source['id'] == self.id_source][0]
        return the_source

    def get_published_string(self):
        time_string = self.published_at.split('.', 1)[0]
        time = datetime.strptime(time_string, "%Y-%m-%d %H:%M:%S")

        return time.strftime('Published the %d, %b %Y')
