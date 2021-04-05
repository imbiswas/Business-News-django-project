import requests
import json
from news.models import news
from news.models import Images, Category
from django.core.files import File  # you need this somewhere
import urllib.request
from django.utils.text import slugify
import os
import shutil
from django.conf import settings

shots_url = 'https://www.news24nepal.tv/wp-json/appharurest/v2/posts/7/'

tags = ['technology', 'festival', 'electronics', 'economics','general', 'business', 'gadgets']
# Done this in django shell:
'''
for t in tags:
    Category.objects.create(title = t, slug = slugify(t))
'''

def loadOnce():

    # Call this from the django shell when you dont have any item
    # load to the database from page 1 to 5
    i = 1

    while(i<=5):

        # Add pages to the url:
        pagei_url = shots_url +(str(i))

        # request the URL and parse the JSON
        response = requests.get(pagei_url)
        response.raise_for_status()# raise exception if invalid response
        json_list = response.json()
        # print(json_list[0]['title']) # prints: जुम्लामा मार्सी चामल भित्र्याउन भ्याइ नभ्याई

        # within the while loop first load from the web and store
        j = len(json_list) - 1

        while(j>=0):

            # Author name
            auth = json_list[j]['desc'].split()
            auth = auth[0]+' '+auth[1]

            # Getting the Image name
            imgurl_split = json_list[j]['image_link_medium'].split('/')
            img_name = imgurl_split[len(imgurl_split) - 1]


            tags_index = j%7

            #save news here
            news.objects.create(Heading = json_list[j]['title'],
                News = json_list[j]['body'],
                timestamp = json_list[j]['date'],
                tags = tags[tags_index],
                category = Category.objects.get(title = tags[tags_index]),
                author = auth,
                excerpt = json_list[j]['desc'])
            
            
            # -----Download image to local directory-----

            # Image's url on the web
            image_url = json_list[j]['image_link_medium']

            # Downloaded Image location
            dw_loc = settings.MEDIA_ROOT + '/downloaded_images'

            r = requests.get(image_url, 
                stream=True,
                headers={'User-agent': 'Mozilla/5.0'}
                )
            if r.status_code == 200:
                with open(dw_loc+'/'+img_name, 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)

            # Saving image for the news
            im = Images()
            im.News = news.objects.get(Heading = json_list[j]['title'])
            im.image.save(
                    os.path.basename(settings.MEDIA_ROOT +'/images/'+img_name), # Saving location of an image
                    File(open(dw_loc+'/'+img_name, 'rb'))) # downloaded location of images
            im.save()

            j = j-1

        i += 1 
