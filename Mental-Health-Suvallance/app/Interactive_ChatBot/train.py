import json
from app.Interactive_ChatBot.nltk_utils import tokenize,stem,bag_of_words
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset,DataLoader
from app.Interactive_ChatBot.model import NeuralNet
with open('app/Interactive_ChatBot/intents.json','r') as f :
    intents=json.load(f)

all_word=[]
tags=[]

xy=[]

for intent in intents['intents']:
    tag=intent['tag']
    tags.append(tag)
    for patterns in intent['patterns']:
        w=tokenize(patterns)
        all_word.extend(w)
        xy.append((w,tag))

ignore_words=['?','!','.',',']
all_word=[stem(w) for w in all_word if w not in ignore_words]
all_word=sorted(set(all_word))
# print(all_word)

tags=sorted(set(tags))
# print(tags)

x_train=[]
y_train=[]
for (pattern_Sentence,tag) in xy:
    bag=bag_of_words(pattern_Sentence,all_word)
    x_train.append(bag)

    label=tags.index(tag)
    y_train.append(label)

x_train=np.array(x_train)
y_train=np.array(y_train)

#Hyper Parameters
batch_size=8
hidden_size=8
output_size=len(tags)
input_size=len(x_train[0])
learning_rate=0.001
num_epochs=1000
# print(input_size,len(all_word))
# print(output_size,tags)

class ChatDataset(Dataset):
    def __init__(self) -> None:
        self.n_samples=len(x_train)
        self.x_data=x_train
        self.y_data=y_train

    def __getitem__(self,index):
        return self.x_data[index],self.y_data[index]
    
    def __len__(self):
        return self.n_samples


dataset=ChatDataset()
train_loader=DataLoader(dataset=dataset,batch_size=batch_size,shuffle=True,num_workers=0)

device=torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model=NeuralNet(input_size,hidden_size,output_size).to(device)

#loss and optimizer
criterion=nn.CrossEntropyLoss()
optimizer=torch.optim.Adam(model.parameters(),lr=learning_rate)

for epoch in range(num_epochs):
    for (words,labels) in train_loader:
        words=words.to(device)
        labels=labels.to(dtype=torch.long).to(device)

        #forward pass
        outputs=model(words)
        loss=criterion(outputs,labels)

        #backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    
    if (epoch+1)%100==0:
        print(f'epoch{epoch+1}/{num_epochs},loss={loss.item():.4f}')
print(f'final loss,loss={loss.item():.4f}')

data={
    "model_state":model.state_dict(),
    "input_size":input_size,
    "output_size":output_size,
    "hidden_size":hidden_size,
    "all_words":all_word,
    "tags":tags
}

FILE="data.pth"
torch.save(data,FILE)
print(f"training complete.file saved to {FILE}")

