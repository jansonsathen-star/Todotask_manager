from django.test import TestCase, Client
from todolist.models import Task
import json


class ApiTasksTest(TestCase):
    def setUp(self):
        Task.objects.create(task="alpha", completed=False)
        Task.objects.create(task="beta", completed=True)
        self.client = Client()

    def test_list_tasks(self):
        r = self.client.get("/todolist/api/tasks/")
        self.assertEqual(r.status_code, 200)
        data = json.loads(r.content)
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 2)

    def test_create_update_delete(self):
        # create
        r = self.client.post(
            "/todolist/api/tasks/create/",
            json.dumps({"task": "gamma"}),
            content_type="application/json",
        )
        self.assertEqual(r.status_code, 200)
        created = json.loads(r.content)
        self.assertIn("id", created)
        tid = created["id"]
        # update
        r2 = self.client.post(
            f"/todolist/api/tasks/{tid}/update/",
            json.dumps({"completed": True}),
            content_type="application/json",
        )
        self.assertEqual(r2.status_code, 200)
        upd = json.loads(r2.content)
        self.assertEqual(upd["completed"], True)
        # delete
        r3 = self.client.post(f"/todolist/api/tasks/{tid}/delete/")
        self.assertEqual(r3.status_code, 200)
        self.assertEqual(json.loads(r3.content)["status"], "ok")
