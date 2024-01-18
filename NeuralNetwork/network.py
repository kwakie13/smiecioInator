import os
import sys
from os import path

import torch
import torch.nn as nn
import torch.nn.functional as f
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
from PIL import Image

BATCH_SIZE = 2

transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

train_set = torchvision.datasets.ImageFolder(root="./Assets/training_set/", transform=transform)
train_loader = torch.utils.data.DataLoader(train_set, batch_size=BATCH_SIZE, shuffle=True, num_workers=2)

test_set = torchvision.datasets.ImageFolder(root="./Assets/test_set/", transform=transform)
test_loader = torch.utils.data.DataLoader(test_set, batch_size=BATCH_SIZE, shuffle=True, num_workers=2)

classes = ("glass", "metal", "paper", "plastic")
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)  # 3 input neurons - R,G and B channels
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 71 * 71, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 4)  # four output neurons - four trash types in project

    def forward(self, x):
        x = self.pool(f.relu(self.conv1(x)))
        x = self.pool(f.relu(self.conv2(x)))
        x = x.view(x.size(0), 16 * 71 * 71)
        x = f.relu(self.fc1(x))
        x = f.relu(self.fc2(x))
        x = self.fc3(x)
        return x


def training_network():
    print("Starting neural network training...")

    net = Net()
    net = net.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)

    for epoch in range(50):  # over 50 - no significant change in loss, approx. 12 minutes on GPU
        running_loss = 0.0
        for i, data in enumerate(train_loader, 0):
            inputs, labels = data[0].to(device), data[1].to(device)
            optimizer.zero_grad()
            outputs = net(inputs.to(device))
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            if i % 2000 == 1999:
                print("[%d, %5d] loss: %.3f" % (epoch + 1, i + 1, running_loss))
                running_loss = 0.0

    print("Finished training!")

    save_network_to_file(net)


def result_from_network(net, loaded_image):
    image = Image.open(loaded_image)
    pil_to_tensor = transforms.ToTensor()(image.convert("RGB")).unsqueeze_(0)
    outputs = net(pil_to_tensor)

    return classes[torch.max(outputs, 1)[1]]


def save_network_to_file(network):
    torch.save(network.state_dict(), "./NeuralNetwork/network_model.pth")
    print("Network saved to file!")


def load_network_from_structure(network):
    network.load_state_dict(torch.load("./NeuralNetwork/network_model.pth", map_location=torch.device('cpu')))


def save_network_to_txt(network):
    original_stdout = sys.stdout

    with open("./NeuralNetwork/network_in_txt.txt", "w") as file:
        sys.stdout = file
        print(network)
        sys.stdout = original_stdout


def testing_network():
    print("Testing network...")

    net = Net()
    net.to(device)
    load_network_from_structure(net)

    correct = 0
    total = 0

    with torch.no_grad():
        for data in test_loader:
            images, labels = data[0].to(device), data[1].to(device)
            outputs = net(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    print("Accuracy of the network on the test images: %d %%\n" % (100 * correct / total))

    correct_pred = {classname: 0 for classname in classes}
    total_pred = {classname: 0 for classname in classes}

    with torch.no_grad():
        for data in test_loader:
            images, labels = data[0].to(device), data[1].to(device)
            outputs = net(images)
            _, predictions = torch.max(outputs, 1)
            for label, prediction in zip(labels, predictions):
                if label == prediction:
                    correct_pred[classes[label]] += 1
                total_pred[classes[label]] += 1

    for classname, correct_count in correct_pred.items():
        accuracy = 100 * float(correct_count) / total_pred[classname]
        print("Accuracy for class {:5s} is: {:.1f} %".format(classname, accuracy))


if __name__ == "__main__":
    if path.isfile("./NeuralNetwork/network_model.pth") and not os.stat(
            './NeuralNetwork/network_model.pth').st_size == 0:
        testing_network()
    else:
        training_network()
