import matplotlib.pyplot as plt
import math
import matplotlib.patches as mpatches  
def main():
    
    
    acc=[]
    loss=[]
    val_loss=[]
    val_acc=[]
    for i in range(2,9):
        num=pow(2,i)
        arr=[]
        count=0
        with open('output'+str(num)+'.txt','r') as f:
            for line in f:
                count+=1;
                if count>=8 and (count-8)%3==0:
       
                    arr.append(line.strip())
        f.close()
        for i in range(20):
            n=arr[i].split('-')
            print(n[2])
            m=n[2].split(' ')
            loss.append(m[2])
            m=n[3].split(' ')
            acc.append(m[2])
            m=n[4].split(' ')
            val_loss.append(m[2])
            m=n[5].split(' ')
            val_acc.append(m[2])
    plt.subplot(211)  
    plt.plot(acc)  
    plt.plot(val_acc)  
    plt.title('model accuracy')  
    plt.ylabel('accuracy')  
    plt.xlabel('epoch')  
    plt.legend(['train', 'test'], loc='upper left')  
   
    # summarize history for loss  
   
    plt.subplot(212)  
    plt.plot(loss)  
    plt.plot(val_loss)  
    plt.title('model loss')  
    plt.ylabel('loss')  
    plt.xlabel('epoch')  
    plt.legend(['train', 'test'], loc='upper left')  
    plt.savefig("plot.png")

        
    
main()
