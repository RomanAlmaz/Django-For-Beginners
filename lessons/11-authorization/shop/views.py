from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from shop.forms import (
    ProductForm,
    ProfileForm,
    RegisterForm,
    ReviewForm,
    UserDetailsForm,
)
from shop.models import Category, Product, Profile, Review


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
            review.save()
            messages.success(request, 'Отзыв добавлен.')
            return redirect('product_detail', pk=product.pk)
        return _render_product_detail(request, product, form)

    return redirect('product_detail', pk=product.pk)


@login_required
def review_update(request, pk, review_pk):
    product = get_object_or_404(Product, pk=pk)
    review = get_object_or_404(Review, pk=review_pk, product=product)

    if review.user != request.user:
        raise Http404

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Отзыв обновлен.')
            return redirect('product_detail', pk=product.pk)
    else:
        form = ReviewForm(instance=review)

    context = {
        'page_title': 'Редактировать отзыв',
        'form': form,
        'product': product,
        'review': review,
    }
    return render(request, 'shop/review_form.html', context)


@login_required
def review_delete(request, pk, review_pk):
    product = get_object_or_404(Product, pk=pk)
    review = get_object_or_404(Review, pk=review_pk, product=product)

    if review.user != request.user:
        raise Http404

    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Отзыв удален.')
        return redirect('product_detail', pk=product.pk)

    context = {
        'page_title': 'Удалить отзыв',
        'product': product,
        'review': review,
    }
    return render(request, 'shop/review_confirm_delete.html', context)


@login_required
def profile(request):
    profile_obj, _ = Profile.objects.get_or_create(user=request.user)
    reviews = Review.objects.filter(user=request.user)

    context = {
        'page_title': 'Мой профиль',
        'profile': profile_obj,
        'reviews': reviews,
    }
    return render(request, 'shop/profile.html', context)


@login_required
def profile_edit(request):
    profile_obj, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserDetailsForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=profile_obj)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Профиль обновлен.')
            return redirect('profile')
    else:
        user_form = UserDetailsForm(instance=request.user)
        profile_form = ProfileForm(instance=profile_obj)

    context = {
        'page_title': 'Редактировать профиль',
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'shop/profile_form.html', context)


def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
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
