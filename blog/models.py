from django.db import models
from django import forms
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render


from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.search.models import Query


class BlogListingPage(RoutablePageMixin, Page):
    """Listing page lists all the Blog Detail Pages."""

    template = "blog/blog_listing_page.html"

    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context."""
        context = super().get_context(request, *args, **kwargs)
        search_query = request.GET.get('query', None)

        if search_query:
            all_posts = BlogDetailPage.objects.live().search(search_query)
            query = Query.get(search_query)

            query.add_hit()
        else:
            all_posts = BlogDetailPage.objects.live().public().order_by('-first_published_at')

        paginator = Paginator(all_posts, 2)
        page = request.GET.get("page")
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context["posts"] = posts
        context['search_query'] = search_query

        return context

    @route(r"^category/(?P<cat_slug>[-\w]*)/$", name="category_view")
    def category_view(self, request, cat_slug):
        """Find blog posts based on a category."""
        context = self.get_context(request)

        try:
            category = BlogCategory.objects.get(slug=cat_slug)
        except Exception:
            category = None

        if category is None:
            pass

        all_posts = BlogDetailPage.objects.live().public().filter(categories__in=[category])
        paginator = Paginator(all_posts, 1)
        page = request.GET.get("page")
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        context["posts"] = posts
        context['search_query'] = None

        return render(request, "blog/blog_category_page.html", context)


class BlogDetailPage(Page):
    """Blog detail page."""

    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text='Overwrites the default title',
    )
    blog_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=False,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )

    content = RichTextField(blank=True)
    categories = ParentalManyToManyField('blog.BlogCategory', blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
        ImageChooserPanel("blog_image"),
        StreamFieldPanel("content"),
        MultiFieldPanel(
            [
                FieldPanel("categories", widget=forms.CheckboxSelectMultiple)
            ],
            heading="Categories"
        ),
    ]


@register_snippet
class BlogCategory(models.Model):
    """Blog catgory for a snippet."""

    name = models.CharField(max_length=255)
    slug = models.SlugField(
        verbose_name="slug",
        allow_unicode=True,
        max_length=255,
        help_text='A slug to identify posts by this category',
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]

    class Meta:
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"
        ordering = ["name"]

    @property
    def get_url_path(self):
        return f'/blog/category/{self.name}/'.lower()

    def __str__(self):
        return self.name
