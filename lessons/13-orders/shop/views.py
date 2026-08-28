from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from shop.cart import (
    add_to_cart,
    get_cart_lines,
    is_product_in_cart,
    remove_from_cart,
    update_cart_item,
)
from shop.forms import (
    ProductForm,
    ProfileForm,
    RegisterForm,
    ReviewForm,
    UserDetailsForm,
)
from shop.models import Category, Order, Product, Profile, Review
from shop.orders import create_order_from_cart


def _render_product_detail(request, product, review_form):
    context = {
        'page_title': product.name,
        'product': product,
        'reviews': product.reviews.all(),
        'review_form': review_form,
        'product_has_orders': product.order_items.exists(),
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
    # OrderItem.product использует on_delete=PROTECT: товар из заказа нельзя
    # стереть из БД. Проверяем заранее, чтобы новичок увидел понятное сообщение,
    # а не страницу ошибки Django.
    has_orders = product.order_items.exists()

    if request.method == 'POST':
        if has_orders:
            messages.error(
                request,
                'Нельзя удалить товар: он уже есть в заказах.',
            )
            return redirect('product_detail', pk=product.pk)
        product.delete()
        return redirect('products')

    context = {
        'page_title': 'Удалить товар',
        'product': product,
        'has_orders': has_orders,
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


def cart_detail(request):
    lines, total = get_cart_lines(request.session)
    context = {
        'page_title': 'Корзина',
        'cart_lines': lines,
        'cart_total': total,
    }
    return render(request, 'shop/cart.html', context)


@require_POST
def cart_add(request, pk):
    product = get_object_or_404(Product, pk=pk)
    quantity = request.POST.get('quantity', '1')
    add_to_cart(request.session, product.pk, quantity)
    messages.success(request, f'«{product.name}» добавлен в корзину.')
    return redirect('product_detail', pk=product.pk)


@require_POST
def cart_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    quantity = request.POST.get('quantity', '1')
    update_cart_item(request.session, product.pk, quantity)
    if not is_product_in_cart(request.session, product.pk):
        messages.success(request, f'«{product.name}» удалён из корзины.')
    else:
        messages.success(request, 'Количество обновлено.')
    return redirect('cart')


@require_POST
def cart_remove(request, pk):
    product = get_object_or_404(Product, pk=pk)
    remove_from_cart(request.session, product.pk)
    messages.success(request, f'«{product.name}» удалён из корзины.')
    return redirect('cart')


@login_required
def checkout(request):
    cart_lines, cart_total = get_cart_lines(request.session)
    if not cart_lines:
        messages.warning(request, 'Корзина пуста. Добавьте товары перед оформлением.')
        return redirect('cart')

    if request.method == 'POST':
        order = create_order_from_cart(request.user, request.session)
        if order is None:
            messages.warning(request, 'Корзина пуста. Добавьте товары перед оформлением.')
            return redirect('cart')
        messages.success(request, f'Заказ #{order.pk} оформлен.')
        return redirect('order_detail', pk=order.pk)

    context = {
        'page_title': 'Оформление заказа',
        'cart_lines': cart_lines,
        'cart_total': cart_total,
    }
    return render(request, 'shop/checkout.html', context)


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    context = {
        'page_title': 'Мои заказы',
        'orders': orders,
    }
    return render(request, 'shop/order_list.html', context)


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if order.user != request.user:
        raise Http404

    context = {
        'page_title': f'Заказ #{order.pk}',
        'order': order,
    }
    return render(request, 'shop/order_detail.html', context)


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
