from django.shortcuts import (
    render,
    get_object_or_404
)

from django.core.paginator import (
    Paginator
)

import base64
import io

from PIL import Image

from . import identifier
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

    # Real identification with the trained ConvNeXt-Tiny model
    # (689 species, test top-1 50.93% / top-5 74.04%). The model runs
    # locally in ONNX Runtime -- no external service. The model file
    # is downloaded at build time (see download_model); if it is
    # missing, the page says so instead of pretending to identify.

    context = {
        'model_available': identifier.model_available(),
        'download_status': identifier.download_status(),
        'results': None,
        'error': None,
        'photo_data_uri': None,
    }

    if request.method != 'POST':
        return render(request, 'birds/identify.html', context)

    upload = request.FILES.get('photo')
    if upload is None:
        context['error'] = 'Please choose a photo of a bird first.'
        return render(request, 'birds/identify.html', context)

    if upload.size > 10 * 1024 * 1024:
        context['error'] = 'That photo is over 10 MB. Please use a smaller one.'
        return render(request, 'birds/identify.html', context)

    try:
        image = Image.open(upload)
        image.verify()
    except Exception:
        context['error'] = 'That file does not look like a photo. Please upload a JPG or PNG image.'
        return render(request, 'birds/identify.html', context)

    # verify() closes the file object; reopen for real use.
    upload.seek(0)
    try:
        image = Image.open(upload).convert('RGB')
    except Exception:
        context['error'] = 'Could not read that photo. Please try another one.'
        return render(request, 'birds/identify.html', context)

    # Bound memory before anything else: a phone photo can be
    # 12-48 megapixels (100+ MB decoded), which could exhaust the
    # 512 MB worker. The model only needs 224 px and the preview
    # 512 px, so shrink anything larger up front.
    if max(image.size) > 1024:
        image.thumbnail((1024, 1024))

    if not identifier.model_available():
        status = identifier.download_status()
        if status['status'] == 'downloading':
            context['error'] = (
                'The identification model is still downloading to the '
                'server (first time only, 57 MB). Please try again in '
                'a minute.'
            )
        else:
            context['error'] = (
                'The identification model is not available on the server '
                'right now. Please try again later.'
            )
        return render(request, 'birds/identify.html', context)

    # Small preview of the uploaded photo, embedded in the page
    # (no file is saved on the server).
    preview = image.copy()
    preview.thumbnail((512, 512))
    buf = io.BytesIO()
    preview.save(buf, format='JPEG', quality=80)
    context['photo_data_uri'] = (
        'data:image/jpeg;base64,'
        + base64.b64encode(buf.getvalue()).decode()
    )

    try:
        predictions = identifier.predict(image, top_k=5)
    except Exception as exc:  # noqa: BLE001 - show a friendly error
        print(f"identify: inference failed: {exc!r}")
        context['error'] = (
            'Something went wrong while identifying the photo. '
            'Please try again with a different photo.'
        )
        return render(request, 'birds/identify.html', context)

    results = []
    for scientific_underscored, confidence in predictions:
        # Model classes are "Passer_domesticus"; the database stores
        # "Passer domesticus".
        scientific = scientific_underscored.replace('_', ' ')
        bird = Bird.objects.filter(
            scientific_name=scientific
        ).first() or Bird.objects.filter(
            scientific_name=scientific_underscored
        ).first()
        results.append({
            'scientific_name': scientific,
            'confidence': confidence,
            'confidence_pct': round(confidence * 100, 1),
            'bird': bird,
        })
    context['results'] = results

    return render(request, 'birds/identify.html', context)
