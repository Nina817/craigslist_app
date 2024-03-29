from django.shortcuts import render
import requests
from . import models
from requests.compat import quote_plus
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required


# Create your views here.
BASE_CRAIGSLIST_URL = 'https://london.craigslist.org/d/housing/search/hhh?query={}'
BASE_IMAGE_URL = "https://images.craigslist.org/{}_600x450.jpg"


# @login_required
def home(request):
    return render(request, 'base.html')


# @login_required
def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')

    post_listings = soup.find_all('li', {'class': 'result-row'})

    final_postings = []

    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')

        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        if post.find(class_='result-image').get('data-ids') and not post.find(title_='no image'):
            post_image = post.find(class_='result-image').get('data-ids').split(",")[0].split(":")[1]
            # post_image2 = post_image[0].split(":")[1]
            image_url = BASE_IMAGE_URL.format(post_image)
        else:
            image_url = "https://i.stack.imgur.com/y9DpT.jpg"

        final_postings.append((post_title, post_url, post_price, image_url))



    stuff_for_frontend = {
        'search': search,
        'final_postings': final_postings,
    }

    # print(len(final_postings))
    return render(request, 'my_app/index.html', stuff_for_frontend)
