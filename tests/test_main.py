import unittest
from main import lint

class DockerfileLintTests(unittest.TestCase):
    def test_reports_latest_and_missing_user(self):
        result=lint("FROM python:latest\nCMD [\"python\", \"app.py\"]\n")
        messages=" ".join(x["message"] for x in result)
        self.assertIn("not pinned",messages)
        self.assertIn("No USER",messages)

    def test_detects_secret_assignment(self):
        result=lint("FROM python:3.12\nARG API_KEY=abc123\nUSER app\n")
        self.assertTrue(any(x["level"]=="ERROR" for x in result))

if __name__=="__main__": unittest.main()
