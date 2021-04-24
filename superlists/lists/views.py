from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item, List

# Create your views here.
def home_page(request):
    return render(request, 'home.html')

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    try:
        items = Item.objects.filter(list=list_)
    except Exception as ep:
        items = []
    return render(request, 'lists.html', {'items': items})

def new_list(request):
    if(request.method == 'POST'):
        # 將資料存入db
        list_ = List.objects.create()
        Item.objects.create(
            text=request.POST.get('item_text', ""),
            list=list_
        ) # 可以直接create 這樣就不用 new then save()
        return redirect('/lists/%d/' % (list_.id,))

