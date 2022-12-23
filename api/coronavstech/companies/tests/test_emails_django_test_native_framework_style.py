from unittest.mock import patch
import json
from django.core import mail
from django.test import TestCase
from django.test import Client

# look at the jupyter notebook file at:
# /home/pavlo/Documents/Projects/Pytest-Django/my_jupyter_notebooks/Django email service_Section 8_Steps 33 -35.ipynb


class EmailUnitTest(TestCase):
    """Test using 'django.test' native framework.
    It uses the same unittest style assertions like
    for example 'self.assertEqual()'. It is because 'django.test'
    is wrapping the unittest library."""

    def test_send_email_should_be_succeed(self) -> None:
        with self.settings(
            EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend"
        ):
            self.assertEqual(len(mail.outbox), 0)  # (3)
            # Send message: (2)
            mail.send_mail(
                subject="Test Subject here",
                message="Test Here is the message",
                from_email="testemail@gmail",
                recipient_list=["testmail2@gmail.com"],
                fail_silently=False,
            )
            # Test that one message has been sent.
            self.assertEqual(len(mail.outbox), 1)  # (3)

            # Verify that the subject of the first message is correct (4)
            self.assertEqual(mail.outbox[0].subject, "Test Subject here")

    def test_send_email_without_arguments_should_send_empty_email(self) -> None:
        client = Client()  # (5.1)
        with patch(
            "api.coronavstech.companies.views.send_mail"
        ) as mocked_send_mail_function:  # (6.1)
            response = client.post(path="/send-email")  # (5.2)
            response_content = json.loads(response.content)  # (5.3)
            self.assertEqual(response.status_code, 200)  # (5.4)
            self.assertEqual(response_content["status"], "success")  # (5.5)
            self.assertEqual(
                response_content["info"], "email sent successfully"
            )  # (5.6)
            mocked_send_mail_function.assert_called_with(  # (6.2)
                subject=None,  # (5)
                message=None,  # (5)
                from_email="python.testme@gmail.com",  # (5)
                recipient_list=["python.testme@gmail.com"],  # (5)
            )

    def test_send_email_with_get_verb_should_fail(self) -> None:  # (7)
        client = Client()
        response = client.get(path="/send-email")
        self.assertEqual(response.status_code, 405)
        self.assertEqual(
            json.loads(response.content), {"detail": 'Method "GET" not allowed.'}
        )
