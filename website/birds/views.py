from django.shortcuts import (
    render,
    get_object_or_404
)

from django.core.paginator import (
    Paginator
)

from .models import Bird

def _clean_param(request, name):

    """GET filter param as a plain string, never None or 'None'.

    The pagination links used to render ?q=None&region=None... when
    a filter was unset, because request.GET.get() returns None and
    the template printed it literally. The next request then
    filtered by the string "None", returning no birds at all
    ("Page 1 of 1") and showing "None" in the search box.
    """

    value = request.GET.get(name) or ''

    return '' if value == 'None' else value




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

    query = _clean_param(request, 'q')

    region = _clean_param(request, 'region')

    migratory_status = _clean_param(request, 'migratory_status')

    category = _clean_param(request, 'category')

    birds = Bird.objects.all().order_by(
        'common_name'
    )

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

        ) | Bird.objects.filter(

            local_name_kashmiri__icontains=query

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
    # UNIQUE CATEGORIES
    # ======================================

    categories = Bird.objects.values_list(
        'category',
        flat=True
    ).distinct()

    return render(

        request,

        'birds/gallery.html',

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

    query = _clean_param(request, 'q')

    region = _clean_param(request, 'region')

    migratory_status = _clean_param(request, 'migratory_status')

    category = _clean_param(request, 'category')

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

    # Photo identification is not built yet. This page is a
    # "Coming Soon" placeholder -- it must NOT pretend to
    # identify a bird. The previous version always returned
    # Bird.objects.first() regardless of the uploaded photo.

    return render(

        request,

        'birds/identify.html'

    )
