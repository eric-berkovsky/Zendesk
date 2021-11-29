import json
import unittest, requests
from unittest.mock import patch, Mock

from zendesk.config import credentials, subdomain
from zendesk.functions import *

zendesk_api = 'zendesk.com/api/v2'


class ZendeskTestCases(unittest.TestCase):
    @patch('requests.get')  # Mock requests' module 'get' method.
    def test_request_response(self, mock_get):
        """
        Confirm that the mock response works
        """
        mock_get.return_value.status_code = 200
        response = requests.get(f'https://{subdomain}.{zendesk_api}/tickets.json', auth=credentials)
        self.assertEqual(200, response.status_code)

    @patch('requests.get')
    def test_get_api_response(self, mock_get):
        """
        Confirm that the correct exception is thrown if the HTTP request is unsuccessful
        """
        mock_get.return_value.status_code = 500
        url = f'https://{subdomain}.{zendesk_api}/tickets.json'
        self.assertRaises(RuntimeError, get_api_response, url)

        mock_get.return_value.status_code = 400
        self.assertRaises(PermissionError, get_api_response, url)

    def test_get_admin_name(self):
        """
        Confirm that the correct name is returned for the user of the web app
        """
        mock_get_patcher = patch('requests.get')
        users = {"users": [{"id": 223443, "name": "John Smith"}]}
        mock_get = mock_get_patcher.start()
        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = users
        response = get_admin_name()
        mock_get_patcher.stop()

        self.assertEqual("John Smith", response)

    def test_get_total_ticket_count(self):
        """
        Confirm that the correct name and ticket count are returned for a user
        """
        mock_get_patcher = patch('requests.get')
        tickets = {"count": {"refreshed_at": "2020-04-06T02:18:17Z", "value": 102}}
        mock_get = mock_get_patcher.start()
        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = tickets
        response = get_total_ticket_count()
        mock_get_patcher.stop()

        self.assertEqual(102, response)

    def test_get_tickets(self):
        """
        Confirm that the right JSON data is returned for 25 tickets
        """
        mock_get_patcher = patch('requests.get')
        with open('ZendeskCodingChallenge/test_ticket_result.json') as json_file:
            tickets = json.load(json_file)
        mock_get = mock_get_patcher.start()
        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = tickets
        response = get_tickets(False, False)
        mock_get_patcher.stop()

        self.assertDictEqual(tickets, response)

    def test_has_prev_tickets(self):
        """
        Confirm that has_prev_tickets() correctly identifies if there are any tickets in the list
        """
        mock_get_patcher = patch('requests.get')
        prev_json = {"tickets": [], "meta": {"has_more": True, "after_cursor": "xxx", "before_cursor": "yyy"},
                     "links": {"next": "https://example.zendesk.com/api/v2/tickets.json?page[size]=100&page[after]=xxx",
                               "prev": "https://example.zendesk.com/api/v2/tickets.json?page[size]=100&page[before]=yyy"
                               }
                     }
        mock_get = mock_get_patcher.start()
        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = prev_json
        url = f'https://{subdomain}.{zendesk_api}/tickets.json'
        response = has_prev_tickets(url)
        self.assertFalse(response)

        prev_json = {"tickets": ['ticket'], "meta": {"has_more": True, "after_cursor": "xxx", "before_cursor": "yyy"},
                     "links": {"next": "https://example.zendesk.com/api/v2/tickets.json?page[size]=100&page[after]=xxx",
                               "prev": "https://example.zendesk.com/api/v2/tickets.json?page[size]=100&page[before]=yyy"
                               }
                     }
        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = prev_json
        response = has_prev_tickets(url)
        mock_get_patcher.stop()
        self.assertTrue(response)

    def test_get_ticket(self):
        mock_get_patcher = patch('requests.get')
        ticket = {
            "ticket": {"assignee_id": 235323, "collaborator_ids": [35334, 234], "created_at": "2009-07-20T22:55:29Z"}
        }
        parsed_ticket = ticket['ticket']
        mock_get = mock_get_patcher.start()
        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = ticket
        response = get_ticket(1)
        mock_get_patcher.stop()

        self.assertDictEqual(parsed_ticket, response)

    def test_parse_date(self):
        """
        Test that parse_date() correctly formats a date
        """
        zendesk_formatted_date = '2009-07-20T22:55:29Z'
        human_readable = 'Monday, July 20, 2009 at 10:55 PM'
        self.assertEqual(human_readable, parse_date(zendesk_formatted_date))

        zendesk_formatted_date = '2011-05-05T10:38:52Z'
        human_readable = 'Thursday, May 5, 2011 at 10:38 AM'
        self.assertEqual(human_readable, parse_date(zendesk_formatted_date))

    def test_get_user_name(self):
        mock_get_patcher = patch('requests.get')
        user = {"user": {"id": 35436, "name": "Johnny Agent"}}
        mock_get = mock_get_patcher.start()
        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = user
        response = get_user_name(35436)
        mock_get_patcher.stop()

        self.assertEqual("Johnny Agent", response)


if __name__ == '__main__':
    unittest.main()
