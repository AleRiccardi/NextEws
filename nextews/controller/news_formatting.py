import pandas as pd

from .. import app, db


class NewsFormatting:
    m_all_authors = None
    m_all_sources = None
    m_new_authors = None
    m_new_news = None

    def __init__(self, news):
        if not news.empty:
            self.m_new_authors = self.__find_new_authors(news)
            self.m_new_news = self.__find_new_news(news)
        else:
            raise Exception("Empty data-frame passed in the constructor.")

    def __find_new_authors(self, news):
        """
        Unpack the downloaded news and extract the new authors
        that are not present in the database.
        :param news: recent news in data-frame format
        :return: the news to add
        """
        recent_authors_name = news['author'].dropna().unique()
        recent_authors = pd.DataFrame({'name': recent_authors_name})
        old_authors_no_id = db.get_authors_df()
        old_authors = old_authors_no_id.set_index('id')
        existing_authors = []

        print("Exist " + str(old_authors.shape[0]) + " authors")

        for index, the_recent_author in recent_authors.iterrows():
            for index, the_old_author in old_authors.iterrows():
                if str(the_recent_author['name']).lower() == str(the_old_author['name']).lower():
                    existing_authors += [the_recent_author['name']]

        new_authors = [recent_name for recent_name in recent_authors.name if recent_name not in existing_authors]
        new_authors = pd.DataFrame({'name': new_authors})
        # print("Found " + str(new_authors.shape[0]) + " new authors")
        db.save_df(name='authors', df=new_authors)
        return new_authors

    def __find_new_news(self, news):
        """
        Unpack the downloaded news and extract the new news
        that are not present in the database.
        :param news: recent news in data-frame format
        :return: the news to add
        """
        recent_news = news
        old_news = db.get_news_df()
        # FORMATTING NEWS TABLE
        # Now that we saved the new authors
        # we can get all of them from the database.
        self.m_all_authors = db.get_authors_df()
        self.m_all_sources = db.get_sources_df()
        recent_news['id_author'] = recent_news['author'].apply(self.get_id_author_by_name)
        recent_news['id_source'] = recent_news['id_source'].apply(self.get_id_source_by_name)
        del recent_news['author']
        del recent_news['name']
        # Reordering columns
        recent_news = (recent_news[[
            'title', 'description', 'content', 'url', 'urlToImage',
            'publishedAt', 'id_author', 'id_source']]
        )
        recent_news.rename(columns={'urlToImage': 'url_to_image', 'publishedAt': 'published_at'}, inplace=True)

        # SELECTING NEWS
        ids_recent_duplicate = []
        for the_recent_index, the_recent_news in recent_news.iterrows():
            for the_old_index, the_old_news in old_news.iterrows():
                if str(the_recent_news['title']).lower() == str(the_old_news['title']).lower():
                    ids_recent_duplicate += [the_recent_index]

        if ids_recent_duplicate:
            recent_news.drop(ids_recent_duplicate, inplace=True)

        return recent_news

    def get_id_author_by_name(self, name):
        """
        Return the id of the author. It can also return -1 in
        case there is no author.
        :param name: name of the author
        :return: the id of the author, -1 if not found
        """
        if name is not "":
            for index, author in self.m_all_authors.iterrows():
                if str(author['name']).lower() == str(name).lower():
                    return author['id']

        return -1

    def get_id_source_by_name(self, name):
        """
        Return the id of the source. It can also return -1 in
        case there is no author.
        :param name: name of the source
        :return: the id of the source, -1 if not found
        """
        if name is "":
            return -2
        for index, source in self.m_all_sources.iterrows():
            if str(source['slug']).lower() == str(name).lower():
                return source['id']

        return -1
