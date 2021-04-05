from news.models import news, TagsNValue, Category
from users.models import UserData
import random

def get_recommended_news(request):

    current_user = request.user

    # All the tags and value associated with current user is collected
    tagsNValue = TagsNValue.objects.filter(name = current_user.username).order_by('-value')

    # List of all news
    newses = news.objects.all()

    # Number of recommended news to show = (no. of news in popular news)/2
    a = newses.count()/2

    # Holds the list of news to recommend to the user
    news_to_recommend = []

    # for user find the total tag list:
    if tagsNValue.exists():
        user_tag_list=[]
        # Get list of all tags in that username.
        for tagvalue in tagsNValue:
            user_tag_list.append(tagvalue.tags)
    
        #if tag list is present in news then collect the news to show in the post:
        for n in newses:
            for user_tag in user_tag_list:
                if user_tag in n.tags and n not in news_to_recommend:
                    news_to_recommend.append(n)
                
        '''
            -------------------------TODO-------------------------------
            - Sort the news list according to the value of the tag
        '''
    
        

        # Some algorithm to get TOP-N recommendation needs to be implemented. 
        # For now we are just shuffling and truncating items from a list.
        random.shuffle(news_to_recommend)
        return news_to_recommend[: int(a)]

        # If user has no tags saved then
        # return a shuffled list of object from newses [10] to [15]
        # Later we can recommend popular news, or recommend according to
        # user's group (age, gender, location)
        # For now we dont have much news so we are returning same news 
        # for recommended and popular news if the user is new.

        '''
        ---------LOGIC TO ADD shuffled newses [10] to [15]------------
        else:
            a = []
            i = 5
            while(i>0):
                news_to_recommend.append(newses[10+i])
                i--
            random.shuffle(news_to_recommend)
        '''

    else:
        # Recommended news for new users:
        news_ = news.objects.order_by('?') # to get unordered/shuffled list

        # For every 2 popular news, there is 1 recommended news. 
        # So count of recommended news = no. of popular news/2
        # Just front end adjustments
        
        news_to_recommend = news_[:a]
        
        return news_to_recommend

def save_tags_and_value(request, tags):
    current_user = request.user

    tagsNValue = TagsNValue.objects.filter(name = current_user.username)

    tv_keys_list=[]
    if tagsNValue.exists():
        li = list(tags.split(","))
        # Get list of all keys of that username.
        for tvi in tagsNValue:
            tv_keys_list.append(tvi.tags)
       
        # for each list passed through link, compare the key in the list
        for item in li:

            # if list has the key then increment the value
            if item in tv_keys_list:
                tv_buf = TagsNValue.objects.get(name = current_user.username, tags = item)
                tv_buf.value = tv_buf.value + 1 
                tv_buf.save()
            
            # if list doesn't have the key then add the key and value = 1
            else :
                TagsNValue.objects.create(name = current_user.username, tags = item, value = 1)

    # If there is no keyvalue pair at all for the user, create one and add value 1 to each key
    else :
        li = list(tags.split(","))
        for item in li:
            TagsNValue.objects.create(name = current_user.username, tags = item, value = 1)


    
    # return render(request, 'news/news_detail.html', context)

def recommendationForUserInCookie(username, singlepagecat):
    '''
        pull news ids, check category for each id
        recommend according to number of news in specific category
        4 news to recommend so, if user is recommended 2 news from highest category
        and single news for next two category
        also count number of revisit to same news. 
    '''

    newsread = UserData.objects.filter(userID = username)

    if newsread.exists():

        categories_key = Category.objects.all()
        keys = []
        for key in categories_key:
            keys.append(key.title)

        # Also create a news dictionary, to check whether user has already read the news
        # don't recommend if they have already read the news. 
        
        category_dict = dict.fromkeys(keys,0)
        for n in newsread:
            category_name = news.objects.get(id=int(n.newsID)).category.title
            print(category_name)
            category_dict[category_name] = category_dict[category_name] + 1
        
        # print (category_dict)
        # sorted_category_dict={k: v for k, v in sorted(category_dict.items(), key=lambda item: item[1])}
        # print(sorted_category_dict)
        required_category=sorted(category_dict, key=category_dict.get, reverse=True)[:3]
        print(type(required_category[0]))
        recommended_news = []
        flag = 1
        for cat in required_category:
            # buffer_category = Category.object.get(title=cat)
            if flag == 1:
                # Check if user has already read the news. 
                buffer_news_list = news.objects.filter(category=Category.objects.get(title=cat))
                a = random.choice(buffer_news_list)
                recommended_news.append(a)
                b = random.choice(buffer_news_list)
                while True:
                    if b != a:
                        recommended_news.append(b)
                        break
                    b = random.choice(buffer_news_list)
                flag = 0
                # print(recommended_news)
            else:
                buffer_news_list = news.objects.filter(category=Category.objects.get(title=cat))
                recommended_news.append(random.choice(buffer_news_list))
        
        # print(recommended_news)

        return recommended_news

    else:
        # Recommended news for new users:
        news_ = news.objects.filter(category=singlepagecat)
        
        news_to_recommend = news_[:4]
        
        return news_to_recommend
    