from django.shortcuts import render, redirect, get_object_or_404

from products.forms import ProductForm, ComponentForm
from products.models import Product, ProductComponent
from products.services.ProductService import ProductService


def list_products(request):
    all_products = ProductService.get_products()
    context = {'products': all_products}
    return render(request, 'products/products.html', context)


def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            print(f"Created Product: {product}")

            return redirect('products')
        else:
            print("Invalid form:")
            print(form.errors)

    else:
        form = ProductForm()

    context = {'form': form}
    return render(request, 'products/product-form.html', context)


def remove_component(request, pk, component_id):
    if request.method == 'POST':
        # Busca o componente específico
        component = get_object_or_404(ProductComponent, id=component_id, parent_product__id=pk)
        component.delete()  # Remove o componente
        return redirect('get_product', pk=pk)
    else:
        return redirect('get_product', pk=pk)


def get_product(request, pk):
    product: Product = ProductService.get_product_by_id(pk)
    notUpdatedComponents = product.components.all()
    components_form = []
    for component in notUpdatedComponents:
        components_form.append(ComponentForm(instance=component))

    if request.method == 'POST':
        print(request.POST)
        product_form = ProductForm(request.POST, instance=product)

        if product_form.is_valid():
            savedProduct = product_form.save()
            # notUpdatedComponents = savedProduct.components.all()

            # components_form = []
            # for component in notUpdatedComponents:
            #     comp_form = ComponentForm(instance=component)
            #     components_form.append(comp_form)
            #     comp_form.save()

            return redirect('products')
        else:
            print("Invalid form:")
            print(product_form.errors)
    else:
        product_form = ProductForm(instance=product)

    context = {'form': product_form, 'components_form': components_form}
    return render(request, 'products/product-form.html', context)


def foo(request):
    pk = "2cd57510-cdd9-448d-afb6-d38e271fcd45"
    parent_product_components = ProductService.get_product_by_id(pk).components_list

    # current_components = [{"id": c.id, "quantity": c.quantity} for c in parent_product_components]

    all_components = ProductService.get_products()

    context = {'components': all_components, }

    return render(request, '', context)
