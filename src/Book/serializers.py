from rest_framework import serializers
from Book.models import Book, Menu, Chapter, Css

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model=Book 
        fields=('title', 'author')

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model=Menu 
        fields=('title', 'position', 'filename', 'book')

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model=Chapter 
        fields=('title', 'content', 'book')

class CssSerializer(serializers.ModelSerializer):
    class Meta:
        model=Css 
        fields=('title', 'content', 'book')