import sys
import urllib.request

from bs4 import BeautifulSoup


class Scrapper:
    def __init__(self, website_url: str):
        self.website_url = website_url

        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    def check_website_status(self):
        print("checking website url ", self.website_url)
        request = urllib.request.Request(self.website_url, headers=self.headers)
        page = urllib.request.urlopen(request)
        soup = BeautifulSoup(page, 'html.parser')

        response = []

        parent_div = soup.find('div', class_='btools-matches')
        if parent_div:
            divs_with_class = parent_div.find_all('div', class_='btools-match')
            if divs_with_class:
                for index, div in enumerate(divs_with_class, start=1):
                    bet_object = {}
                    header = div.find('ul', class_='match-breadcrumbs t-ellipsis')
                    if header:
                        date = header.find('li', class_='match-breadcrumbs__date').text.strip()
                        location = header.find('li', class_='match-breadcrumbs__item').find('a',
                                                                                            class_="match-breadcrumbs__link").text.strip()
                        league = header.find('li', class_='match-breadcrumbs__item t-ellipsis').find('a',
                                                                                                     class_='match-breadcrumbs__link t-ellipsis').text.strip()

                        bet_object.update({'location': location, 'league': league, 'date': date})

                    teams_header = div.find('div', class_='btools-match__body').find('div',
                                                                                     class_='btools-match-teams').find(
                        'p').find('a')

                    type_of_bet = div.find('div',class_='btools-match-teams').find('span').text.strip().split(" ")
                    print("->{}<-".format(type_of_bet))

                    odds = div.find('div', class_='d-flex').find_all('div', class_='btools-odd-mini__value')
                    logos = div.find_all('div', class_='btools-odd-mini')
                    test_list = []
                    logos_list = []
                    for odd in odds:
                        test_list.append(odd.find('span').text)

                    for logo in logos:
                        logos_list.append(get_logo_website(logo_url=logo.find('img').get('data-src')))

                    if teams_header and odds:
                        teams_list = teams_header.text.strip().splitlines()
                        teams_list = [part.strip() for part in teams_list]
                        profit = div.find('span', class_='sure-bet-cta__inner').text.split("%")[0]
                        bet_object.update({'team1': {'name': teams_list[0],
                                                     'odd': test_list[0],
                                                     'house': logos_list[0]},
                                           'team2': {'name': teams_list[-1],
                                                     'odd': test_list[1],
                                                     'house': logos_list[1]},
                                           'type_of_bet': ' '.join(type_of_bet),
                                           'profit': profit})
                    response.append(bet_object)

        return response


def get_logo_website(logo_url: str) -> str:
    if 'betano' in logo_url:
        return 'betano'
    elif '22bet' in logo_url:
        return '22bet'
    elif 'bwin' in logo_url:
        return 'bwin'
    elif 'betway' in logo_url:
        return 'betway'
    elif 'betclic' in logo_url:
        return 'betclic'
    else:
        return logo_url


if __name__ == '__main__':
    scrapper = Scrapper(website_url='https://oddspedia.com/br/apostas-certas')
    resp = scrapper.check_website_status()
    print(resp)
