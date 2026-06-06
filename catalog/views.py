from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import CoffeeSort

def coffee_list(request):
    sorts = CoffeeSort.objects.filter(is_active=True)
    paginator = Paginator(sorts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'catalog/coffee_list.html', {'page_obj': page_obj})

def coffee_detail(request, slug):
    coffee = get_object_or_404(CoffeeSort, slug=slug, is_active=True)
    return render(request, 'catalog/coffee_detail.html', {'coffee': coffee})