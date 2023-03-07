from bs4 import BeautifulSoup
import lxml
import requests

# import request

url = ['https://www.amazon.in/Samsung-Mystique-Storage-Purchased-Separately/product-reviews/B09TWGDY4W/ref' \
       '=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews']
# https://www.amazon.in/Samsung-Mystique-Storage-Purchased-Separately/product-reviews/B09TWGDY4W/ref
# =cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber=2

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 "
                  "Safari/537.36",
    "Accept-Language": "en-US,en;q=0.5"
}

count = 1
for i in range(440):

    link = ''
    for letter in url[0]:

        if link[-2:] == 'dp':
            link = link.replace('dp', 'arp')
        if link[-8:] == 'show_all':
            link = link.replace('show_all', 'paging')

        if count >= 1 and link == 'https://www.amazon.in/Samsung-Mystique-Storage-Purchased-Separately/product-reviews' \
                                  '/B09TWGDY4W/ref=cm_cr_arp_d_paging_btm':
            link += f'_next_{count + 1}?'
            count += 1
        else:
            link += letter
        if link[-11:] == 'all_reviews':
            link += f'&pageNumber={count}'

    url.append(link)

reviews_lst = []
for samsung_link in url:
    # print(samsung_link)
    response = requests.get(samsung_link, headers=header)
    samsung_web = response.text
    soup = BeautifulSoup(samsung_web, 'lxml')
    for review in soup.find_all(name='span', class_='a-size-base review-text review-text-content'):
        reviews_lst.append(review.getText())
        # with open('review.csv', 'a', encoding='utf-8') as file:
        #     file.write(review.getText())
        # # print(review.getText())
for review in reviews_lst:
    if review == '\n':
        reviews_lst.remove('\n')
# print(reviews_lst)
with open('reviews.csv', 'a', encoding='utf-8') as file:
    for review in reviews_lst:
        file.write(review)

