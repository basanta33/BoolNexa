import reflex as rx
from reflex.plugins import RadixThemesPlugin
from reflex_base.plugins.sitemap import SitemapPlugin

config = rx.Config(
    app_name="digital_logic_lab",
    deploy_url="https://boolnexa-teal-ring.reflex.run",
    plugins=[
        RadixThemesPlugin(),
        SitemapPlugin(),
    ],
)