import requests
from bs4 import BeautifulSoup

abiturient_name = "Мыцыкова Анна Алексеевна"
rating_url = "http://www.abitur.vsu.ru/data/simple_rating"
candidates_rating_url = "http://www.abitur.vsu.ru/data/candidates_rating"
education_forms = {1: 'Очная'}
financing_source = {1: 'Бюджет', 2: 'Договор'}
education_program = {12: 'Биология', 15: 'Почвоведение', 300: "Медицинская кибернетика"}

def get_rating(url, form, source, program):
  url = "%s/%i_%i_%i.html" % (url, form, source, program)

  cur_rating = -1
  r = requests.get(url)
  r.encoding = 'utf-8'
  if (r.status_code == 200):
    soup = BeautifulSoup(r.text,'lxml')
    div = soup.find('div',string=abiturient_name)
    if(div):
      cur_rating = int(div.find_parent('tr').td.text or 0)

  return(cur_rating)

def get_rating_doc():
  rating_doc = "Рейтинги абитуриента %s в Воронежском университете\n" % abiturient_name

  for rating_type in [candidates_rating_url, rating_url]:
    if (rating_type == candidates_rating_url):
      rating_doc += "\nРейтинг подавших согласие:"
    else:
      rating_doc += "\nОбщий рейтинг:"

    for source_id in financing_source:
      for program_id in education_program:
        rating = get_rating(rating_type,1,source_id,program_id)
        if (rating > 0): 
          rating_doc += "\n%s %s: %s" % (financing_source[source_id], education_program[program_id], rating)

    rating_doc += "\n"

  return(rating_doc)
