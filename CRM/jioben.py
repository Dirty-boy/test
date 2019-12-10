
import os

if __name__ == '__main__':

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CRM.settings")
    import django
    django.setup()

    import random
    from main import models

    c_list = []

    for i in range(521):

        obj = models.Customer(
            qq=f'{i+11}{i+22}{i+33}',
            name='方伯仁%s'%i,
            course=['PythonFullStack',],

        )
        c_list.append(obj)
    models.Customer.objects.bulk_create(c_list)













