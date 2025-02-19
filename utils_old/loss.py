#添加focalloss类
import torch
import torch.nn as nn
import torch.nn.functional as F

class FocalLoss(nn.Module):
    def __init__(self, alpha=0.9, gamma=2, reduction='none'):
        super(FocalLoss, self).__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.reduction = reduction

    def forward(self, inputs, targets):
        BCE_loss = F.cross_entropy(inputs, targets, reduction='none')
        pt = torch.exp(-BCE_loss)
        F_loss = self.alpha * (1-pt)**self.gamma * BCE_loss

        if self.reduction == 'sum':
            return torch.sum(F_loss)
        elif self.reduction == 'mean':
            return torch.mean(F_loss)
        else:
            return F_loss

class ReweightedSoftmaxLoss(nn.Module):
    def __init__(self, weights=None, reduction='none'):
        super(ReweightedSoftmaxLoss, self).__init__()
        self.weights = weights
        self.reduction = reduction

    def forward(self, inputs, targets):
        if self.weights is not None:
            self.weights = torch.tensor(self.weights).to(inputs.device)
        CE_loss = F.cross_entropy(inputs, targets, weight=self.weights, reduction='none')
        
        if self.reduction == 'sum':
            return torch.sum(CE_loss)
        elif self.reduction == 'mean':
            return torch.mean(CE_loss)
        else:
            return CE_loss

