from django.shortcuts import get_object_or_404, redirect, render

from shop.forms import ProductForm
from shop.models import Category, Product


def home(request):
    context = {
        'page_title': 'Главная',
        'welcome_message': (
            'Добро пожаловать в Django Shop! Это главная страница нашего магазина.'
        ),
        'categories': Category.objects.all(),
        'featured_products': Product.objects.filter(is_featured=True),
    }
    return render(request, 'shop/home.html', context)


def products(request):
    context = {
        'page_title': 'Товары',
        'products': Product.objects.all(),
    }
    return render(request, 'shop/products.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {
        'page_title': product.name,
        'product': product,
    }
    return render(request, 'shop/product_detail.html', context)


def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm()

    context = {
        'page_title': 'Добавить товар',
        'form': form,
    }
    return render(request, 'shop/product_form.html', context)


def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)

    context = {
        'page_title': 'Редактировать товар',
        'form': form,
        'product': product,
    }
    return render(request, 'shop/product_form.html', context)


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.delete()
        return redirect('products')

    context = {
        'page_title': 'Удалить товар',
        'product': product,
    }
    return render(request, 'shop/product_confirm_delete.html', context)


def about(request):
    context = {
        'page_title': 'О сайте',
        'about_text': (
            'Django Shop - учебный проект для пошагового изучения Django.'
        ),
        'team_members': [
            'Roman - автор курса',
            'Django - наш любимый фреймворк',
        ],
    }
    return render(request, 'shop/about.html', context)


def contact(request):
    context = {
        'page_title': 'Контакты',
        'contact_text': (
            'Свяжитесь с нами по вопросам курса или проекта Django Shop.'
        ),
        'email': 'hello@djangoshop.example',
    }
    return render(request, 'shop/contact.html', context)
