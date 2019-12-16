import json

from api.login import validate_credentials, valid_token, valid_token_optional
from api.tests.test_views import create_request_with_token_header, user_tokens
from dbas.tests.utils import construct_dummy_request, TestCaseWithConfig


class ValidateCredentialsTest(TestCaseWithConfig):
    def test_valid_credentials(self):
        request = construct_dummy_request()
        request.validated = {
            'nickname': 'Walter',
            'password': 'iamatestuser2016'
        }
        validate_credentials(request)
        self.assertEqual(0, len(request.errors))
        self.assertIn('nickname', request.validated)
        self.assertIn('token', request.validated)

    def test_invalid_credentials(self):
        request = construct_dummy_request()
        request.validated = {
            'nickname': 'Walter',
            'password': 'somerandomstuffwhichisdefinitelynotapassword'
        }
        validate_credentials(request)
        self.assertNotIn('user', request.validated)
        self.assertGreater(len(request.errors), 0)


class ValidTokenJWTTest(TestCaseWithConfig):
    header = 'Authorization'

    def test_invalid_token(self):
        request = construct_dummy_request()
        request.headers[self.header] = 'Bearer thisisnotarealtoken'
        valid_token(request)
        self.assertGreater(len(request.errors), 0)
        self.assertNotIn('user', request.validated)

    def test_valid_token(self):
        request = create_request_with_token_header()
        valid_token(request)
        self.assertEqual(len(request.errors), 0)
        self.assertIn('user', request.validated)


class ValidTokenTest(TestCaseWithConfig):
    header = 'X-Authentication'

    def test_valid_token(self):
        nickname = 'Walter'
        token = user_tokens[nickname]
        request = construct_dummy_request()
        request.headers[self.header] = json.dumps(
            {'nickname': nickname, 'token': token, 'additional key': 'will be ignored'})
        valid_token(request)
        self.assertEqual(request.errors, [])
        self.assertIn('user', request.validated)

    def test_invalid_nickname(self):
        nickname = 'Walter_not_in_db'
        token = 'mytoken'
        request = construct_dummy_request()
        request.headers[self.header] = json.dumps({'nickname': nickname, 'token': token})
        valid_token(request)
        self.assertGreater(len(request.errors), 0)
        self.assertNotIn('user', request.validated)

    def test_invalid_nickname_with_valid_signature(self):
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJuaWNrbmFtZSI6IlBhc2NhbDEyMyIsImlkIjoxLCJncm91cCI6InVzZXJzIiwiaWF0IjoxNTY4MTQxMzAwLCJtb2RlIjoiYWktY29uZnJvbnRhdGlvbmFsIn0.9HlU0FtSwLZbT0Wq73TpvrfF0kvcLkseZFx7UpWmhp-KKqcqc6zGGWQsW6kc7gZcf_M96R-i_u-CzvaK1TOxYw'
        request = construct_dummy_request()
        request.headers[self.header] = json.dumps({'token': token})
        valid_token(request)
        self.assertGreater(len(request.errors), 0)
        self.assertIn("nickname", str(request.errors[0]))
        self.assertNotIn('user', request.validated)

    def test_unknown_user_id_with_valid_signature(self):
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJuaWNrbmFtZSI6IlBhc2NhbCIsImlkIjoxMzM3LCJncm91cCI6InVzZXJzIiwiaWF0IjoxNTY4MTQxMzAwLCJtb2RlIjoiYWktY29uZnJvbnRhdGlvbmFsIn0.sj45qib5-SlK6EFS2_sE_jXhMKYO6o_INTeZIF0ivwfncUbhahfLp13sAjL3ByEzFwzj2GMcumyATnB6z9MLGQ'
        request = construct_dummy_request()
        request.headers[self.header] = json.dumps({'token': token})
        valid_token(request)
        self.assertGreater(len(request.errors), 0)
        self.assertIn("unknown", str(request.errors[0]))
        self.assertNotIn('user', request.validated)

    def test_anonymous_user_ignore_optional(self):
        nickname = 'anonymous'
        token = 'mytoken'
        request = construct_dummy_request()
        request.headers[self.header] = json.dumps({'nickname': nickname, 'token': token})
        valid_token_optional(request)
        self.assertListEqual(request.errors, [])
        self.assertIn('user', request.validated)
