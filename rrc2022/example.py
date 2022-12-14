"""Example policy for Real Robot Challenge 2022"""
import numpy as np
import torch

from rrc_2022_datasets import PolicyBase

from . import policies
import torch
import torch.nn as nn
import os
class TorchBasePolicy(PolicyBase):
    def __init__(
        self,
        torch_model,
        action_space,
        observation_space,
        episode_length,
    ):
        self.action_space = action_space
        self.device = "cpu"
        self.policy = torch_model
        self.policy.eval()

        # load torch script
        self.action_space = action_space
        self.action_max = self.action_space.high[0]

    @staticmethod
    def is_using_flattened_observations():
        return True

    def reset(self):
        pass  # nothing to do here

    def get_action(self, observation):
        observation = torch.tensor(observation, dtype=torch.float, device=self.device)
        action = self.policy(observation.unsqueeze(0))
        action = action.detach().numpy()[0]
        action *= self.action_max
        return action


class TorchPushPolicyExpert(TorchBasePolicy):
    """Example policy for the push task, using a torch model to provide actions.

    Expects flattened observations.
    """

    def __init__(self, action_space, observation_space, episode_length):
        self.policy = Policy_(observation_space.shape[0], action_space.shape[0])
        self.policy.load_state_dict(torch.load(os.path.dirname(os.path.abspath(__file__))+"/policies/trifinger-cube-push-real-expert-v0True-180.pt",map_location=torch.device('cpu'))["policy"])
        super().__init__(self.policy, action_space, observation_space, episode_length)

class TorchPushPolicyMixed(TorchBasePolicy):
    """Example policy for the push task, using a torch model to provide actions.

    Expects flattened observations.
    """

    def __init__(self, action_space, observation_space, episode_length):
        self.policy = Policy_(observation_space.shape[0], action_space.shape[0])
        self.policy.load_state_dict(torch.load(os.path.dirname(os.path.abspath(__file__))+"/policies/trifinger-cube-push-real-mixed-v0True-860.pt",map_location=torch.device('cpu'))["policy"])
        super().__init__(self.policy, action_space, observation_space, episode_length)


class TorchLiftPolicyExpert(TorchBasePolicy):
    """Example policy for the lift task, using a torch model to provide actions.

    Expects flattened observations.
    """

    def __init__(self, action_space, observation_space, episode_length):
        self.policy = Policy_(observation_space.shape[0], action_space.shape[0])
        self.policy.load_state_dict(torch.load(os.path.dirname(os.path.abspath(__file__))+"/policies/trifinger-cube-lift-real-expert-v0True-990.pt",map_location=torch.device('cpu'))["policy"])
        super().__init__(self.policy, action_space, observation_space, episode_length)

class TorchLiftPolicyMixed(TorchBasePolicy):
    """Example policy for the lift task, using a torch model to provide actions.

    Expects flattened observations.
    """

    def __init__(self, action_space, observation_space, episode_length):
        self.policy = Policy_(observation_space.shape[0], action_space.shape[0])
        self.policy.load_state_dict(torch.load(os.path.dirname(os.path.abspath(__file__))+"/policies/trifinger-cube-lift-real-mixed-v0True-410.pt",map_location=torch.device('cpu'))["policy"])
        super().__init__(self.policy, action_space, observation_space, episode_length)

class Policy_(nn.Module):
    def __init__(self, o_dim, a_dim):
        super(Policy_, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(o_dim, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, a_dim),
            nn.Tanh()
        )
    def forward(self,o_input):
        return self.net(o_input)