output = ''
num_cards = 3
tot_cards = 0
fin = False
for i in range(1,6):
    if fin or tot_cards +1 > num_cards:
        break
    tot_cards += 1
    current = 'u'
    for j in range(0,i-1):
        if(tot_cards >= num_cards):
            fin = True
            break
        current += 'd'
        tot_cards += 1
    output += f"{current}\n"
    
print(f"{output}")


