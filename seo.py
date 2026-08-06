"""SEO metadata and structured data for BoolNexa."""

from __future__ import annotations

import json

import reflex as rx


SITE_URL = "https://boolnexa-teal-ring.reflex.run"
PAGE_URL = f"{SITE_URL}/"

PAGE_TITLE = "BoolNexa - Free Online Digital Logic Simulator"
PAGE_DESCRIPTION = (
    "Design, connect, and simulate digital logic circuits online with BoolNexa. "
    "Explore logic gates, flip-flops, adders, subtractors, multiplexers, "
    "demultiplexers, encoders, and decoders for free."
)

SOCIAL_DESCRIPTION = (
    "Build and simulate digital logic circuits online with logic gates, "
    "flip-flops, adders, multiplexers, encoders, decoders, and more."
)

SOFTWARE_APPLICATION_SCHEMA = {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "BoolNexa",
    "url": PAGE_URL,
    "applicationCategory": "EducationalApplication",
    "applicationSubCategory": "Digital Logic Simulator",
    "operatingSystem": "Any",
    "browserRequirements": "Requires a modern web browser with JavaScript enabled.",
    "description": PAGE_DESCRIPTION,
    "softwareVersion": "1.1.0",
    "isAccessibleForFree": True,
    "offers": {
        "@type": "Offer",
        "price": "0",
        "priceCurrency": "USD",
    },
    "featureList": [
        "Interactive digital logic circuit design",
        "Real-time circuit simulation",
        "Logic gates",
        "Flip-flops",
        "Adders and subtractors",
        "Multiplexers and demultiplexers",
        "Encoders and decoders",
        "Clocked sequential circuits",
        "Project import and export",
    ],
}


def seo_head_components() -> list[rx.Component]:
    """Return global head elements that are not represented by page meta tags."""
    return [
        rx.el.link(rel="canonical", href=PAGE_URL),
        rx.el.link(rel="icon", href="/favicon.ico"),
        rx.el.meta(name="theme-color", content="#0f172a"),
        rx.el.meta(name="author", content="BoolNexa"),
        rx.el.meta(name="application-name", content="BoolNexa"),
        rx.el.meta(name="apple-mobile-web-app-title", content="BoolNexa"),
        rx.el.script(
            json.dumps(SOFTWARE_APPLICATION_SCHEMA, separators=(",", ":")),
            type="application/ld+json",
        ),
    ]


def seo_meta() -> list[dict[str, str]]:
    """Return page-level SEO, Open Graph, and Twitter/X metadata."""
    return [
        {"name": "robots", "content": "index, follow, max-image-preview:large"},
        {"name": "googlebot", "content": "index, follow, max-image-preview:large"},
        {"name": "description", "content": PAGE_DESCRIPTION},
        {"property": "og:site_name", "content": "BoolNexa"},
        {"property": "og:title", "content": PAGE_TITLE},
        {"property": "og:description", "content": SOCIAL_DESCRIPTION},
        {"property": "og:type", "content": "website"},
        {"property": "og:url", "content": PAGE_URL},
        {"property": "og:locale", "content": "en_US"},
        {"name": "twitter:card", "content": "summary"},
        {"name": "twitter:title", "content": PAGE_TITLE},
        {"name": "twitter:description", "content": SOCIAL_DESCRIPTION},
    ]
