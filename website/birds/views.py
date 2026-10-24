from django.shortcuts import (
    render,
    get_object_or_404
)

from django.core.paginator import (
    Paginator
)

from .models import Bird


# ==========================================
# LANDING PAGE
# ==========================================

def landing_page(request):

    total_birds = Bird.objects.count()

    migratory_birds = Bird.objects.filter(

    migratory_status__in=[

        "Winter Migratory",

        "Summer Migratory",

        "Rare Visitor"
    ]

).count()

    regions = Bird.objects.values_list(

        'region',

        flat=True

    ).distinct().count()

    categories = Bird.objects.values_list(

        'category',

        flat=True

    ).distinct().count()
    

    return render(

        request,

        'birds/landing.html',

        {

            'total_birds': total_birds,

            'migratory_birds':
                migratory_birds,

            'regions': regions,

            'categories': categories
        }
    )
def gallery(request):

    return render(

        request,

        'birds/gallery.html'
    )
def about(request):

    return render(

        request,

        'birds/about.html'
    )
def contact(request):

    return render(

        request,

        'birds/contact.html'
    )
# ==========================================
# HOME PAGE
# ==========================================

def home(request):

    query = request.GET.get(
        'q'
    )

    region = request.GET.get(
        'region'
    )

    migratory_status = request.GET.get(
        'migratory_status'
    )

    category = request.GET.get(
        'category'
    )

    birds = Bird.objects.all()

    # ======================================
    # SEARCH
    # ======================================

    if query:

        birds = birds.filter(

            common_name__icontains=query

        ) | Bird.objects.filter(

            scientific_name__icontains=query

        ) | Bird.objects.filter(

            family__icontains=query
        )

    # ======================================
    # REGION FILTER
    # ======================================

    if region:

        birds = birds.filter(
            region__icontains=region
        )

    # ======================================
    # MIGRATORY FILTER
    # ======================================

    if migratory_status:

        birds = birds.filter(
            migratory_status__icontains=
            migratory_status
        )

    # ======================================
    # CATEGORY FILTER
    # ======================================

    if category:

        birds = birds.filter(
            category__icontains=category
        )

    # ======================================
    # PAGINATION
    # ======================================

    paginator = Paginator(

        birds,

        12
    )

    page_number = request.GET.get(
        'page'
    )

    page_obj = paginator.get_page(
        page_number
    )

    # ======================================
    # DYNAMIC REGION DISPLAY
    # ======================================

    if region:

        for bird in page_obj:

            bird.display_region = region

    else:

        for bird in page_obj:

            bird.display_region = bird.region

    # ======================================
    # UNIQUE CATEGORIES
    # ======================================

    categories = Bird.objects.values_list(

        'category',

        flat=True

    ).distinct()

    return render(

        request,

        'birds/home.html',

        {

            'page_obj': page_obj,

            'query': query,

            'region': region,

            'migratory_status':
                migratory_status,

            'categories': categories,

            'selected_category':
                category
        }
    )

# ==========================================
# BIRD DETAIL
# ==========================================

def bird_detail(request, id):

    bird = get_object_or_404(

        Bird,

        id=id
    )

    return render(

        request,

        'birds/bird_detail.html',

        {
            'bird': bird
        }
    )


# ==========================================
# AI IDENTIFICATION
# ==========================================

def identify_bird(request):

    prediction = None

    if request.method == 'POST':

        # TEMPORARY DEMO

        prediction = Bird.objects.first()

    return render(

        request,

        'birds/identify.html',

        {
            'prediction': prediction
        }
    )