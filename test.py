# print(user_info.promotion.with_entities(Promotion.school_code).all())
from werkzeug.security import generate_password_hash

from settings import POWER_ROLES, POWER_ROLES_DICT, PUBLICIST, CAN_SEE_ALL_ORDERS

power = POWER_ROLES[1]
index = POWER_ROLES.index(power)
for i in range(index+1, POWER_ROLES_DICT.__len__()):
    print(POWER_ROLES_DICT[i])

print('PUBLICIST' in CAN_SEE_ALL_ORDERS)