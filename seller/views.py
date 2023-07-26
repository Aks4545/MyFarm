from django.contrib import messages
from django.shortcuts import get_object_or_404, render,redirect
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from items.forms import CategoryForm, ProductForm
from items.models import  product,category
from .forms import sellerform
from .models import seller
from django.contrib.auth.decorators import login_required,user_passes_test
from accounts.views import check_role_vendor
from django.template.defaultfilters import slugify

# Create your views here.



def get_vendor(request):
    vendor = seller.objects.get(user=request.user)
    return vendor


@login_required(login_url = 'login')
@user_passes_test(check_role_vendor)
def vprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(seller, user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = sellerform(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'Settings updated.')
            return redirect('vprofile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form = UserProfileForm(instance = profile)
        vendor_form = sellerform(instance=vendor)

    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile': profile,
        'vendor': vendor,
    }
    return render(request, 'vendor/vprofile.html',context )


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def product_add(request):
    vendor = get_vendor(request)
    categories = category.objects.filter(vendor=vendor).order_by('created_at')
    context = {
        'categories': categories,
    }
    return render(request,'vendor/product_add.html',context)



@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def product_by_category(request, pk=None):
    vendor = get_vendor(request)
    categories = get_object_or_404(category, pk=pk)
    Products = product.objects.filter(vendor=vendor , category=categories)
    context = {
        'Products': Products,
        'category': category,
    }
    return render(request, 'vendor/product_by_category.html', context)



@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_category(request):
    
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            
            category.save() # here the category id will be generated
            category.slug = slugify(category_name)+'-'+str(category.id)
            category.save()
            messages.success(request, 'Category added successfully!')
            return redirect('product_add')
        else:
            print(form.errors)

    else:
        form = CategoryForm()
    context = {
        'form': form,
    }
    return render(request, 'vendor/add_category.html', context)


def edit_category(request,pk=None):
    categories = get_object_or_404(category,pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST,instance=categories)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            categories = form.save(commit=False)
            categories.vendor = get_vendor(request)
            
            categories.save() # here the category id will be generated
            categories.slug = slugify(category_name)+'-'+str(categories.id)
            categories.save()
            messages.success(request, 'Category Updated successfully!')
            return redirect('product_add')
        else:
            print(form.errors)

    else:
        form = CategoryForm(instance=categories)
    context = {
        'form': form,
        'categories':categories,
    }
    return render(request,'vendor/edit_category.html',context)


def delete_category(request,pk=None):
    Category = get_object_or_404(category,pk=pk)
    Category.delete()
    messages.success(request, 'Category Deleted successfully!')
    return redirect('product_add')




@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            foodtitle = form.cleaned_data['product_title']
            food = form.save(commit=False)
            food.vendor = get_vendor(request)
            food.slug = slugify(foodtitle)
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('product_by_category', food.category.id)
        else:
            print(form.errors)
    else:
        form = ProductForm()
        # modify this form
        form.fields['category'].queryset = category.objects.filter(vendor=get_vendor(request))
    context = {
        'form': form,
    }
    return render(request, 'vendor/add_product.html', context)



@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_product(request, pk=None):
    prod = get_object_or_404(product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=prod)
        if form.is_valid():
            producttitle = form.cleaned_data['product_title']
            prod = form.save(commit=False)
            prod.vendor = get_vendor(request)
            prod.slug = slugify(producttitle)
            form.save()
            messages.success(request, 'product updated successfully!')
            return redirect('product_by_category', prod.category.id)
        else:
            print(form.errors)

    else:
        form = ProductForm(instance=prod)
        form.fields['category'].queryset = category.objects.filter(vendor=get_vendor(request))
    context = {
        'form': form,
        'prod': prod,
    }
    return render(request, 'vendor/edit_product.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_product(request, pk=None):
    prod = get_object_or_404(product, pk=pk)
    prod.delete()
    messages.success(request, 'product has been deleted successfully!')
    return redirect('product_by_category', prod.category.id)




