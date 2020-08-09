from __future__ import print_function
import torch
x = torch.rand(5, 3)
print(x)
print(torch.cuda.is_available())
print(torch.cuda.device_count())
print(torch.cuda.get_device_name())
print(torch.cuda.current_device())

