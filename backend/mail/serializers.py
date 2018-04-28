from rest_framework import serializers
from mail.models import mails
#from datetime import datetime

class mailsSerializer(serializers.ModelSerializer):
  class Meta:
    model = mails
    fields = ('id', 'date', 'addressfrom', 'addressto', 'subject', 'message')
#    fields = ('Date', 'NameFrom', 'AddressFrom', 'NameTo', 'AddressTo', 'Subject', 'Message')


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
        instance.Id = validated_data.get('id', instance.Id)
        instance.Date = validated_data.get('date', instance.Date)
        instance.AddressFrom = validated_data.get('addressfrom', instance.AddressFrom)
        instance.AddressTo = validated_data.get('addressto', instance.AddressTo)
        instance.Subject = validated_data.get('subject', instance.Subject)
        instance.Message = validated_data.get('message', instance.Message)
        instance.save()
        return instance
