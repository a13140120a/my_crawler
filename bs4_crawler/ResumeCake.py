import requests
from bs4 import BeautifulSoup

# get a list of user id from each resume page
def get_user_id(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}
    res = requests.get(url, headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    list_of_userId = []
    items = soup.findAll(class_="item-link")
    for i in items:
        # print(i.extract())
        result = i.attrs["href"]
        if not result.startswith('/resumes/'):
            userId = result[1:]
            list_of_userId.append(userId)

    return list_of_userId


# get text data from each user
def get_cv_text(url_user):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}
    res = requests.get(url_user, headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    result = soup.get_text()
    return result


def main():
    url = 'https://www.cakeresume.com/resumes?page=' + '1'
    lst_users = get_user_id(url)
    print(lst_users)

    print('='*20)

    url_user = 'https://www.cakeresume.com/' + 'bolaslien'
    user_text = get_cv_text(url_user)
    print(user_text)


if __name__ == '__main__':
    main()