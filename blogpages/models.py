from django.db import models
from django.core.exceptions import ValidationError

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


class BlogIndex(Page):
    template = "blogpages/blog_index_page.html"
    max_count = 1  # Limit to one instance of this page type.
    parent_page_types = ["home.HomePage"]
    subpage_types = ["blogpages.BlogDetail"]

    subtitle = models.CharField(max_length=100, blank=True)
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        FieldPanel("body"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context["blogpages"] = BlogDetail.objects.live().public()
        return context



class BlogDetail(Page):
    subtitle = models.CharField(max_length=100, blank=True)
    body = RichTextField(blank=True)
    parent_page_types = ["blogpages.BlogIndex"]
    subpage_types = []

    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        FieldPanel("body"),
        FieldPanel("image"),
    ]

    def clean(self):
        super().clean()

        body_text = str(self.body).strip()
        validation_rules = (
            (
                "subtitle",
                bool(self.title and self.subtitle and self.title == self.subtitle),
                "The subtitle cannot be the same as the title.",
            ),
            (
                "body",
                bool(self.subtitle and body_text and body_text == self.subtitle),
                "The body cannot be the same as the subtitle.",
            ),
        )
        errors = {
            field: ValidationError(message)
            for field, invalid, message in validation_rules
            if invalid
        }

        if errors:
            raise ValidationError(errors)
