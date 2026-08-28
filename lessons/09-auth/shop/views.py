from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from shop.forms import ProductForm, RegisterForm, ReviewForm
from shop.models import Category, Product


def _render_product_detail(request, product, review_form):
    context = {
        'page_title': product.name,
        'product': product,
        'reviews': product.reviews.all(),
        'review_form': review_form,
    }
    return render(request, 'shop/product_detail.html', context)


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
    review_form = ReviewForm() if request.user.is_authenticated else None
    return _render_product_detail(request, product, review_form)


@login_required
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


@login_required
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


@login_required
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


@login_required
def review_create(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.author_name = request.user.get_username()
            review.save()
            return redirect('product_detail', pk=product.pk)
        return _render_product_detail(request, product, form)

    return redirect('product_detail', pk=product.pk)


def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Добро пожаловать в Django Shop!')
            return redirect('home')
    else:
        form = RegisterForm()

    context = {
        'page_title': 'Регистрация',
        'form': form,
    }
    return render(request, 'shop/register.html', context)


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
