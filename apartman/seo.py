"""
apartman/seo.py - SEO views (sitemap, robots.txt)
"""
from django.http import HttpResponse
from django.views.generic import TemplateView
from apartman.models import Apartman
from izleti.models import Lokacija
from datetime import date


def robots_txt(request):
    """robots.txt za tražilice"""
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Disallow: /dashboard/",
        "Disallow: /moj-racun/",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def sitemap_xml(request):
    """Sitemap za Google"""
    apartman = Apartman.objects.filter(aktivan=True).first()
    lokacije = Lokacija.objects.filter(aktivno=True)
    base = request.build_absolute_uri('/').rstrip('/')

    urls = [
        {'loc': base + '/', 'priority': '1.0', 'changefreq': 'weekly'},
        {'loc': base + '/apartman/', 'priority': '0.9', 'changefreq': 'monthly'},
        {'loc': base + '/izleti/', 'priority': '0.8', 'changefreq': 'monthly'},
        {'loc': base + '/okolica/', 'priority': '0.7', 'changefreq': 'monthly'},
        {'loc': base + '/rezervacije/', 'priority': '0.9', 'changefreq': 'weekly'},
    ]

    for lok in lokacije:
        urls.append({
            'loc': f"{base}/izleti/{lok.pk}/",
            'priority': '0.6',
            'changefreq': 'monthly',
        })

    xml_lines = ['<?xml version="1.0" encoding="UTF-8"?>',
                 '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']

    for u in urls:
        xml_lines += [
            '  <url>',
            f'    <loc>{u["loc"]}</loc>',
            f'    <changefreq>{u["changefreq"]}</changefreq>',
            f'    <priority>{u["priority"]}</priority>',
            f'    <lastmod>{date.today()}</lastmod>',
            '  </url>',
        ]

    xml_lines.append('</urlset>')
    return HttpResponse('\n'.join(xml_lines), content_type='application/xml')
