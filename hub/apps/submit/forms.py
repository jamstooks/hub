from django import forms

from ..browse.forms import LeanSelectMultiple, LeanSelect
from ..content.models import Author, File, Image, Website


class SubmitResourceForm(forms.ModelForm):
    """
    A very generic ModelForm that is later executed by a modelform_factory.
    We'll just add some very generic validation here.
    """

    class Meta:
        widgets = {
            'topics': forms.widgets.SelectMultiple,
            'disciplines': forms.widgets.SelectMultiple,
            'organizations': LeanSelectMultiple,
        }

        exclude = (
            'id',
            'content_type',
            'status',
            'permission',
            'submitted_by',
            'published',
            'notes'
        )

    def clean_topics(self):
        topics = self.cleaned_data.get('topics')
        if topics and len(topics) > 3:
            raise forms.ValidationError('Please choose no more than 3 topics.')
        return topics

    def clean_disciplines(self):
        disciplines = self.cleaned_data.get('disciplines')
        if disciplines and len(disciplines) > 3:
            raise forms.ValidationError('Please choose no more than 3 disciplines.')
        return disciplines

    def clean_institutions(self):
        institutions = self.cleaned_data.get('institutions')
        if institutions and len(institutions) > 3:
            raise forms.ValidationError('Please choose no more than 3 institutions.')
        return institutions
        
    def save(self, request):
        self.instance.submitted_by = request.user
        return super(SubmitResourceForm, self).save()


class AffirmationMixin(object):

    def clean_affirmation(self):
        if not self.cleaned_data.get('affirmation'):
            raise forms.ValidationError('You need to acknowledge the affirmation')
        return self.cleaned_data.get('affirmation')


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        exclude = ('id', 'ct')
        widgets = {
            'organization': LeanSelect,
        }

    def save(self, instance):
        self.instance.ct = instance
        return super(AuthorForm, self).save()


class FileForm(AffirmationMixin, forms.ModelForm):
    class Meta:
        model = File
        exclude = ('id', 'ct')

    def save(self, instance):
        self.instance.ct = instance
        return super(FileForm, self).save()


class ImageForm(AffirmationMixin, forms.ModelForm):
    class Meta:
        model = Image
        exclude = ('id', 'ct')

    def save(self, instance):
        self.instance.ct = instance
        return super(ImageForm, self).save()


class WebsiteForm(forms.ModelForm):
    class Meta:
        model = Website
        exclude = ('id', 'ct')

    def save(self, instance):
        self.instance.ct = instance
        return super(WebsiteForm, self).save()
