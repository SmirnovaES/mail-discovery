from rest_framework import serializers
from mail.models import mails
#from datetime import datetime

class mailsSerializer(serializers.ModelSerializer):
  class Meta:
    model = mails
#    fields = ('Id', 'Date', 'NameFrom', 'AddressFrom', 'NameTo', 'AddressTo', 'Subject', 'Message')
    fields = ('Date', 'NameFrom', 'AddressFrom', 'NameTo', 'AddressTo', 'Subject', 'Message')


#class LetterSerializer(serializers.Serializer):
#    id = serializers.IntegerField(read_only=True)
#    rev_time = serializers.DateTimeField(default=datetime.now)
#    topic = serializers.CharField(max_length=100, default='mail topic')
#    body = serializers.CharField(required=False, allow_blank=True, default='It is message body.')
#    sender = serializers.CharField(required=False, allow_blank=True, default='mr. sender', max_length=100)
#    receiver = serializers.CharField(required=False, allow_blank=True, default='mr. receiver', max_length=100)

    

    def create(self, validated_data):
        """
        Create and return a new `Letter` instance, given the validated data.
        """
        return mails.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Letter` instance, given the validated data.
        """
#        instance.Id = validated_data.get('Id', instance.Id)
        instance.Date = validated_data.get('Date', instance.Date)
        instance.NameFrom = validated_data.get('NameFrom', instance.NameFrom)
        instance.AddressFrom = validated_data.get('AddressFrom', instance.AddressFrom)
        instance.NameTo = validated_data.get('NameTo', instance.NameTo)
        instance.AddressTo = validated_data.get('AddressTo', instance.AddressTo)
        instance.Subject = validated_data.get('Subject', instance.Subject)
        instance.Message = validated_data.get('Message', instance.Message)
        instance.save()
        return instance
