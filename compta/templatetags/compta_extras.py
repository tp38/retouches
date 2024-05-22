from django import template

register = template.Library()



def twodigits(value):
    if value < 10 :
        return '0'+str(value)
    else:
        return str(value)

register.filter("twodigits", twodigits)
