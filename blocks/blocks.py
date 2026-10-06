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

    class Meta:
        icon = "pilcrow"
        group = "Standalone blocks"
        template = "blocks/text_block.html"
        admin_text = "This is from my TextBlock class"
        label = "Text Block"


class InfoBlock(blocks.StaticBlock):

    class Meta:
        icon = "arrow-right"
        group = "Standalone blocks"
        template = "blocks/info_block.html"
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
            group = "iterables"
            template = "blocks/faq_list_block.html"


class CarouselBlock(blocks.StreamBlock):
    image = ImageChooserBlock()
    quotation = blocks.StructBlock(
        [
            ("text", blocks.TextBlock()),
            ("author", blocks.CharBlock()),
        ]
    )

    class Meta:
        template = "blocks/carousel_block.html"
        group = "iterables"


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
        template = "blocks/call_to_action_block.html"


class ImageBlock(ImageChooserBlock):

    class Meta:
        template = "blocks/image_block.html"
        group = "Standalone blocks"
