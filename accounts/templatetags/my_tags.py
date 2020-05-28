from django import template
import datetime
register = template.Library()


def age(birthday):
    today = datetime.date.today()
    return (today.year - birthday.year) - int((today.month, today.day) < (birthday.month, birthday.day))


def get_partner(user, chat):
    for partner in chat.members.all():
        if partner != user:
            return partner
    return None


register.simple_tag(get_partner)
register.filter('age', age)