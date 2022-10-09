amount = input()
years = input()
print("year","Start","paid in","interest","Final")
final = 0
for i in range (1, int(years)):
    Start = final
    interest = (int(Start) + int(amount)) * 0.1
    final = int(Start) + int(amount) + int(interest)
    print(i, Start, amount, interest, final)

