# Generated by Django 3.0.6 on 2020-05-16 15:44
import os

import nltk
from django.db import migrations
import pandas as pd
from news_clustering.settings import BASE_DIR


def load_initial_dataset(apps, schema_editor):
    df = pd.read_pickle(os.path.join(BASE_DIR, 'news_clustering/datasets/lenta-ru-news-embedded.pkl'))

    Article = apps.get_model('news', 'Article')
    Cluster = apps.get_model('news', 'Cluster')

    for _, clustered_articles in df.groupby('cluster_id'):
        cluster = Cluster.objects.create()
        articles = []

        for article in clustered_articles.itertuples():
            articles.append(
                Article(
                    title=article.title,
                    text=article.text,
                    source=article.url,
                    publish_date=article.date,
                    text_sentences=nltk.sent_tokenize(article.text),
                    text_sentence_embeddings=list(map(lambda i: i.tolist(), article.text_embeddings)),
                    title_embedding=article.title_embeddings.tolist(),
                    cluster_id=cluster.id,
                )
            )

        Article.objects.bulk_create(articles)


def skip(*args):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_initial_dataset, skip),
    ]