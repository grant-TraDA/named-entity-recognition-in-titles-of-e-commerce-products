import datasets
from .common import generate_examples, generate_info, get_splits, TOY_TAGS

NER_TAGS_DICT = TOY_TAGS


class CoNLLConfig(datasets.BuilderConfig):
    def __init__(self, **kwargs):
        super(CoNLLConfig, self).__init__(**kwargs)


class CoNLL(datasets.GeneratorBasedBuilder):
    def _info(self):
        return generate_info(NER_TAGS_DICT)

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        return get_splits("toys", "es")

    def _generate_examples(self, filepath=None):
        return generate_examples(filepath, NER_TAGS_DICT)
