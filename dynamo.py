from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute


class Ngrok(Model):
    class Meta:
        region = 'us-west-2'
        aws_access_key_id = 'AKIAV75AMAC5Q73LDO76'
        aws_secret_access_key = '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'
        table_name = 'Ngrok'
    url = UnicodeAttribute(hash_key=True)
    url_val = UnicodeAttribute(null=True, attr_name='url_val')


def get_ngrok_url():
    thread_item = Ngrok.get('ngrok_url')
    return thread_item.url_val


def get_bff_url():
    thread_item = Ngrok.get('bff_url')
    return thread_item.url_val
# if Thread.exists():
#     Thread.delete_table()
# if not Ngrok.exists():
#     Ngrok.create_table(read_capacity_units=1,
#                        write_capacity_units=1, wait=True)
# thread_item = Ngrok('ngrok_url', url_val='http://test.com')
# thread_item.save()

# thread_item = Ngrok.get('ngrok_url')
# thread_item.update(actions=[Ngrok.url_val.set("http:test2.com")])
# print(thread_item.url_val)
