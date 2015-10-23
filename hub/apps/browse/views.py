from __future__ import unicode_literals

from logging import getLogger

from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView, TemplateView

from hub.permissions import get_aashe_member_flag
from ..content.models import CONTENT_TYPE_CHOICES, CONTENT_TYPES, ContentType
from ..metadata.models import SustainabilityTopic
from .filter import GenericFilterSet

logger = getLogger(__name__)


class HomeView(TemplateView):
    """
    The Home view.

    @permisson: HomeView is visible for everybody
    """
    template_name = 'browse/home.html'

    def get_context_data(self, **kwargs):
        ctx = super(HomeView, self).get_context_data(**kwargs)
        ctx.update({
            'topic_list': SustainabilityTopic.objects.all(),
            'content_type_list': dict(CONTENT_TYPE_CHOICES),
        })
        return ctx

# List of content type keys which don't require Login This only enables the
# 'browse' view of the content type. Each object must still be separately set to
# `member_only=False` to make it open.
PUBLIC_CONTENT_TYPES = (
    'academicprogram',
)

class BrowseView(ListView):
    """
    A very generic browse view to handle all sorts of views at once. Generally
    we have two views:

        - browse view, handling the result set for keyword and content type
          searches

        - topic view, if a topic is set, we render a custom template located
          in `browse/topic/<name>.html`.

    @permission: BrowseView generally requires Login, except:

        - The AcademicProgram content type view is open
        - The Toolkit tab is open, all others not visible
    """
    template_name = 'browse/browse.html'
    content_type_class = None
    sustainabilty_topic = None

    def dispatch(self, *args, **kwargs):
        """
        Persmission handling and load some generic objects into the class so we
        have it globally available.
        """
        # Load the specified SustainabilityTopic
        if self.kwargs.get('topic'):
            self.sustainabilty_topic = get_object_or_404(
                SustainabilityTopic, slug=self.kwargs['topic'])

        # Load the specified Content Type object. Make Content Type a nice
        # little object so it works similar to SustainabilityTopic
        if self.kwargs.get('ct'):
            if self.kwargs.get('ct') not in CONTENT_TYPES:
                raise Http404('This Content type does not exist')
            self.content_type_class = CONTENT_TYPES[self.kwargs['ct']]
            self.content_type_class.slug = self.kwargs.get('ct')

        # If no content type and no topic is set, we need at least a
        # search keyword:
        if (not self.sustainabilty_topic and not self.content_type_class
            and not self.request.GET.get('search')):
            return HttpResponseRedirect(reverse('home'))

        # Search results do generally need LoginRequired, however there
        # are certain ContentTypes defined in PUBLIC_CONTENT_TYPES which
        # don't even need login, they are browseable by everyone.
        if (self.content_type_class and
            self.content_type_class.slug in PUBLIC_CONTENT_TYPES):
            return super(BrowseView, self).dispatch(*args, **kwargs)

        # If it was not a PUBLIC content type, we do need login at least.
        if not self.request.user.is_authenticated():
            return render(self.request, 'registration/login_required.html',
                status=HttpResponseForbidden.status_code)

        return super(BrowseView, self).dispatch(*args, **kwargs)

    def get_template_names(self):
        """
        If a specific 'topic' is set in the url name, we'll render a template
        for this. In all other cases we have a generic browse result template.
        """
        if self.sustainabilty_topic:
            return ('browse/results/topic.html',)

        if self.content_type_class:
            return ('browse/results/content_type.html',)

        return ('browse/results/search.html',)

    def get_filterset(self):
        """
        Builds and returns a filter form object. Content Type classes might
        have their own, custom FilterSet defined in `model.get_custom_filterset`.
        """
        if self.content_type_class and hasattr(
        self.content_type_class, 'get_custom_filterset'):
            return self.content_type_class.get_custom_filterset()
        else:
            return GenericFilterSet

    def get_filterset_data(self):
        """
        Wether we're in a content type or topic view, we want to have the list
        of content types already filtered by these.
        """
        data = self.request.GET.copy()
        if self.sustainabilty_topic:
            data['topics'] = self.sustainabilty_topic.slug
        if self.content_type_class:
            data['content_type'] = self.content_type_class.slug
        logger.debug('filterset data: {}'.format(data))
        return data

    def get_title(self):
        """
        Returns the actual title of the current object, either topic,
        content type or search.
        """
        if self.sustainabilty_topic:
            return self.sustainabilty_topic.name
        if self.content_type_class:
            return self.content_type_class._meta.verbose_name
        if self.request.GET.get('search'):
            return 'Search for "{}"'.format(self.request.GET['search'])
        return 'Search Results'

    def get_queryset(self):
        return self.get_filterset()(
            self.get_filterset_data(),
            queryset=ContentType.objects.published())

    def get_context_data(self, **kwargs):
        ctx = super(BrowseView, self).get_context_data(**kwargs)
        ctx.update({
            'topic': self.sustainabilty_topic,
            'topic_list': SustainabilityTopic.objects.all(),
            'content_type': self.content_type_class,
            'content_type_list': dict(CONTENT_TYPE_CHOICES),
            'page_title': self.get_title(),
        })

        # Additional toolkit content for topic views
        if self.sustainabilty_topic:
            featured = (ContentType.objects.published()
                .filter(topics=self.sustainabilty_topic))

            new_resources = (ContentType.objects.published()
                .filter(topics=self.sustainabilty_topic)
                .order_by('-published')[:10])

            ctx.update({
                'featured_list': featured,
                'news_list': [],
                'new_resources_list': new_resources,
            })
        return ctx


class ResourceView(DetailView):
    """
    Actual Detail view of ContentType objects.

    @permisson:

        - Login Required
        - Each ContentType has a `member_only` attribut we will check too.
          Some objects might only need Login.
    """
    queryset = ContentType.objects.published()

    def dispatch(self, *args, **kwargs):
        """
        Check if this object is `Member Only`. If so, only AASHE members and
        Auth superusers are able to see it.

        Other than that, at least a login is required, which is provided by
        the `LoginRequiredMixin`.
        """
        obj = self.get_object()

        # Check if this object is open to anybody
        if obj.permission == ContentType.PERMISSION_CHOICES.open:
            return super(ResourceView, self).dispatch(*args, **kwargs)

        # The user needs to be at least logged in from here
        if not self.request.user.is_authenticated():
            return render(self.request, 'registration/login_required.html',
                status=HttpResponseForbidden.status_code)

        # If the object only needs login, we're fine and can display it:
        if obj.permission == ContentType.PERMISSION_CHOICES.login:
            return super(ResourceView, self).dispatch(*args, **kwargs)

        # User is either member, or superuser, so its' fine to view
        if get_aashe_member_flag(self.request.user):
            return super(ResourceView, self).dispatch(*args, **kwargs)

        # Otherwise, and finally, we deny.
        return render(self.request, 'registration/member_required.html',
            status=HttpResponseForbidden.status_code)


    def get_template_names(self):
        return (
            'browse/details/{}.html'.format(self.kwargs['ct']),
            'browse/details/base.html'
        )

    def get_object(self, queryset=None):
        if not self.kwargs['ct'] in CONTENT_TYPES:
            raise Http404('Resource model does not exist')

        if queryset is None:
            queryset = self.get_queryset()

        try:
            ct_model = CONTENT_TYPES[self.kwargs['ct']]
            obj = ct_model.objects.get(pk=self.kwargs['id'])
        except queryset.model.DoesNotExist:
            raise Http404('Resource not found')
        return obj
