def my_side_effect(url):
            """ Side Effect function for test """
            test_url = "https://api.github.com/orgs/google"
            if url == test_url:
                return cls.org_payload
            return cls.repos_payload