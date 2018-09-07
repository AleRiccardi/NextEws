import pandas as pd
from datetime import datetime

from .. import app, db


class NewsDb:
    m_news = None
    m_authors = None
    m_sources = None

    def __init__(self, news):
        if not news.empty:
            self.m_news = news
            self.m_sources = db.get_sources_df()
            self.m_authors = db.get_authors_df()
            self.save_new_authors()
            # now that we saved the new authors
            # we can get all of them from the database.
            self.m_authors = db.get_authors_df()

            self.m_news['id_author'] = self.m_news['author'].apply(self.get_id_author_by_name)
            del self.m_news['author']

            self.m_news['id_source'] = self.m_news.id_source.apply(self.get_id_source_by_name)
            del self.m_news['name']

            self.m_news = self.m_news[
                ['title', 'description', 'content', 'url', 'urlToImage', 'publishedAt', 'id_author', 'id_source']]
            self.m_news.rename(columns={'urlToImage': 'url_to_image', 'publishedAt': 'published_at'}, inplace=True)
            self.m_news.head(1)
        else:
            raise Exception("Empty data-frame passed in the constructor.")

    def save_new_authors(self):
        """
        Unpack the downloaded news and extract the authors
        to add them to the database.
        :return:
        """
        authors = self.m_news['author'].dropna().unique()
        recent_authors = pd.DataFrame({'name': authors})
        old_authors = self.m_authors.set_index('id')
        existing_authors = []

        print("Exist " + str(old_authors.shape[0]) + " authors")

        for index, the_recent_author in recent_authors.iterrows():
            for index, the_old_author in old_authors.iterrows():
                if str(the_recent_author['name']).lower() == str(the_old_author['name']).lower():
                    existing_authors += [the_recent_author['name']]
        print(existing_authors)
        new_authors = [recent_name for recent_name in recent_authors.name if recent_name not in existing_authors]
        df_new_authors = pd.DataFrame({'name': new_authors})

        print("Upload of " + str(df_new_authors.shape[0]) + " authors")
        db.save_df(name='authors', df=df_new_authors)

    def get_id_author_by_name(self, name):
        """
        Return the id of the author. It can also return -1 in
        case there is no author.
        """
        if name is not "":
            for index, author in self.m_authors.iterrows():
                if str(author['name']).lower() == str(name).lower():
                    return author['id']

        return -1

    def get_id_source_by_name(self, name):
        if name is "":
            return -2
        for index, source in self.m_sources.iterrows():
            if str(source['slug']).lower() == str(name).lower():
                return source['id']

        return -1

    def upload(self):
        last_news_dict = db.get_last_news_single()
        limit_time = last_news_dict['published_at']
        limit_time = datetime.strptime(limit_time, "%Y-%m-%dT%H:%M:%SZ")
        news_to_add = self.m_news.iloc[0:0] # create an empty data-frame
        for index, m_news in self.m_news.iterrows():
            if m_news['published_at'] > limit_time:
                news_to_add.append(m_news)

        print("Upload of " + str(news_to_add.shape[0]) + " news")
        return news_to_add
