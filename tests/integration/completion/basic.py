from pytest import fixture, mark

from sls.completion.complete import Completion
from sls.document import Document, Position
from sls.services.hub import ServiceHub


def document(text):
    doc = Document('.fake.uri.', text)
    return doc


class CompletionTest():
    def __init__(self):
        self.c = Completion.full(ServiceHub())

    def set(self, text):
        self.doc = document(text)
        return self

    def get_completion_for(self, pos):
        return self.c.complete(ws=None, doc=self.doc, pos=pos)

    def test(self, pos):
        result = self.get_completion_for(Position(*pos))
        # filter only for label for now
        return [k['label'] for k in result['items']]


@fixture
def completion(hub):
    return CompletionTest()


@mark.parametrize('text,pos,expected', [
    ('ht b', (0, 1), [
        'http',
    ]),
    ('http b', (0, 5), [
        'fetch', 'help', 'server'
    ]),
])
def test_complete_service(text, pos, expected, completion):
    assert completion.set(text=text).test(pos) == expected


@mark.parametrize('text,pos,expected', [
    ('slack send ', (0, 11), [
        'attachments', 'channel', 'text', 'token'
    ]),
    ('http fetch ', (0, 11), [
        'body', 'headers', 'method', 'query', 'url'
    ]),
    ('microservice/uuid ', (0, 18), [
        'entrypoint'
    ]),
])
def test_complete_service_arguments(text, pos, expected, completion):
    assert completion.set(text=text).test(pos) == expected
