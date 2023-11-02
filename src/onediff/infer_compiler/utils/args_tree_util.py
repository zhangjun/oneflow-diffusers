import torch
import oneflow as flow
from oneflow.framework.args_tree import ArgsTree

from typing import Any
from ..convert_torch_to_of._globals import _initial_package_names
from ..convert_torch_to_of.proxy import proxy_class

_ONEFLOW_HAS_REGISTER_RELAXED_TYPE_API = False
try:
    from oneflow.framework.args_tree import register_relaxed_type

    _ONEFLOW_HAS_REGISTER_RELAXED_TYPE_API = True
except:
    pass


def register_args_tree_relaxed_types():
    transformers_mocked = False
    for pkg in _initial_package_names:
        if "transformers" in pkg:
            transformers_mocked = True
    if _ONEFLOW_HAS_REGISTER_RELAXED_TYPE_API and transformers_mocked:
        import transformers

        register_relaxed_type(
            proxy_class(transformers.modeling_outputs.BaseModelOutputWithPooling)
        )
        register_relaxed_type(
            proxy_class(transformers.models.clip.modeling_clip.CLIPTextModelOutput)
        )
    else:
        pass


def input_output_processor(func):
    def process_input(*args, **kwargs):
        def input_fn(value):
            if isinstance(value, torch.Tensor):
                return flow.utils.tensor.from_torch(value)
            else:
                return value

        args_tree = ArgsTree((args, kwargs), False, tensor_type=torch.Tensor)
        out = args_tree.map_leaf(input_fn)
        mapped_args = out[0]
        mapped_kwargs = out[1]
        return mapped_args, mapped_kwargs

    def process_output(output):
        def output_fn(value):
            if isinstance(value, flow.Tensor):
                return flow.utils.tensor.to_torch(value)
            else:
                return value

        out_tree = ArgsTree((output, None), False)
        out = out_tree.map_leaf(output_fn)
        return out[0]

    def wrapper(cls, *args, **kwargs):
        mapped_args, mapped_kwargs = process_input(*args, **kwargs)
        output = func(cls, *mapped_args, **mapped_kwargs)
        return process_output(output)

    return wrapper
