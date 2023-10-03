import torch
import oneflow as flow
from onediff.infer_compiler import oneflow_compile
from onediff.infer_compiler.convert_torch_to_of import (
    add_to_proxy_of_mds,
    get_full_class_name,
)


class PyTorchModel(torch.nn.Module):
    """used torch2of conversion.

    For PyTorch models, input model must inherit torch.nn.Module to utilize trace and conversion of layers. 
    """

    def __init__(self):
        super().__init__()
        self.linear = torch.nn.Linear(4, 4)

    def forward(self, x):
        return self.linear(x)


class OneFlowModel(flow.nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = flow.nn.Linear(4, 4)

    def forward(self, x):
        return self.linear(x)


# Register PyTorch model to OneDiff
cls_key = get_full_class_name(PyTorchModel)
add_to_proxy_of_mds({cls_key: OneFlowModel})


# Compile PyTorch model to OneFlow
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
pytorch_model = PyTorchModel().to(device)
of_model = oneflow_compile(pytorch_model, use_graph=False)


# Verify conversion
x = torch.randn(4, 4).to(device)

y_pt = pytorch_model(x)
y_of = of_model(x)

print(
    f"""
      PyTorch output: {type(y_pt)}  
      {y_pt}
      OneFlow output: {type(y_of)}
      {y_of}
"""
)

"""Output:
      PyTorch output: <class 'torch.Tensor'>  
      tensor([[ 0.3281,  0.3748,  0.1928, -0.0843],
        [-0.3299,  1.1503,  0.0115, -0.2054],
        [ 0.1292, -0.1496,  1.1743, -0.4726],
        [ 0.2691,  0.2332,  0.1492,  0.5211]], device='cuda:0',
       grad_fn=<AddmmBackward0>)
      OneFlow output: <class 'torch.Tensor'>
      tensor([[ 0.3281,  0.3748,  0.1928, -0.0843],
        [-0.3299,  1.1503,  0.0115, -0.2054],
        [ 0.1292, -0.1496,  1.1743, -0.4726],
        [ 0.2691,  0.2332,  0.1492,  0.5211]], device='cuda:0')
"""