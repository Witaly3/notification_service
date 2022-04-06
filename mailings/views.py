from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets

from .models import Mailing, Client, Message
from .serializers import MailingSerializer, ClientSerializer, MessageSerializer


class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()


class MailingViewSet(viewsets.ModelViewSet):
    serializer_class = MailingSerializer
    queryset = Mailing.objects.all()

    @action(detail=True, methods=['get'])
    def info(self, request, pk=None):
        """
        Summary data for a specific mailing list
        """
        queryset_mailing = Mailing.objects.all()
        get_object_or_404(queryset_mailing, pk=pk)
        queryset = Message.objects.filter(mailing_id=pk).all()
        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def fullinfo(self, request):
        """
        Summary data for all mailings
        """
        total_count = Mailing.objects.count()
        mailing = Mailing.objects.values('id')
        content = {'Total number of mailings': total_count,
                   'The number of messages sent': ''}
        result = {}
        
        for row in mailing:
            res = {'Total messages': 0, 'Sent': 0, 'No sent': 0}
            mail = Message.objects.filter(mailing_id=row['id']).all()
            group_sent = mail.filter(sending_status='Sent').count()
            group_no_sent = mail.filter(sending_status='No sent').count()
            res['Total messages'] = len(mail)
            res['Sent'] = group_sent
            res['No sent'] = group_no_sent
            result[row['id']] = res
        
        content['The number of messages sent'] = result
        return Response(content)
