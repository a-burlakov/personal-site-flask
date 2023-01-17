import os
import json
from flask import Flask, render_template
from flask_flatpages import FlatPages, pygments_style_defs

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FLATPAGES_MARKDOWN_EXTENSIONS = []
FLATPAGES_ROOT = 'content'
BLOG_PICTURES_FOLDER = 'static/img/posts/'
POST_DIR = 'posts'
PORT_DIR = 'portfolio'
app = Flask(__name__)
flatpages = FlatPages(app)
app.config.from_object(__name__)


@app.route("/")
def index():
    posts = [p for p in flatpages if p.path.startswith(POST_DIR)
             and not p.meta.get('archived', False)]
    posts.sort(key=lambda item: item['date'], reverse=True)
    for post in posts:
        picture_name = post.path.split('/')[-1] + '.png'
        if os.path.exists(BLOG_PICTURES_FOLDER + picture_name):
            post.meta['picture_path'] = BLOG_PICTURES_FOLDER + picture_name
        else:
            post.meta['picture_path'] = BLOG_PICTURES_FOLDER + 'blog-no-picture.png'

    recent_posts = posts.copy()
    recent_posts = recent_posts[:4]
    cards = [p for p in flatpages if p.path.startswith(PORT_DIR)]
    cards.sort(key=lambda item: item['title'])
    with open('settings.json', encoding='utf8') as config:
        data = config.read()
        settings = json.loads(data)

    tags = set()
    for p in flatpages:
        t = p.meta.get('tag')
        if t:
            tags.add(t.lower())

    return render_template('index.html', **settings,
                           posts=posts, recent_posts=recent_posts,
                           cards=cards, bigheader=True, tags=tags)


@app.route('/posts/<name>/')
def post(name):
    path = '{}/{}'.format(POST_DIR, name)
    post = flatpages.get_or_404(path)
    return render_template('post.html', post=post)


@app.route('/portfolio/<name>/')
def card(name):
    path = '{}/{}'.format(PORT_DIR, name)
    card = flatpages.get_or_404(path)
    return render_template('card.html', card=card)


@app.route('/pygments.css')
def pygments_css():
    return pygments_style_defs('monokai'), 200, {'Content-Type': 'text/css'}


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000, debug=True)
