# for uid errors


import os
import django
import uuid

# Django ayarlarını yapılandır
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'haftaici.settings')
django.setup()

from apps.users.models import CustomUser

def update_uids():
    users = CustomUser.objects.all()
    for user in users:
        user.uid = uuid.uuid4()
        user.save()

if __name__ == '__main__':
    update_uids()
    print("Tüm kullanıcıların uid alanları güncellendi.")

