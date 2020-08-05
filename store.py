import datetime
from peewee import SqliteDatabase, Model, DateField, CharField, IntegerField
db = SqliteDatabase('store.db')

class BaseModel(Model):
  class Meta:
    database = db

class Rating(BaseModel):
  rating_date = DateField()
  abiturient_name = CharField()
  education_form = IntegerField(default=1)
  financing_program = IntegerField()
  education_program = IntegerField()
  rating_all = IntegerField(default=0)
  rating_candidates = IntegerField(default=0)


def updateRatings(rating_date, abiturient_name, education_form, financing_program, education_program, rating_all=0, rating_candidates=0):
  """Update ratings to databse

  Return True if ratings changed
  """
  rating, created = Rating.get_or_create(
    rating_date = rating_date,
    abiturient_name = abiturient_name,
    education_form = education_form,
    financing_program = financing_program,
    education_program = education_program,
    defaults ={'rating_all': rating_all, 'rating_candidates': rating_candidates}
  )

  rating_all_changed = not (rating.rating_all == rating_all)
  rating_candidates_changed = not (rating.rating_candidates == rating_candidates)

  if(created == False):
    rating.rating_all = rating_all
    rating.rating_candidates = rating_candidates
    rating.save()

  return (rating_all_changed or rating_candidates_changed)

def getLastRating(rating_type,abiturient_name, education_form, financing_program, education_program):
  query = (Rating
    .select(Rating.rating_all,Rating.rating_candidates)
    .where(
      (Rating.abiturient_name == abiturient_name) &
      (Rating.education_form == education_form) &
      (Rating.financing_program == financing_program) &
      (Rating.education_program == education_program)
    )
    .order_by(Rating.rating_date.desc())
    .limit(1)
    )
  
  if query.count() == 0:
    return 0

  if rating_type == 'all':
    return query[0].rating_all
  else:
    return query[0].rating_candidates


#db.drop_tables([Rating])
db.create_tables([Rating])

# u = updateRatings(datetime.date.today(),'Мыцыкова Анна Алексеевна',1,1,12,)

# print(getLastRating('all','Мыцыкова Анна Алексеевна',1,1,12))

# for rating in Rating.select().dicts():
#   print(rating)

#abitur = Rating(rating_date = datetime.date.today(), abiturient_name = 'Анна Мыцыкова', financing_program = 1, education_program = 12)
#abitur.save()

