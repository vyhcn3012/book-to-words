from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from bson import ObjectId
from Book.models import Book, Menu
from Book.serializers import BookSerializer, MenuSerializer, ChapterSerializer, CssSerializer
from Book.funtion_helpers import text_to_word

import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup, NavigableString
from PIL import Image
import os
import re

# Create your views here.
@csrf_exempt
def bookApi(request,id=0):
    if request.method=='GET':
        departments = Book.objects.all()
        departments_serializer=BookSerializer(departments,many=True)
        return JsonResponse(departments_serializer.data,safe=False)
    elif request.method=='POST':
        file = request.FILES['file']
        file_url = file.name
        with open(file_url, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        book = epub.read_epub(file_url)
        title = book.get_metadata('DC', 'title')[0][0]
        author = book.get_metadata('DC', 'creator')[0][0]
        departments_serializer=BookSerializer(data={'title':title,'author':author})

        if departments_serializer.is_valid():
            book_instance = departments_serializer.save()
            menuItems = get_book_menu(book)
            css = get_book_css(book)
            chapters = get_book_chapter(book, css['avoid'])
            for item in menuItems:
                menu_serializer=MenuSerializer(data={'title':item['title'],'position':item['position'],'filename':item['file_name'], 'book':str(book_instance.id)})
                if menu_serializer.is_valid():
                    menu_serializer.save()
                else:
                    print(menu_serializer.errors)

            for item in css['result']:
                css_serializer=CssSerializer(data={'title':item['file_name'],'content':item['content'], 'book':str(book_instance.id)})
                if css_serializer.is_valid():
                    css_serializer.save()
                else:
                    print(css_serializer.errors)

            for item in chapters:
                chapter_serializer=ChapterSerializer(data={'title':item['file_name'],'content':item['content'], 'book':str(book_instance.id)})
                if chapter_serializer.is_valid():
                    chapter_serializer.save()
                else:
                    print(chapter_serializer.errors)
                
        # delete file
        os.remove(file_url)
        
        if departments_serializer.is_valid():
            return JsonResponse("Added Successfully",safe=False)
        return JsonResponse("Failed to Add")
    elif request.method=='PUT':
        department_data=JSONParser().parse(request)
        department=Book.objects.get(DepartmentId=department_data['DepartmentId'])
        departments_serializer=BookSerializer(department,data=department_data)
        if departments_serializer.is_valid():
            departments_serializer.save()
            return JsonResponse("Updated Successfully",safe=False)
        return JsonResponse("Failed to Update")
    elif request.method=='DELETE':
        department=Book.objects.get(DepartmentId=id)
        department.delete()
        return JsonResponse("Deleted Successfully",safe=False)

def get_book_menu(book):
    menuItems = []
    position = 0
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_NAVIGATION:
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            for nav_point in soup.find_all('navpoint'):
                # Extract chapter titles from navpoint elements
                title = nav_point.find('navlabel').text
                # Get the HTML file name associated with this chapter
                content = nav_point.find('content')
                file_name = content['src'] if content else None
                file_names = f'{file_name}'.split('/')
                file_name = file_names[-1].split('.')[0] + '.html'
                position += 1
                menuItems.append({'title': title, 'file_name': file_name, 'position': position})

    return menuItems

def get_book_css(book):
    avoid = ['../../']
    result = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_STYLE:
            file_names = f'{item.file_name}'.split('/')

            merged = []
            for i in range(len(file_names) - 1):
                if file_names[i] == 'OEBPS':
                    merged.append('../')
                else:
                    merged.append(file_names[i] + "/")

            avoid.append("".join(merged))
            avoid = list(set(avoid))
            avoid = [item for item in avoid if item != '']

            result.append({'file_name': file_names[-1], 'content': item.get_content().decode("utf-8")})
    
    return {"result": result, "avoid": avoid}

def get_book_chapter(book, avoid):
    result = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            file_names = f'{item.file_name}'.split('/')
            file_name = file_names[-1].split('.')[0] + '.html'

            # Extract and save HTML content
            html_content = item.content.decode('utf-8')
            for item in avoid:
                html_content = re.sub(item, '', html_content)

            html_content = re.sub('xhtml', 'html', html_content)

            soup = BeautifulSoup(html_content, 'html.parser')
            # get all content and change to text
            for tag in soup.find_all():
                if tag.name == 'p':
                    if tag.find('img'):
                        continue
                    words = text_to_word(tag.text)
                    new_content = []
                    for word in words:
                        span_tag = soup.new_tag('span')
                        span_tag['class'] = word['type']
                        span_tag.append(NavigableString(word['text']))
                        new_content.append(span_tag)

                    tag.clear()

                    for span in new_content:
                        # print(span)
                        tag.append(span)
                        tag.append(' ')

            result.append({'file_name': file_name, 'content': str(soup)})

    return result

            

