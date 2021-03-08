import sys
import time
from collections import deque

from skimage.color import rgb2gray
from skimage.transform import rescale

import torch
import gym
import numpy as np
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from matplotlib import pyplot as plt
from simWrap import SimWrap


class Agent(nn.Module):
    def __init__(self, num_of_frames=3):
        super(Agent, self).__init__()

        # self.input = nn.Linear(96*96*3, 500)
        # self.hidden1 = nn.Linear(500, 500)
        # self.hidden2 = nn.Linear(500, 500)
        # self.policy = nn.Linear(500, 4)
        # self.value = nn.Linear(500, 1)

        self.num_of_frames = num_of_frames

        self.h = torch.zeros(1, 256)

        self.norm1 = nn.BatchNorm2d(num_of_frames)
        self.norm2 = nn.BatchNorm2d(32)

        self.conv1 = nn.Conv2d(num_of_frames, 32, num_of_frames, stride=2, padding=1)
        self.conv2 = nn.Conv2d(32, 32, 3, stride=2, padding=1)
        self.conv3 = nn.Conv2d(32, 32, 3, stride=2, padding=1)
        self.conv4 = nn.Conv2d(32, 32, 3, stride=2, padding=1)

        self.gru = nn.GRUCell(1152, 256)
        self.policy = nn.Linear(256, num_of_frames)
        self.value = nn.Linear(256, 1)

        self.prelu1 = nn.PReLU()
        self.prelu2 = nn.PReLU()
        self.prelu3 = nn.PReLU()
        self.prelu4 = nn.PReLU()

        nn.init.xavier_uniform_(self.conv1.weight, gain=nn.init.calculate_gain('leaky_relu'))
        nn.init.constant_(self.conv1.bias, 0.01)
        nn.init.xavier_uniform_(self.conv2.weight, gain=nn.init.calculate_gain('leaky_relu'))
        nn.init.constant_(self.conv2.bias, 0.01)
        nn.init.xavier_uniform_(self.conv3.weight, gain=nn.init.calculate_gain('leaky_relu'))
        nn.init.constant_(self.conv3.bias, 0.01)
        nn.init.xavier_uniform_(self.conv4.weight, gain=nn.init.calculate_gain('leaky_relu'))
        nn.init.constant_(self.conv4.bias, 0.01)
        nn.init.constant_(self.gru.bias_ih, 0)
        nn.init.constant_(self.gru.bias_hh, 0)
        nn.init.xavier_uniform_(self.policy.weight, gain=nn.init.calculate_gain('leaky_relu'))
        nn.init.constant_(self.policy.bias, 0.01)
        nn.init.xavier_uniform_(self.value.weight, gain=nn.init.calculate_gain('leaky_relu'))
        nn.init.constant_(self.value.bias, 0.01)

        self.train()


    def reset(self):
        self.h = torch.zeros(1, 256)

    def forward(self, state):

        # state = self.input(state)
        # state = self.hidden1(state)
        # state = self.hidden2(state)
        #
        # policy = F.softmax(self.policy(state))
        # value = self.value(state)
        #
        # return value, policy
        state = state.view(1, self.num_of_frames, 96, 96)
        state = self.norm1(state)

        data = self.prelu1(self.conv1(state))
        data = self.prelu2(self.conv2(data))
        data = self.prelu3(self.conv3(data))
        data = self.prelu4(self.conv4(data))

        data = self.norm2(data)
        data = data.view(1, -1)

        h = self.gru(data, self.h)
        self.h = h.detach()

        pre_policy = h.view(-1)

        policy = F.softmax(self.policy(pre_policy))
        value = self.value(pre_policy)

        return value, policy


class Trainer:

    def __init__(self, num_of_frames, gamma):
        self.agent = Agent(num_of_frames)
        self.num_of_frames = num_of_frames
        self.gamma = gamma
        self.optimizer = optim.Adam(self.agent.parameters(), lr=1e-4)

    def train(self, episodes, render):
        sim = SimWrap()
        sim.init()
        sim.reset()
        all_episodes, all_rewards = [], []
        possible_actions = [[-0.8, 0.0, 0.0], [0.8, 0.0, 0], [0.0, 0.1, 0.0], [0.0, 0.0, 0.6]]
        for episode in range(episodes):
            states = deque([])
            done = False
            total_reward = 0
            if episode < episodes - 10:
                rewards, values, policies, actions = [], [], [], []
                action_count = 0
                negative_count = 0

                # we're pre-populating the states deque by taking first num_of_frames steps as "full throttle":
                # while len(states) < self.num_of_frames:
                #     env.step([0.0, 0.0, 0.0])
                #     #state = env.render(mode='rgb_array')
                #     states.append(state)
                state, _, _ = sim.step([0, 1, 0])
                while not done:
                    #_input = preprocess(states)
                    if action_count > 200:

                        self.apply_gradients(policies, actions, rewards, values)
                        rewards, values, policies, actions = [], [], [], []
                        action_count = 0
                    action_ix, value, policy = self.get_action(state, False)
                    action = np.array(possible_actions[action_ix], dtype=np.float32)
                    state, reward, done, _ = sim.step(action)
                    if render:
                        env.render()

                    # state = env.render(mode='rgb_array')
                    # states.append(state)
                    # while len(states) > self.num_of_frames:
                    #     states.popleft()
                    rewards.append(reward)
                    values.append(value)
                    policies.append(policy)
                    actions.append(action_ix)
                    total_reward += reward
                    action_count += 1
                    if reward < 0:
                        negative_count += 1
                    else:
                        negative_count = 0
                    if negative_count > 30:
                        done = True

                sim.reset()
                #env.close()

                self.apply_gradients(policies, actions, rewards, values)
            else:
                state, _, _, _ = env.step([0, 1, 0])
                while not done:
                    action_ix, _, _ = self.get_action(state, True)
                    action = np.array(possible_actions[action_ix], dtype=np.float32)
                    state, reward, done, _ = sim.step(action)
                    #env.render()
                    total_reward += reward

            all_episodes.append(episode)
            all_rewards.append(total_reward)
            print("episode: {}, reward: {}".format(episode, total_reward))

            plot(all_episodes, all_rewards)

    def apply_gradients(self, policies, actions, rewards, values):
        actions_one_hot = torch.tensor([[int(i == action) for i in range(3)] for action in actions], dtype=torch.float32)

        policies = torch.stack(policies)
        values = torch.cat(values)
        values_nograd = torch.zeros_like(values.detach(), requires_grad=False)
        values_nograd.copy_(values)

        discounted_rewards = self.discount_rewards(rewards)
        advantages = discounted_rewards - values_nograd

        log_policies = torch.log(0.00000001 + policies)

        one_log_policies = torch.sum(log_policies * actions_one_hot, dim=1)

        entropy = torch.sum(policies * -log_policies)

        policy_loss = -torch.mean(one_log_policies * advantages)

        value_loss = F.mse_loss(values, discounted_rewards)

        value_loss_nograd = torch.zeros_like(value_loss)
        value_loss_nograd.copy_(value_loss)

        policy_loss_nograd = torch.zeros_like(policy_loss)
        policy_loss_nograd.copy_(policy_loss)

        loss = policy_loss + 0.5 * value_loss - 0.01 * entropy
        self.agent.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(self.agent.parameters(), 40)

        # update the weights with the computed gradients:
        self.optimizer.step()

        return float(loss.detach())

    def discount_rewards(self, rewards):
        discounted_rewards = [0 for _ in rewards]
        loop_rewards = [clip_reward(reward) for reward in rewards]
        loop_rewards.append(0)

        for main_ix in range(len(discounted_rewards) - 1, -1, -1):
            for inside_ix in range(len(loop_rewards) - 1, -1, -1):
                if inside_ix >= main_ix:
                    reward = loop_rewards[inside_ix]
                    discounted_rewards[main_ix] += self.gamma**(inside_ix - main_ix) * reward

        return torch.tensor(discounted_rewards)

    def get_action(self, state, show):
        input_list = []
        for o in state:
            for j in o:
                for k in j:
                    input_list.append(k)
        value, policy = self.agent.forward(torch.Tensor(input_list))
        if show:
            action_ix = np.argmax(torch.tensor(policy).detach().numpy())
        else:
            action_ix = np.random.choice(3, 1, p=torch.tensor(policy).detach().numpy())[0]
        return action_ix, value, policy


def clip_reward(reward):
    """ Clips the rewards into the <-3, 3> range preventing too big of the gradients variance."""

    return max(min(reward, 3), -3)


def preprocess(states):
    return torch.stack([torch.tensor(preprocess_one(image_data), dtype=torch.float32) for image_data in states])


def preprocess_one(image):
    """
    Scales the rendered image and makes it grayscale
    """
    return rescale(rgb2gray(image), (0.24, 0.16), anti_aliasing=False, mode='edge', multichannel=False)


def plot(all_episodes, all_rewards):
    fig = plt.figure()
    sub = fig.add_subplot(111)
    sub.plot(all_episodes, all_rewards)
    fig.savefig('test-plot.jpg')
    plt.close(fig)


if __name__ == "__main__":
    trainer = Trainer(3, gamma=0.999)
    trainer.train(episodes=1000, render=False)
