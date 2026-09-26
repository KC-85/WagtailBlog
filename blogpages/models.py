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

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase



class BlogPageTags(TaggedItemBase):
    content_object = ParentalKey(
        "blogpages.BlogDetail",
        on_delete=models.CASCADE,
        related_name="tagged_items",
    )

class BlogDetail(Page):
    subtitle = models.CharField(max_length=100, blank=True)
    body = RichTextField(
        blank=True,
        features=["blockquote", "h3", "image", "ul", "strikethrough"]
    )
    tags = ClusterTaggableManager(through=BlogPageTags, blank=True)


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
        FieldPanel("tags"),
    ]

    def clean(self):
        super().clean()

        errors = {}

        if 'blog' in self.title.lower():
            errors['title'] = "The title cannot contain the word 'blog'."

        if 'blog' in self.subtitle.lower():
            errors['subtitle'] = "The subtitle cannot contain the word 'blog'."

        if 'blog' in self.slug.lower():
            errors['slug'] = "The slug cannot contain the word 'blog'."

        if errors:
            raise ValidationError(errors)
