from category.models import Category

def categoryMenu(request):
    categoryList = Category.objects.all()
    return dict(categoryList=categoryList)
