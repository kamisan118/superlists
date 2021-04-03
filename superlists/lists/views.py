from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item

# Create your views here.
def home_page(request):
    if(request.method == 'POST'):
        # 將資料存入db
        Item.objects.create(text=request.POST.get('item_text', "")) # 可以直接create 這樣就不用 new then save()
        return redirect('/lists/the-only-list-in-the-world')

    return render(request, 'home.html')

def view_list(request):
    items = Item.objects.all()
    return render(request, 'lists.html', {'items': items})