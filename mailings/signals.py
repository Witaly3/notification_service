from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q

from .models import Mailing, Client, Message
from .tasks import send_message


@receiver(post_save, sender=Mailing, dispatch_uid="create_message")
def create_message(sender, instance, created, **kwargs):
    if created:
        mailing = Mailing.objects.filter(id=instance.id).first()
        clients = Client.objects.filter(Q(mobile_operator_code=mailing.mobile_operator_code) |
                                        Q(tag=mailing.tag)).all()
        
        for client in clients:
            Message.objects.create(
                sending_status="No sent",
                client_id=client.id,
                mailing_id=instance.id
            )
            message = Message.objects.filter(mailing_id=instance.id, client_id=client.id).first()
            data = {
                'id': message.id,
                "phone": client.phone_number,
                "text": mailing.text
            }
            client_id = client.id
            mailing_id = mailing.id
            
            if instance.to_send:
                send_message.apply_async((data, client_id, mailing_id),
                                         expires=mailing.date_end)
            else:
                send_message.apply_async((data, client_id, mailing_id),
                                         eta=mailing.date_start, expires=mailing.date_end)

            
