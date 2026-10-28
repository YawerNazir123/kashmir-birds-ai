from django.shortcuts import (
    render,
    get_object_or_404
)

from django.core.paginator import (
    Paginator
)

import base64
import csv
import io

from pathlib import Path

from PIL import Image

from . import identifier
from .models import Bird

# Model class -> IOC common name, from the cleaned 689-species
# list (model-data/cleaned-species-list.csv). The model predicts
# scientific names, but the database stores some species under
# an older scientific name (e.g. Demoiselle Crane is
# "Anthropoides virgo" in the DB, "Grus virgo" in the model).
# Matching by common name as well means those birds are found
# in the field guide instead of wrongly reported as new.
_MODEL_COMMON_NAMES = None


def _model_common_names():
    global _MODEL_COMMON_NAMES
    if _MODEL_COMMON_NAMES is None:
        _MODEL_COMMON_NAMES = {}
        csv_path = (
            Path(__file__).resolve().parents[3]
            / 'model-data' / 'cleaned-species-list.csv'
        )
        try:
            with open(csv_path, encoding='utf-8') as handle:
                for row in csv.DictReader(handle):
                    scientific = (row.get('scientific_name') or '').strip()
                    common = (row.get('common_name') or '').strip()
                    if scientific and common:
                        _MODEL_COMMON_NAMES[scientific] = common
        except OSError:
            # No mapping file: fall back to scientific-name
            # matching only. Never break identification.
            pass
    return _MODEL_COMMON_NAMES


def _find_bird(scientific_name):
    """Find the Bird row for a model's scientific name.

    Tries the scientific name as stored, then the common name
    from the cleaned species list. Returns None when the
    species is not in the field guide at all.
    """
    bird = Bird.objects.filter(
        scientific_name=scientific_name
    ).first()
    if bird is not None:
        return bird
    common = _model_common_names().get(scientific_name)
    if common:
        bird = Bird.objects.filter(
            common_name=common
        ).first()
    return bird

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

    # The region field stores combined values such as
    # "Jammu, Kashmir Valley", so counting distinct raw values
    # would give 6. The site covers 3 named regions; count
    # those.
    named_regions = set()
    for value in Bird.objects.values_list('region', flat=True):
        for part in (value or '').split(','):
            part = part.strip()
            if part:
                named_regions.add(part)
    regions = len(named_regions)

    categories = Bird.objects.values_list(

        'category',

        flat=True

    ).distinct().count()

    # Rare & Iconic Birds: six species whose info.json status is
    # "Rare Visitor" in J&K, each with a photo in the database.
    # Verified 2026-10-26 from bird_database/*/info.json.
    featured_names = [
        'Black-necked Crane',
        'Himalayan Monal',
        'Amur Falcon',
        'Saker Falcon',
        'Greater Spotted Eagle',
        'Cinereous Vulture',
    ]
    featured_blurbs = {
        'Black-necked Crane':
            'A rare high-altitude crane — only a handful reach '
            'the wetlands of Ladakh each year.',
        'Himalayan Monal':
            'Kashmir’s most colourful pheasant — a glittering '
            'high-altitude bird of the Himalayan forests.',
        'Amur Falcon':
            'A small falcon on a long migration — a rare passage '
            'visitor through Kashmir.',
        'Saker Falcon':
            'A powerful falcon of open country, a rare winter '
            'visitor to the region.',
        'Greater Spotted Eagle':
            'A scarce winter visitor to Kashmir’s wetlands and '
            'lowlands.',
        'Cinereous Vulture':
            'One of the world’s largest vultures, a rare winter '
            'visitor to the Himalayas.',
    }
    featured_birds = []
    for name in featured_names:
        bird = Bird.objects.filter(
            common_name=name
        ).first()
        if bird is None or not bird.image:
            continue
        bird.featured_blurb = featured_blurbs.get(name, '')
        featured_birds.append(bird)

    return render(

        request,

        'birds/landing.html',

        {

            'total_birds': total_birds,

            'migratory_birds':
                migratory_birds,

            'regions': regions,

            'categories': categories,

            'featured_birds': featured_birds,
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

        ) | Bird.objects.filter(

            local_name_dogri__icontains=query

        ) | Bird.objects.filter(

            local_name_ladakhi__icontains=query

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
def contributors(request):

    return render(

        request,

        'birds/contributors.html'
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
        'top_result': None,
        'top_bird': None,
        'is_new_bird': False,
        'low_confidence': False,
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
        bird = _find_bird(scientific)
        results.append({
            'scientific_name': scientific,
            'confidence': confidence,
            'confidence_pct': round(confidence * 100, 1),
            'bird': bird,
        })
    context['results'] = results

    # The top prediction drives the detail card / new-bird banner.
    top = results[0]
    context['top_result'] = top
    context['top_bird'] = top['bird']
    context['is_new_bird'] = top['bird'] is None
    # A top guess under 30% is not a confident identification;
    # the template says so plainly instead of presenting it
    # as certain.
    context['low_confidence'] = top['confidence'] < 0.30

    return render(request, 'birds/identify.html', context)
