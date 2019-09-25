import torch
from torch import nn
import torch.optim as optim
from nets import vgg_module, mobilenetv2_module
from penguin import getsingleimg
from nets.multibox_loss import MultiBoxLoss

x, _ = getsingleimg()
vgg_test = vgg_module('train')
mobilenetv2_test = mobilenetv2_module('train')

vgg_test.eval()
vgg_test = vgg_test.cuda()
mobilenetv2_test.train()
mobilenetv2_test = mobilenetv2_test.cuda()
torch.backends.cudnn.benchmark = True

mbv2_pred = mobilenetv2_test(x)
# vgg_s = vgg_test(x)

# l2_loss = nn.MSELoss()
# loss_hint = l2_loss(mbv2_pred[-1], vgg_s)

criterion = MultiBoxLoss(21, 0.5, True, 0, True, 3, 0.5, False)
loss_ssd = criterion.forward(mbv2_pred[:3], mbv2_pred[:2], torch.Tensor([[[40.,25.,245.,265.,3.]]]))

gamma = 0.5
total_loss = loss_ssd #+ gamma * loss_hint
# first_block = []
# for name, i in mobilenetv2_test.named_parameters():
#     name = name.split('.')
#     if 'features' in name[0] and int(name[1]) <= 7 :
#         first_block.append(i)

optimizer = optim.SGD(mobilenetv2_test.parameters(), lr=0.01, momentum=0.9,
                        weight_decay=5e-4)
total_loss.backward()
optimizer.step()