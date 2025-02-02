from rest_framework import serializers
from .models import *

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields=['id','post','username','comment_text','created_at']


class PostSerializer(serializers.ModelSerializer):
    comments=CommentSerializer(many=True, read_only=True)
    #역참조가 comments였으므로 comments로 가져와야됨 
    
    class Meta:
        model=Post
        fields=['id','title','date','body','language','comments']

