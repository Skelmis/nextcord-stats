from django.conf import settings
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import URLPattern, URLResolver, reverse

from base.forms import SitemapFilterForm

urlconf = __import__(settings.ROOT_URLCONF, {}, {}, [""])


def list_urls(lis, acc=None):
    if acc is None:
        acc = []
    if not lis:
        return
    l = lis[0]
    if isinstance(l, URLPattern):
        yield acc + [str(l.pattern)]
    elif isinstance(l, URLResolver):
        yield from list_urls(l.url_patterns, acc + [str(l.pattern)])
    yield from list_urls(lis[1:], acc)


def sitemap_view(request):
    if request.method == "POST":
        # Redirect with relevant args
        url = reverse("base-sitemap")
        form = SitemapFilterForm(request.POST)
        if not form.is_valid():
            return redirect(url)

        return redirect(url + f"?filter={form.cleaned_data['filter_query']}")

    request_filter = request.GET.get("filter", None)

    raw_urls = list(list_urls(urlconf.urlpatterns))
    urls = []
    for uri in raw_urls:
        joined_url = "".join(uri)

        # Exclude admin routes
        if joined_url.startswith("admin/") and joined_url != "admin/":
            continue

        # Apply filters
        if request_filter and request_filter not in joined_url:
            continue

        urls.append(joined_url.rstrip("/"))

    urls = sorted(urls)

    plot_headers = ["Url", "Jump link"]

    form = SitemapFilterForm()

    return render(
        request,
        "base/sitemap.html",
        context={
            "all_urls": urls,
            "headers": plot_headers,
            "urls": urls,
            "form": form,
        },
    )
