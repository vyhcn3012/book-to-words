from django.http import JsonResponse
import os
from ebooklib import epub

def import_book(file):
    from Book.serializers import BookSerializer, MenuSerializer, CssSerializer, ChapterSerializer
    from Book.views import get_book_menu, get_book_css, get_book_chapter
    

    file_url = file.name
    with open(file_url, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    book = epub.read_epub(file_url)
    title = book.get_metadata('DC', 'title')[0][0]
    author = book.get_metadata('DC', 'creator')[0][0]
    departments_serializer = BookSerializer(data={'title': title, 'author': author})

    if departments_serializer.is_valid():
        book_instance = departments_serializer.save()
        menuItems = get_book_menu(book)
        css = get_book_css(book)
        chapters = get_book_chapter(book, css['avoid'])
        
        for item in menuItems:
            menu_serializer = MenuSerializer(
                data={'title': item['title'], 'position': item['position'], 'filename': item['file_name'], 'book': str(book_instance.id)})
            if menu_serializer.is_valid():
                menu_serializer.save()
            else:
                print(menu_serializer.errors)

        for item in css['result']:
            css_serializer = CssSerializer(
                data={'title': item['file_name'], 'content': item['content'], 'book': str(book_instance.id)})
            if css_serializer.is_valid():
                css_serializer.save()
            else:
                print(css_serializer.errors)

        for item in chapters:
            chapter_serializer = ChapterSerializer(
                data={'title': item['file_name'], 'content': item['content'], 'book': str(book_instance.id)})
            if chapter_serializer.is_valid():
                chapter_serializer.save()
            else:
                print(chapter_serializer.errors)

    # Clean up the uploaded file
    os.remove(file_url)

    if departments_serializer.is_valid():
        return JsonResponse("Added Successfully", safe=False)
    return JsonResponse("Failed to Add")
