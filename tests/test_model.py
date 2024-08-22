import unittest


class TestModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        print('setUpClass')

    @classmethod
    def tearDownClass(cls) -> None:
        print('tearDownClass')

    def setUp(self) -> None:
        print('setUp')

    def tearDown(self) -> None:
        print('tearDown')

    @unittest.skipIf(False, '不运行')
    def test_model(self):
        import peewee
        from athenaeum.crawl.models.model import Model

        class Demo(peewee.Model):
            pass

        self.assertTrue(issubclass(Demo, Model))
