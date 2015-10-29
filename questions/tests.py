#!/usr/bin/env
# -*- encoding: utf-8
# vim: ts=4 et sw=4 sts=4

"""
"""

from django.conf import settings

settings.configure(DEBUG=True)

from django.test import TestCase, LiveServerTestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

import logging

logger = logging.getLogger(__name__)

try:
    from selenium.webdriver.firefox.webdriver import WebDriver
except:
    print("No Selenium tests possible")

from random import Random

from questions.models import Question, Answer, PossibleAnswer, Profile
from social.facebook import Facebook

fixtures = ['category.yaml', 'initial_data.json', ]


class QuestionIntegrationTests(LiveServerTestCase):
    """
    Selenium Tests
    --------------

    Will fail for server installations.

    """

    @classmethod
    def setUpClass(cls):
        try:
            cls.selenium = WebDriver()
        except NameError as err:
            cls.selenium = False
            logger.debug(err)
        super(QuestionIntegrationTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        if cls.selenium:
            cls.selenium.quit()
        super(QuestionIntegrationTests, cls).tearDownClass()

    def test_admin_site(self):
        if self.selenium:
            # user opens web browser, navigates to admin page
            self.browser.get(self.live_server_url + '/admin/')
            body = self.browser.find_element_by_tag_name('body')
            self.assertIn('Django administration', body.text)
        else:
            self.assertTrue(True)


class AnonymousUrlTest(TestCase):
    """
    Test all URLs exposed by :mod:`question` to verify they all work,
    i.e. are not returning an server-error.
    """
    fixtures = [
        'groups.yaml',
        'user.yaml',
        'profile.yaml',
        'category.yaml',
        'question.yaml',
        'answer.yaml',
        'initial_data.json',
    ]

    def setUp(self):
        """
        setUp tests
        ===========
        """
        pass

    def tearDown(self):
        """
        tearDown tests
        ==============
        """
        pass

    def test_home(self):
        """
        test_home
        =========
        test the homepage for :mod:`question`
        """
        response = self.client.get(reverse('question:home'))
        self.assertEqual(response.status_code, 200)

    def test_profile_view(self):
        """
        test_profile_view
        =================
        test the views for :mod:`question.models.Profile` through
        :mod:`question.views.ProfileView`
        """
        response = self.client.get(reverse('question:profile-view', args=(5,)))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse('user:login') +
            '?next='+reverse('question:profile-view', args=(5,))
        )
        response = self.client.get(reverse('question:profile-view', args=(6,)))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse('user:login') +
            '?next='+reverse('question:profile-view', args=(6,))
        )

    def test_profile_edit(self):
        """
        test_profile_edit
        =================
        test the views for :mod:`question.models.Profile` through
        :mod:`question.views.ProfileEdit`
        """
        response = self.client.get(reverse('question:profile-edit'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse('user:login') +
            '?next='+reverse('question:profile-edit')
        )

    def test_profile_list(self):
        """
        test_profile_list
        =================

        Test for :mod:`question.views.ProfileList`
        """
        response = self.client.get(reverse('question:profile-list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse('user:login') +
            '?next='+reverse('question:profile-list')
        )

    def test_question_list(self):
        """
        test_question_list
        =========
        test for :mod:`question.views.QuestionList`
        """
        response = self.client.get(reverse('question:question-list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('user:login')+'?next=/q/q/')

    def test_question_detail(self):
        """
        test_question_detail
        =========
        test for :mod:`question.views.QuestionDetail`

        Page shall be visible to the public
        """
        response = self.client.get(
            reverse(
                'question:question-detail', args=(1,)
                )
            )
        self.assertEqual(response.status_code, 200)

    def test_answer_list(self):
        """
        test_answer_list
        =========
        test for :mod:`question.views.AnswerList`
        """
        response = self.client.get(reverse('question:answer-list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse('user:login') +
            '?next='+reverse('question:answer-list')
        )

    def test_answer_detail(self):
        """
        test_answer_detail
        =========
        test for :mod:`question.views.AnswerDetail`

        Page shall be visible to the public only if Answer.is_public is True
        """
        response = self.client.get(
            reverse(
                'question:answer-detail', args=(1,)
                )
            )
        """Answer '1' is set to `is_public=False`, should return 404."""
        self.assertEqual(response.status_code, 404)
        response = self.client.get(
            reverse(
                'question:answer-detail', args=(2,)
                )
            )
        """Answer '2' is set to `is_public=True`, should be visible to anon."""
        self.assertEqual(response.status_code, 200)


class UserUrlTest(TestCase):
    """
    Do the same as `question.tests.AnonymousUrlTest`, but logged in.
    """
    fixtures = [
        'groups.yaml',
        'user.yaml',
        'profile.yaml',
        'category.yaml',
        'question.yaml',
        'initial_data.json',
    ]

    def setUp(self):
        """
        setUp tests
        ===========
        """
        self.client.login(username="andreas", password="xt1tkpm.")

    def tearDown(self):
        """
        tearDown tests
        ==============
        """

    def test_home(self):
        """
        test_home
        =========
        test the homepage for :mod:`question`
        """
        response = self.client.get(reverse('question:home'))
        self.assertEqual(response.status_code, 200)

    def test_profile_view(self):
        """
        test_profile_edit
        =========
        test the views for :mod:`question.models.Profile` through
        :mod:`question.views.ProfileView`
        """
        response = self.client.get(reverse('question:profile-view', args=(5,)))
        self.assertEqual(response.status_code, 200)
        """Profile with ID 5 has a public profile. This should show."""
        response = self.client.get(reverse('question:profile-view', args=(6,)))
        self.assertEqual(response.status_code, 404)
        """Profile with ID 6 has no public profile. This should not show."""

    def test_profile_edit(self):
        """
        test_profile_edit
        =================
        test the views for :mod:`question.models.Profile` through
        :mod:`question.views.ProfileEdit`

        .. todo: raises a warning from `crispy_forms`
        """
        response = self.client.get(reverse('question:profile-edit'))
        # print(response)
        self.assertEqual(response.status_code, 200)
        """A logged in user should be able to edit his profile."""

    def test_profile_list(self):
        """
        test_profile_list
        =================

        Test for :mod:`question.views.ProfileList`
        """
        response = self.client.get(reverse('question:profile-list'))
        self.assertEqual(response.status_code, 200)

    def test_question_list(self):
        """
        test_question_list
        ==================
        test for :mod:`question.views.QuestionList`

        Expect to get `200`
        """
        response = self.client.get(reverse('question:question-list'))
        self.assertEqual(response.status_code, 200)

    def test_answer_list(self):
        """
        test_answer_list
        ==================
        test for :mod:`question.views.AnswerList`

        User needs to be logged in.

        Expect to get `200`
        """
        response = self.client.get(reverse('question:answer-list'))
        self.assertEqual(response.status_code, 200)

    def test_compare(self):
        """
        test_question_list
        ==================
        test for :mod:`question.views.QuestionList`
        """
        url = reverse('question:compare', kwargs={"pk": "1"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class QuestionTest(TestCase):
    fixtures = ['category.yaml', 'initial_data.json', ]

    def setUp(self):
        """
        setUp Tests
        ===========

        Create a bunch of users, along with random profiles and random answers
        """
        self.random = Random()
        for c in range(1, 150):
            u = User.objects.create(username="user%s" % c)
            g = "M"
            if self.random.randint(0, 100) > 50:
                g = "F"
            p = Profile(user=u, gender=g)
            p.save()
            u.save()

        q = Question.objects.create(question="Hallo?")
        p1 = PossibleAnswer.objects.create(
            answer="Was!",
            question=q
        )
        p2 = PossibleAnswer.objects.create(
            answer="Ich verstehe die Frage nicht.",
            question=q
        )

        for c in range(1, 100):
            """Intentionally create 50 answers less than users."""
            p = Profile.objects.get(user__username="user%s" % c)
            if self.random.randint(0, 100) > 50:
                a = Answer.objects.create(
                    profile=p,
                    question=q,
                    user_answer=p1
                )
            else:
                a = Answer.objects.create(
                    profile=p,
                    question=q,
                    user_answer=p2
                )

    def test_possible_answers(self):
        """
        Test whether question has possible answers
        """
        q = Question.objects.get(pk=1)
        c = q.possible_answer_count()
        self.assertGreater(c, 0)

    def test_has_answer(self):
        """
        Test whether question has any answers
        """
        q = Question.objects.get(pk=1)  # first question
        p = Profile.objects.get(user__username="user1")
        answer = q.has_answer(p)
        self.assertTrue(answer)
        p = Profile.objects.get(user__username="user148")
        answer = q.has_answer(p)
        self.assertFalse(answer)

    def test_answer_percent(self):
        """
        Test whether question.answer_percent returns an array
        """
        q = Question.objects.get(pk=1)  # first question
        r = q.answer_percent()
        self.assertEqual(type(r), type({}))


class ModelTest(TestCase):
    fixtures = [
        'groups.yaml',
        'user.yaml',
        'profile.yaml',
        'category.yaml',
        'question.yaml',
        'initial_data.json',
    ]

    def setUp(self):
        """
        """


class ProfileManagerTest(TestCase):
    fixtures = [
        'groups.yaml',
        'user.yaml',
        'profile.yaml',
        'category.yaml',
        'question.yaml',
        'initial_data.json',
    ]

    def setUp(self):
        """
        """

    def test_female(self):
        r = Profile.objects.female().count()
        self.assertEquals(r, 2)

    def test_male(self):
        r = Profile.objects.male().count()
        self.assertEquals(r, 4)

    def test_female_percent(self):
        r = Profile.objects.female_percent()
        self.assertEquals(r, 2.0/6.0)

    def test_male_percent(self):
        r = Profile.objects.male_percent()
        self.assertEquals(r, 4.0/6.0)


class FacebookTest(TestCase):
    fixtures = [
        'groups.yaml',
        'user.yaml',
        'profile.yaml',
        'category.yaml',
        'question.yaml',
        'initial_data.json',
    ]

    def setUp(self):
        pass

    def test_facebook_create_object(self):
        """
        test_facebook_create_object
        ===========================

        test the homepage for :mod:`question.facebook.Facebook.create_question`
        """
        u = User.objects.get(pk=1)
        q = Question.objects.get(pk=1)
        f = Facebook(u)
        result = f.create_question(q)
        self.assertEqual(result, [])


class ApiTest(TestCase):
    fixtures = [
        'groups.yaml',
        'user.yaml',
        'profile.yaml',
        'category.yaml',
        'question.yaml',
        'initial_data.json',
    ]

    def setUp(self):
        pass

    def test_question_api(self):
        """
        test_question_api
        =================

        test the homepage for :mod:`question`
        """
        response = self.client.get(reverse("question:api-question-list"))
        self.assertEqual(response.status_code, 200)
