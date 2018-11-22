# add unigrams+bigrams
# + new dictionary liwc
# + wordnet effect (64+).
#
# save it as sparse matrix and then pickle.
# + SVM with linear kernel.
# use liwc and sintement .
# 1. convert everything to unigrams(TF-IDF encoding)
# 2. for every group of features "class" have a model (LR and SVM)
# 3. have 1 model that combines all features (LR and SVM)
from pickle import dump, load
from xml.dom import minidom

#from sklearn.feature_extraction.text import TfidfVectorizer

from article_class import ArticleClass


# save a dataset to file
def save_dataset(dataset, filename):
    dump(dataset, open(filename, 'wb'))
    print('Saved: %s' % filename)


# load a clean dataset
def load_dataset(filename):
    return load(open(filename, 'rb'))


def extract_features(vocabulary):
    #vectorizer = TfidfVectorizer()
    #vectorizer.fit(vocabulary)
    #return vectorizer
    return None


class DataProcessing(object):
    def __init__(self):
        self.vectorizer = None
        pass

    def read_articles(self, articles_filename, labels_filename, training=True):
        # parse an xml file by name
        # if training:
        #    vocabulary = []
        articles_file = minidom.parse(articles_filename)
        labels_file = minidom.parse(labels_filename)
        articles_data = articles_file.getElementsByTagName('article')[:100]
        articles_labels = labels_file.getElementsByTagName('article')[:100]
        articles = dict()
        for article in articles_data:
            article_id = article.attributes['id'].value
            articles[article_id] = ArticleClass(article_id)
            try:
                articles[article_id].published_at = article.attributes['published-at'].value
            except KeyError:
                articles[article_id].published_at = None
            articles[article_id].title = article.attributes['title'].value
            articles[article_id].text = ""
            paragraphs = article.childNodes
            for paragraph in paragraphs:
                if paragraph.nodeType == paragraph.TEXT_NODE:
                    articles[article_id].text += paragraph.data
                articles[article_id].text += " ".join(p.data for p in paragraph.childNodes if p.nodeType == p.TEXT_NODE)
            articles[article_id].clean_article()
            # if training:
            #    vocabulary.extend(articles[article_id].text)
        for label in articles_labels:
            article_id = label.attributes['id'].value
            articles[article_id].hyperpartisan = (1 if label.attributes['hyperpartisan'].value == "true" else 0)
            articles[article_id].bias = label.attributes['bias'].value
            articles[article_id].labeled_by = label.attributes['labeled-by'].value
        print("Done reading data")
        # if training:
        #    self.vectorizer = self.extract_features(vocabulary)
        #    print("Done extracting features")

        return articles

    def read_titles(self, articles_filename, labels_filename):
        articles_file = minidom.parse(articles_filename)
        labels_file = minidom.parse(labels_filename)
        articles_data = articles_file.getElementsByTagName('article')
        articles_labels = labels_file.getElementsByTagName('article')
        articles = dict()
        for article in articles_data:
            article_id = article.attributes['id'].value
            articles[article_id] = ArticleClass(article_id)
            articles[article_id].title = article.attributes['title'].value
            articles[article_id].clean_title()

        for label in articles_labels:
            article_id = label.attributes['id'].value
            articles[article_id].hyperpartisan = (1 if label.attributes['hyperpartisan'].value == "true" else 0)
        print("Done reading data")

        return articles


if __name__ == '__main__':
    path = "/home/tariq/Downloads/datasets/hyperpartisan/"
    dataprocessor = DataProcessing()
    articles_training = dataprocessor.read_articles(path+"articles-training-20180831.xml",
                                                  path+"ground-truth-training-20180831.xml")
    articles_testing = dataprocessor.read_articles(path+"articles-validation-20180831.xml",
                                                 path+"ground-truth-validation-20180831.xml")
    # articles = dataprocessor.read_articles("/tmp/pycharm_project_127/data/test/articles-training-text.xml",
    #                                       "/tmp/pycharm_project_127/data/test/articles-training.xml", training=True)
    X_train = []
    y_train = []
    X_test = []
    y_test = []

    # for id in articles:
    #    X_train.append(" ".join(articles[id].text))
    #    y_train.append(articles[id].hyperpartisan)

    for id in articles_training:
        X_train.append(articles_training[id].text)
        y_train.append(articles_training[id].hyperpartisan)

    for id in articles_testing:
        X_test.append(articles_testing[id].text)
        y_test.append(articles_testing[id].hyperpartisan)

    print("Done appending labels")

    # X_train = dataprocessor.vectorizer.transform(X_train)
    # X_test = dataprocessor.vectorizer.transform(X_test)

    save_dataset([X_train, y_train], path+'pkl-objects/train_articles.pkl')
    save_dataset([X_test, y_test], path+'pkl-objects/test_articles.pkl')
    # save_dataset(dataprocessor.vectorizer, 'pkl-objects/vectorizer.pkl')

    print("Done vectorizing")
