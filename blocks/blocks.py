from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class TextBlock(blocks.TextBlock):

    def __init__(self, **kwargs):
        super().__init__(
            **kwargs,
            help_text="This is from my TextBlock class (help text is here)",
            max_length=500,
            min_length=10,
            required=False,
        )


class InfoBlock(blocks.StaticBlock):

    class Meta:
        icon = "..."
        template = "..."
        admin_text = "This is from my InfoBlock class"
        label = "General Information"


class FAQBlock(blocks.StructBlock):
    question = blocks.CharBlock()
    answer = blocks.RichTextBlock(
        features=["bold", "italic"],
        required=True,
    )


class FAQListBlock(blocks.ListBlock):
    def __init__(self, **kwargs):
        super().__init__(FAQBlock(), **kwargs)

        class Meta:
            min_num = 1
            max_num = 5
            icon = "list-ul"
            label = "Frequently Asked Questions 2"
            icon = "..."
            template = "..."


class CarouselBlock(blocks.StreamBlock):
    image = ImageChooserBlock()
    quotation = blocks.StructBlock(
        [
            ("text", blocks.TextBlock()),
            ("author", blocks.CharBlock()),
        ]
    )


class CallToActionBlock(blocks.StructBlock):
    text = blocks.RichTextBlock(
        features=["bold", "italic"],
        required=True,
    )
    page = blocks.PageChooserBlock()
    button_text = blocks.CharBlock(
        max_length=50,
        required=False,
    )

    class Meta:
        label = "CTA #1"


class ImageBlock(ImageChooserBlock):

    class Meta:
        template = "..."


