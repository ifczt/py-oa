# print(user_info.promotion.with_entities(Promotion.school_code).all())
import calendar
import datetime

from werkzeug.security import generate_password_hash


def get_xAxis(month=datetime.datetime.now().month):
    year = datetime.datetime.now().year
    data = []
    if month == datetime.datetime.now().month:
        day = datetime.datetime.now().day
        return list(range(1, day))
    else:
        day = calendar.monthrange(year, 1)[1]
        return list(range(1, day))

aa = get_xAxis()
print(aa)
stra ='2019-12-26 23:59:59'
print(datetime.datetime.strptime(stra))