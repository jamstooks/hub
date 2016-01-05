from django.contrib.auth.models import User
from django.core import mail
from django_webtest import WebTest

from ..apps.content.types.videos import Video
from ..apps.metadata.models import (Organization,
                                    SustainabilityTopic,
                                    InstitutionalOffice)


class AdminTestCase(WebTest):

    def setUp(self):
        super(AdminTestCase, self).setUp()
        self.superuser = User.objects.create_superuser(
            first_name='Super',
            last_name='User',
            email='superuser@example.com',
            username='superuser',
            password='password'
        )

        self.resource = Video(content_type='video',
                              status='new',
                              permission='open',
                              title='Test Video Resource',
                              slug='test-video-resource',
                              link='http://example.com/video',
                              submitted_by=self.superuser)
        self.resource.save()
        self.resource.organizations.add(
            Organization.objects.create(account_num=1,
                                        org_name='Hipster University',
                                        exclude_from_website=0))
        self.resource.topics.add(
            SustainabilityTopic.objects.create(name='Science'))
        self.resource.institutions.add(
            InstitutionalOffice.objects.create(name='Lirum'))
        self.resource.save()

    def _post_resource(self, status):
        response = self.app.get(self.resource.get_admin_url(),
                                user=self.superuser.username)
        response.form['status'] = status
        return response.form.submit()

    def test_mail_is_sent_upon_resource_approval(self):
        self._post_resource('published')
        self.assertEqual(1, len(mail.outbox))
        self.assertIn('approved', mail.outbox[0].subject.lower())

    def test_mail_is_sent_upon_resource_rejection(self):
        self._post_resource('declined')
        self.assertEqual(1, len(mail.outbox))
        self.assertIn('declined', mail.outbox[0].subject.lower())