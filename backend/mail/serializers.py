from rest_framework import serializers
from mail.models import Letter
from datetime import datetime

class LetterSerializer(serializers.ModelSerializer):
  class Meta:
    model = Letter
    fields = ('id', 'date_rec', 'topic', 'body', 'sender', 'receiver')

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
        return Letter.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Letter` instance, given the validated data.
        """
        instance.date_rec = validated_data.get('date_rec', instance.date_rec)
        instance.topic = validated_data.get('topic', instance.topic)
        instance.body = validated_data.get('body', instance.body)
        instance.sender = validated_data.get('sender', instance.sender)
        instance.receiver = validated_data.get('receiver', instance.receiver)
        instance.save()
        return instance
