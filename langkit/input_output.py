from logging import getLogger
from typing import Optional

from sentence_transformers import util
from whylogs.experimental.core.udf_schema import register_dataset_udf

from langkit.transformer import load_model

from . import lang_config, prompt_column, response_column

_prompt = prompt_column
_response = response_column

_transformer_model = None
_transformer_name = None

diagnostic_logger = getLogger(__name__)


def init(transformer_name: Optional[str] = None):
    global _transformer_model, _transformer_name
    if transformer_name is None:
        transformer_name = lang_config.transformer_name
    _transformer_model = load_model(transformer_name)
    _transformer_name = transformer_name


init()


@register_dataset_udf([_prompt, _response], f"{_response}.relevance_to_prompt")
def similarity_MiniLM_L6_v2(text):
    if _transformer_model is None:
        raise ValueError(
            "response.relevance_to_prompt must have a transformer model initialized before use."
        )

    series_result = []
    for x, y in zip(text["prompt"], text["response"]):
        try:
            embedding_1 = _transformer_model.encode(x, convert_to_tensor=True)
            embedding_2 = _transformer_model.encode(y, convert_to_tensor=True)
            similarity = util.pytorch_cos_sim(embedding_1, embedding_2)
            series_result.append(similarity.item())
        except Exception as e:
            diagnostic_logger.warning(
                f"pandas {text} caused similarity_MiniLM_L6_v2 to encounter error: {e}"
            )
            series_result.append(None)
    return series_result
