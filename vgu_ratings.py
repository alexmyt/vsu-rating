import requests
from bs4 import BeautifulSoup
import store
import datetime

abiturient_name = "Мыцыкова Анна Алексеевна"
ratings_url = {'all': 'http://www.abitur.vsu.ru/data/simple_rating', 'candidates':'http://www.abitur.vsu.ru/data/candidates_rating'}
rating_url = "http://www.abitur.vsu.ru/data/simple_rating"
candidates_rating_url = "http://www.abitur.vsu.ru/data/candidates_rating"
education_forms = {1: 'Очная'}
financing_source = {1: 'Бюджет', 2: 'Договор'}
education_program = {12: 'Биология', 15: 'Почвоведение', 300: "Медицинская кибернетика"}

def get_rating(rating_type, form, source, program):
  url = "%s/%i_%i_%i.html" % (ratings_url[rating_type], form, source, program)

  cur_rating = -1
  updated = False
  r = requests.get(url)
  r.encoding = 'utf-8'
  if (r.status_code == 200):
    soup = BeautifulSoup(r.text,'lxml')
    div = soup.find('div',string=abiturient_name)
    if(div):
      cur_rating = int(div.find_parent('tr').td.text or 0)
      
  rating_all = 0
  rating_candidates = 0 
  if cur_rating > 0:
    if rating_type == 'candidates':
      rating_candidates = cur_rating
    else:
      rating_all = cur_rating
    
  updated = store.updateRatings(datetime.date.today(),abiturient_name,1,source,program,rating_all,rating_candidates)
  
  return cur_rating, updated

def fetch_all_ratings():
  any_updated = False

  for rating_type in ratings_url.keys():
    for source_id in financing_source:
      for program_id in education_program:
          rating, updated = get_rating(rating_type,1,source_id,program_id)
          any_updated = any_updated and updated

  return any_updated

def get_rating_doc():
  rating_doc = "Рейтинги абитуриента %s в Воронежском университете\n" % abiturient_name

  for rating_type in ratings_url.keys():
    if (rating_type == 'candidates'):
      rating_doc += "\nРейтинг подавших согласие:"
    else:
      rating_doc += "\nОбщий рейтинг:"

    for source_id in financing_source:
      for program_id in education_program:
        
        # first, get rating from database
        rating = store.getLastRating(rating_type,abiturient_name,1,source_id,program_id)

        # if not found - get from site
        if rating < 1:
          rating, updated = get_rating(rating_type,1,source_id,program_id)

        if (rating > 0): 
          rating_doc += "\n%s %s: %s" % (financing_source[source_id], education_program[program_id], rating)

    rating_doc += "\n"

  return rating_doc